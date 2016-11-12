import copy
from flask import Flask, render_template, flash, request
from wtforms import Form
from forms import TwilioForm
from twilio.rest import TwilioRestClient
import twilio.twiml
from db_handler import db_handler
app = Flask(__name__)
app.config.from_object('config')

import time
import config_twilio
#basic parameters, subject to change

APPLICANT = {
        'name': None,
        'phone_number': None,
        'age': None,
        'location': None
        }

MSG = {
	'msg_id': None,
	'from': None,
	'to': None,
	'body': None,
	'responded': False
}

MY_NUMBER = '2132109968'

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
    return 'nothing'

@app.route('/send', methods=['GET', 'POST'])
def to_send():
    form = TwilioForm()
    if request.method == 'POST':
    	print form.validate()
        print request.values.get('phone_number')
        print request.values.get('From')
    	if form.validate_on_submit():
    	    #update the database
    	    my_handler = db_handler()
    	    new_msg['msg_id'] = int(form.phone_number) + int(time.time())
    	    new_msg['to'] = form.phone_number
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

if __name__=="__main__":
    app.run(debug=True)
