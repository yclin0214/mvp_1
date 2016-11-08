from flask import Flask, render_template, flash, request
from wtforms import Form
from forms import TwilioForm

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def to_send():
    form = TwilioForm()
    if request.method == 'POST':
    	print form.validate()
    	print form.phone_number
    	print form.message_body
    	
    	if form.validate_on_submit():
    	    print "submitted"
    	    return "Submitted"
    	else:
    	    print form.errors
    
    return render_template('twilioform.html', titile='To Send', form = form)

if __name__=="__main__":
    app.run(debug=True)
