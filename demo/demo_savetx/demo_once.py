import sys
sys.path.append('/home/mmlab/Logchain/logchain_monitoring')
from demo.demo_savetx import transaction_generator
from PyQt5 import QtCore, QtGui, QtWidgets
from demo.demo_savetx import request_test

import queue
import time
transaction_queue = queue.Queue()

class LogchainDemo_cycle(object):
    requests_url = ""
    def generate_transaction(self):

        tx= transaction_generator.transaction_generator()
        transaction_queue.put(tx)

    def set_request_url(self, url="http://163.239.25.42:5000/tx/save/"):
        self.requests_url = url

    def send_transaction(self):
        tx= transaction_queue.get()
        try:
            response=request_test.post_transaction(self.requests_url,tx)
            print(response.text)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please input request url")
    else :
        #print(sys.argv[1])
        demo = LogchainDemo_cycle()
        demo.generate_transaction()
        demo.set_request_url(url=sys.argv[1])
        demo.send_transaction()
