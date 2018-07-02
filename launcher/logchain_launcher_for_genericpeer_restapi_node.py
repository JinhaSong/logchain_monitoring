import logging
import sys
sys.path.append('D:\\CloudStation\\Project\\Logchain\\logchain_monitoring')

import threading

from PyQt5 import QtWidgets
from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from queue import Queue
from peerproperty import nodeproperty
from peerproperty import set_peer
from storage import file_controller
from communication.restapi_dispatch import save_tx_queue, contract_execution_queue
from communication.restapi_dispatch import contract_deploy_queue, query_block_queue
from communication.restapi_dispatch import infopage
from communication.peermgr import peerconnector
from service.blockmanager import genesisblock
from communication.msg_dispatch import dispatch_queue_list
from communication.msg_dispatch import t_type_queue_thread
from communication.msg_dispatch import b_type_queue_thread
from communication.msg_dispatch import v_type_queue_thread
from communication.p2p import receiver
from monitoring import monitoring


app = Flask(__name__)

query_q = Queue()
savetx_q = Queue()
smartcontract_deploy_q = Queue()
smartcontract_execute_q = Queue()


@app.route('/contract/deploy/', methods=['POST'])
def contract_deploy():
    monitoring.log('log.request(deploy smart contract) rcvd.')
    if not request.json or not 'contract_title' in request.json or not 'contract_body' in request.json or not 'contract_args' in request.json:
        abort(400)
    smartcontract_deploy_q.put((request.json,request.remote_addr))
    monitoring.log("log."+str(smartcontract_deploy_q))
    monitoring.log("log." + str(smartcontract_deploy_q.qsize()))
    return jsonify({
        "contract_title": request.json["contract_title"],
        "contract_body": request.json["contract_body"],
        "contract_args": request.json["contract_args"],
        'info' : "You can see the deployed contract address list via the following link:"
                 "http://host:5000/info/contract/deployed/"
    }), 201




@app.route('/contract/execute/', methods=['POST'])
def contract_execute():
    monitoring.log('log.request(execute contract) rcvd.')

    if not request.json or not 'contract_addr' in request.json or not 'contract_function' in request.json or not 'contract_args' in request.json:
        abort(400)
    smartcontract_execute_q.put((request.json, request.remote_addr))
    monitoring.log("log."+str(smartcontract_execute_q))
    monitoring.log("log." + str(smartcontract_execute_q.qsize()))
    return jsonify({
        "contract_addr": request.json["contract_addr"],
        "contract_function": request.json["contract_function"],
        "contract_args": request.json["contract_args"],
        'info' : "You can see the executed contract list via the following link:"
                 "http://host:5000/info/contract/executed/"
    }), 201



@app.route('/tx/save/', methods=['POST'])
def tx_save():
    monitoring.log('log.request(save tx) rcvd...')
    if not request.json or not 'tx_title' in request.json:
        abort(400)
    savetx_q.put((request.json, request.remote_addr))
    monitoring.log("log."+str(savetx_q))
    monitoring.log("log."+str(savetx_q.qsize()))

    monitoring.log("transaction." + str(savetx_q) + '(' + str(savetx_q.qsize()) + ')')

    return jsonify({
        "tx_title": request.json["tx_title"],
        "tx_body": request.json["tx_body"],
        'info' : "You can see the tx address via the following link:"
                 "http://host:5000/info/tx/"
    }), 201


@app.route('/info/tx/', methods=['GET'])
def get_txinfo():
    return jsonify(infopage.SavedTxList)


@app.route('/info/contract/deployed/', methods=['GET'])
def get_contract_deployed_info():
    return jsonify(infopage.DeployedSmartContractList)

@app.route('/info/contract/deployed/result/', methods=['GET'])
def get_contract_deployed_result_info():
    return jsonify(infopage.DeployedSmartContractResultList)


@app.route('/info/contract/executed/', methods=['GET'])
def get_contract_executed_info():
    return jsonify(infopage.ExecutedSmartContractList)

@app.route('/info/contract/executed/result/', methods=['GET'])
def get_contract_executed_result_info():
    return jsonify(infopage.ExecutedSmartContractResultList)



@app.route("/")
def hello():
    return "Logchain-s launcher for Generic Peer - REST API node"


def initialize_process_for_generic_peer():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    monitoring.log("log.Start Logchain launcher for Generic Peer...")

    initialize()

    monitoring.log('log.Run processes for PeerConnector.')
    if not peerconnector.start_peerconnector():
        monitoring.log('log.Aborted because PeerConnector execution failed.')
        sys.exit(1)

    set_peer.set_my_peer_num()
    monitoring.log("log.My peer num: " + str(nodeproperty.My_peer_num))

    'Genesis Block Create'
    genesisblock.genesisblock_generate()

    monitoring.log("log.Start a thread to receive messages from other peers.")
    recv_thread = receiver.ReceiverThread(
        1, "RECEIVER", nodeproperty.My_IP_address, nodeproperty.My_receiver_port)
    recv_thread.start()
    monitoring.log("log.The thread for receiving messages from other peers has started.")


    t_type_qt = t_type_queue_thread.TransactionTypeQueueThread(
        1, "TransactionTypeQueueThread",
        dispatch_queue_list.T_type_q
    )
    t_type_qt.start()

    v_type_qt = v_type_queue_thread.VotingTypeQueueThread(
        1, "VotingTypeQueueThread",
        dispatch_queue_list.V_type_q
    )
    v_type_qt.start()

    b_type_qt = b_type_queue_thread.BlockTypeQueueThread(
        1, "BlockTypeQueueThread",
        dispatch_queue_list.B_type_q
    )
    b_type_qt.start()


def initialize():
    monitoring.log('log.Start the blockchain initialization process...')
    file_controller.remove_all_transactions()
    file_controller.remove_all_blocks()
    file_controller.remove_all_voting()
    monitoring.log('log.Complete the blockchain initialization process...')
    set_peer.init_myIP()

def initialize_process_for_RESTAPInode():
    queryqueue_thread = query_block_queue.QueryQueueThread(
        1, "QueryQueueThread", query_q
    )
    queryqueue_thread.start()
    logging.debug('QueryQueueThread started')

    savetxqueue_thread = save_tx_queue.RESTAPIReqSaveTxQueueThread(
        1, "RESTAPIReqSaveTxQueueThread", savetx_q
    )
    savetxqueue_thread.start()
    logging.debug('RESTAPIReqSaveTxQueueThread started')

    contract_deploy_restapi_thread = contract_deploy_queue.RESTAPIReqContractDeployQueueThread(
        1, "RESTAPIReqContractDeployQueueThread", smartcontract_deploy_q
    )
    contract_deploy_restapi_thread.start()
    logging.debug('RESTAPIReqContractDeployQueueThread started')


    contract_exec_restapi_thread = contract_execution_queue.RESTAPIReqContractExecutionQueueThread(
        1, "RESTAPIReqContractExecutionQueueThread", smartcontract_execute_q
    )
    contract_exec_restapi_thread.start()
    logging.debug('RESTAPIReqContractExecutionQueueThread started')


def monitoring_run(args=None):
    monitor_app = QtWidgets.QApplication(sys.argv)
    monitoring.Main_form = monitoring.Form(args)
    monitor_app.exec()


# REST API Node launcher function
if __name__ == "__main__":
    logging.basicConfig(stream = sys.stderr, level = logging.DEBUG)

    argv = sys.argv
    hostname = '0.0.0.0'

    if len(argv) == 2:
        arg_1 = argv[1]
        if arg_1 == "monitor":
            initialize_process_for_generic_peer()
            initialize_process_for_RESTAPInode()
            t = threading.Thread(target=monitoring_run, args='')
            t.start()
            sys.exit(app.run(host=hostname, threaded=True))
    elif len(argv) == 3:
        arg_1 = argv[1]
        arg_2 = argv[2]
        if arg_1 == "monitor":
            if arg_2 == "mini":
                initialize_process_for_generic_peer()
                initialize_process_for_RESTAPInode()
                t = threading.Thread(target=monitoring_run, args='m')
                t.start()
                sys.exit(app.run(host=hostname, threaded=True))
            elif arg_2 == "ex":
                initialize_process_for_generic_peer()
                initialize_process_for_RESTAPInode()
                t = threading.Thread(target=monitoring_run, args='ex')
                t.start()
                sys.exit(app.run(host=hostname, threaded=True))
            else:
                print("wrong argument !!")
    else:
        initialize_process_for_generic_peer()
        initialize_process_for_RESTAPInode()
        app.run(host=hostname)
