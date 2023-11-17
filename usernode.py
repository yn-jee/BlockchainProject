from multiprocessing import Process
import transaction as tx
class user_node(tx.transaction):
    def __init__(self, node_num):
        ...