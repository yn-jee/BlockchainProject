from multiprocessing import Process
import time
import block as bl

class full_node(bl.block):
    def __init__(self, node_num, stack_matrix_block, stack_matrix_tx, queue_user):
        super().__init__()
        self.node_num = node_num

        # block_stack_matrix의 i번째 열의 원소들을 자신의 send_stack_block에 저장
        self.send_stack_block = []
        for row in stack_matrix_block:
            if row[node_num]:
                self.send_stack_block.append(row[node_num])

        # block_stack_matrix의 i번째 행을 자신의 recv_stack_block으로 사용
        self.recv_stack_block = [row for row in stack_matrix_block[node_num] if row != None]

        """full_num = len(stack_matrix_block)
        for i in range(full_num):
            if self.send_stack_block[i] != None and self.send_stack_block[i]:
                self.send_stack_block[i].pop()
                self.send_stack_block[i].append(1313)
                self.send_stack_block[i].append("done")"""

        # stack_matrix_tx의 i번째 열의 원소들을 자신의 send_stack_tx에 저장
        self.send_stack_tx = []
        for row in stack_matrix_tx:
            self.send_stack_tx.append(row[node_num])

        # stack_matrix_tx의 i번째 행을 자신의 recv_stack_tx로 사용
        self.recv_stack_tx = stack_matrix_tx[node_num]
        self.recv_queue = queue_user
        self.utxo_pool = []


    def run_full(self, genesis):
        self.recv_stack_block[0].append(genesis)
        for _ in range(10): # while true로 바꾸기
            for row in self.recv_stack_block:
                temp_transactions = []
                if row:
                    print("block received")
                    # 여기서 블록검증 후 자신과 연결된 모든 send_stack_block을 통해 block 전파
                    top_of_stack = row.pop()    # 한 스택 내에서 가장 위의 것만 유효하다고 판단함
                    all_in_utxo_pool = True
                    #print("heights")
                    #temp_transactions = temp_transactions + (top_of_stack.list_of_transactions)

                    #merkle tree root validate
                    for i in range(len(top_of_stack.list_of_transactions)):
                        # block의 어느 transaction이 자신의 UTXO pool에 없다면 break
                        if not self.check_utxo_in_pool(top_of_stack.list_of_transactions[i]):
                            all_in_utxo_pool = False
                    # 모든 transaction이 자신의 UTXO pool에 있다면
                    #if all_in_utxo_pool:
                     #   for i in range(len(top_of_stack.list_of_transactions)):
                            # 그 블록 내 모든 트랜잭션이 전부 valid한지 확인



            """else:
                print("no block received")
                temp_block = bl.block()"""

    def check_utxo_in_pool(self, utxo):
        if utxo in self.utxo_pool:
            return True
        else:
            return False

    """def tx_validation(self, utxo):
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1,
                                            hashfunc=sha256)  # the default is sha1
        vk.verify(bytes.fromhex(sig), message)  # True"""



"""
1119
send_stack_block에서 None 빼는 중
자신과 연결된 ... 곳들에 제네시스 블록 보내기 하려고.

"""





"""def send_message(self, message):
        print(f"{self.node_num} sending: {message}")
        self.send_stack_block.put(message)

    def receive_message(self):
        while True:
            if not self.receive_stack.empty():
                message = self.receive_stack.get()
                print(f"{self.node_num} received: {message}")
            # time.sleep(1)  # Short delay to prevent excessive CPU usage
    def run(self):
        for i in range(5):
            self.send_message(f"Message {i} from {self.node_num}")
            time.sleep(1)  # Simulate processing delay
            self.receive_message()

def process_function(node):
    node.run()
    """
    # 큐의 리스트가 필요한가 해서...
