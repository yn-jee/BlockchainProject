from multiprocessing import Process
import time
import transaction as tx

class full_node(tx.transaction):
    def __init__(self, node_num, stack_matrix):
        super().__init__()
        self.node_num = node_num

        # stack_matrix의 i번째 열의 원소들을 자신의 send_stack에 저장
        self.send_stack = []
        for row in stack_matrix:
            self.send_stack.append(row[node_num])

        # stack_matrix의 i번째 행을 자신의 recv_stack으로 사용
        self.recv_stack = stack_matrix[node_num]

        full_num = len(stack_matrix)
        for i in range(full_num):
            if self.send_stack[i] != None and self.send_stack[i]:
                self.send_stack[i].pop()

        self.test = 0

    # def connect(self, peer_full):  # PRNG로 생성된 topology에 의해 선택된 쌍을 잇기







    """def send_message(self, message):
        print(f"{self.node_num} sending: {message}")
        self.send_stack.put(message)

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
