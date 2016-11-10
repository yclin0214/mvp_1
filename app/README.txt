Some configuration and setup:
1. set up a virtual environment within a directory
2. within in a virtual environment, pip install flask, pip install twilio binary, pip install pymongo (python wrapper for mongoDB)
3. remember to use .gitignore exclude binary files, do not include it in git push
4. twilio account is personalized, so the test won't work for a different number. Need to register a new test account
5. Use ngrok to re-route the local IP address to a public-accessible IP address to let twilio service discover the web service

The next steps:
1. Implement the database handler for mongoDB and integrate into the main.py (can also be renamed as views.py) 
2. Implement the front end for multi-users interaction mode
3. Open a commercial twilio account
4. Integrate with api.ai (the idea is that any message sent/received through twilio service will be saved in mongoDB, and another nlp related module will parse the the messages for every user)
5. Once we finish implementing the SMS-based model, we can go for some initial testing with both human-driven and NLP-driven approaches
