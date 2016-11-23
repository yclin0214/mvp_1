#import python native libraries
import copy
import time
#import flask related files and libraries
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form
#import twilio related file
from forms import TwilioForm
from twilio.rest import TwilioRestClient
import twilio.twiml
from config_twilio import *
#import database related file
from db_handler import db_handler

app = Flask(__name__)
app.config.from_object('config')



#basic parameters, subject to change

APPLICANT = {
        'phone_number': None,
        'name': None,
        'age': None,
        'location': None,
        'count': None #number of the messages
        }

MSG = {
	'msg_id': None,
	'phone_number': None,
	'from': None, #if 'from' equals to 'phone_number', then it's sent by the user
	'body': None,
	'responded': False
}

MY_NUMBER = '2132109968'

#Test admin features (bad practice here)
num_msg_dict = {'':[]}
last_update_time = 0;
update_time = 0;

@app.route('/', methods=['GET', 'POST'])
def to_receive():
    #instantiate a db handler
    msg_id = request.values.get('MessageSid')
    if msg_id:
    	#Todo: need to check if the number is legit
    	my_handler = db_handler()
        new_msg = copy.deepcopy(MSG)
        incoming_number = request.values.get('From')
        new_msg['msg_id'] = msg_id
        new_msg['from'] = incoming_number
        new_msg['to'] = 'our_server'
        new_msg['body'] = request.values.get('Body')
        my_handler.msg_collection.insert_one(new_msg)
        print "***Debug: new message added!***"
        
        if my_handler.applicant_collection.find({'phone_number':incoming_number}) == None:
        	print "**debug**"
        	new_applicant = copy.deepcopy(APPLICANT)
       		new_applicant['phone_number'] = incoming_number
       		new_applicant['location'] = request.values.get('FromCity')
        	my_handler.applicant_collection.insert_one(new_applicant)
        	print "***Debug: new applicant added!***"

        for applicant in my_handler.applicant_collection.find():
        	print
        	print "***Debug***"
        	print applicant['phone_number']
        	print applicant['location']
        my_handler.close()
        
    #add to num_msg_dict and send to admin. Todo: bad practice, just to test
    num_msg_dict[incoming_number].append(request.values.get('Body'))
    update_time = time.time()
    return 'nothing'

@app.route('/send', methods=['GET', 'POST'])
#Todo: need to debug this function
def to_send():
    form = TwilioForm()
    if request.method == 'POST':
    	print form.validate()
        print request.values.get('phone_number')
        print request.values.get('From')
    	if form.validate_on_submit():
    	    #update the database
            new_msg = copy.deepcopy(MSG)
    	    my_handler = db_handler()
    	    new_msg['msg_id'] = int(form.phone_number.data)+int(time.time())
    	    new_msg['to'] = form.phone_number.data
    	    new_msg['from'] = 'our_server'
    	    new_msg['body'] = form.message_body.data
    	    my_handler.msg_collection.insert_one(new_msg)
    	    my_handler.close()
    	    #send through twilio
            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages.create(to=form.phone_number.data,from_=TWILIO_NUMBER, body=form.message_body.data)
    	    return "Submitted"
    	else:
    	    print form.errors

    return render_template('twilioform.html', titile='To Send', form = form)

@app.route('/history', methods=['GET'])
def show_all_entry():
    my_handler = db_handler()
    for msg in my_handler.msg_collection.find():
    	print "***Debug***"
    	print msg['msg_id']
        print msg['from']
        print msg['body']
    return ' '

@app.route('/admin', methods=['GET'])
def admin_entry():
    return render_template('admin.html')

@app.route('/api/sms_post', methods=['GET','POST'])
def send_sms ():
    if request.method == 'POST':
    	number = request.form['number']
    	content = request.form['content']
    	print request.form['number']
    	print request.form['content']
    	num_msg_dict[number].append(content)
    	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(to=request.form['number'],from_=TWILIO_NUMBER, body=request.form['content'])
    	return jsonify({'status': 'send succeeds'})
    return jsonify({'status': 'send fails'})

@app.route('/api/contact_updates', methods=['GET'])
def send_contact_update():
    if (update_time > last_update_time):
    	#There's update. Process the message counts of each number and send update. It's okay to have inefficient algorithm here for now.
    	contact_dict = {'': int}
    	for number in num_msg_dict:
    	    contact_dict[number] = len(num_msg_dict[number])
    	return jsonify({'contact_list':contact_dict})
    return jsonify({'contact_list': None})

@app.route('/api/message_updates', methods=['GET'])
def list_messages():
    count = request.form['count']
    number = request.form['number']
    if number is not None:
        if len(num_msg_dict[number]) > count:
            return jsonify({'new_message_list':num_msg_dict[number][count:]})
    return jsonify({'new_message_list': None})

if __name__=="__main__":
    app.run(debug=True)
