from model.user_sms import UserSms
from db import Session
import threading

#print UserSms.update(1, 1, 1, '1233')

class  Counter(threading.Thread):
    def __init__(self):
        super(Counter, self).__init__()
        self.a = 1

    def run(self):
        print Session()


for i in range(3):
    Counter().start()

