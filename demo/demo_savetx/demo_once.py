import sys
sys.path.append('/workspace')
from demo.demo_savetx import transaction_generator
from PyQt5 import QtCore, QtGui, QtWidgets
from demo.demo_savetx import request_test

import queue
import time
transaction_queue = queue.Queue()

class LogchainDemo_cycle(object):
    requests_url = ""
    def generate_transaction(self):

        tx= transaction_generator.transaction_generator_realData()
        transaction_queue.put(tx)

    def set_request_url(self, url):
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
        demo = LogchainDemo_cycle()
        demo.generate_transaction()
        demo.set_request_url(sys.argv[1])
        demo.send_transaction()
