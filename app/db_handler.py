from pymongo import MongoClient

#Todo: It's a very pre-mature database handler. Need to do major rework later.

class db_handler():
    def __init__(self):
        # Todo:
        # We need to guarantee the database connection session is
        # alive all time
        self.client = MongoClient()
        self.msg_db = self.client['msg_db']
        self.msg_collection = self.msg_db['msg_collection']

        self.applicant_db = self.client['applicant_db']
        self.applicant_collection = self.applicant_db['applicant_collection']

    def close(self):
        self.client.close()
