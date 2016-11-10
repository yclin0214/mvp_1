#basic parameters, subject to change
NAME = 'name'
PHONE_NUMBER = 'phone_number'
MSGS_IN = 'msgs_in'
MSGS_OUT = 'msgs_out'
AGE = 'age'
LOCATION = 'location'
#APPLICANT is a single document to be saved into MongoDB
APPLICANT = {
        NAME: None,
        PHONE_NUMBER: None,
        #need to add a time stamp to msg in the future
        MSGS_IN: [],
        MSGS_OUT: [],
        AGE: None,
        LOCATION: None
        }
