from multiprocessing import Process
import transaction as tx
import random as rd
import ecdsa as ec
from hashlib import sha256
class user_node(tx.transaction):
    def __init__(self, node_num, queue_user, sk, vk, stack_matrix_user, other_users):
        super().__init__()
        # send_queue로 네트워크에 트랜잭션 전파
        self.send_queue = queue_user

        # 사용자끼리의 거래 기록을 stack_matrix_user에 저장
        # stack_matrix_user i번째 열의 원소들을 자신의 send_stack_tx에 저장
        # 여기에 자신이 판매자인 transaction을 공유
        self.send_stack_tx = []
        for row in stack_matrix_user:
            self.send_stack_tx.append(row[node_num])

        # stack_matrix_user i번째 행을 자신의 send_stack_tx에 저장
        # 여기서 자신이 구매자인 transaction을 공유받음
        self.recv_stack_tx = stack_matrix_user[node_num]

        self.sk = ec.SigningKey.from_string(sk, curve=ec.SECP256k1, hashfunc=sha256)
        self.vk = ec.VerifyingKey.from_string(vk, curve=ec.SECP256k1, hashfunc=sha256)


        self.other_users = other_users

        #----무작위 개수만큼 자동차 생성----
        # 자동차 개수 설정
        self.cars_num = rd.randint(3, 11)
        # 자동차 개수만큼 자동차 생성 및 저장
        # self.cars = [] ... 필요 없을 것 같음
        # self.txs = []도 필요없음. recv_stack_tx에 저장됨


    """def run_user(self):
        # user node가 소유한 자동차 별로 트랜잭션을 생성하고, full node와 공유하는 queue에 put
        for i in range(self.cars_num):
            car = tx.vehicle()
            Vid, modelName, manufacturedTime = car.get_vehicle_data()
            new_tx = tx.transaction(Vid, modelName, manufacturedTime)
            self.cars.append(car)
            self.txs.append(new_tx)
            #   큐에 넣으려면 서명 과정이 필요함 .............
            #   input은 특정 자동차의 판매자(seller)의 public key이며,
            #   output은 이 자동차의 구매자(buyer)의 public key에 해당한다.
            #   또한 트랜잭션은 <trID, Vid, tradeCnt, modelName, manufacturedTime, price, tradingTime, others>의 값들을 포함

            #sign the tx
            #self.send_queue.put(new_tx)

            print("put tx")"""

    def run_user(self, txid, vout, sig):
        # 처음 실행할 때
        # user node가 소유한 자동차 별로 트랜잭션을 생성하고, full node와 공유하는 queue에 put
        for i in range(self.cars_num):
            car = tx.vehicle()
            Vid, modelName, manufacturedTime = car.get_vehicle_data()

            new_tx_in = tx.tx_in(txid, vout, sig)
            new_tx_out = tx.tx_out(self.vk, Vid, modelName, manufacturedTime)
            new_tx = tx.transaction(new_tx_in, new_tx_out)
            self.recv_stack_tx[0].append(new_tx)    # 첫번째 recv 배열에 자신이 가진 차들을 저장

        # 그 이후
        # 약 15초 간격으로 트랜잭션 발생
        # 자신이 관리하는 자동차 라면 자신이 그 구매 트랜잭션을 알고 있어야. ...

        # while True:
        i = 0
        while i < 10: # 임시로 10번만
            for row in self.recv_stack_tx:    # 자기가 트랜잭션 받을 배열들의 개수만큼
                # 트랜잭션 생성 후 랜덤한 사용자에게 보내기
                if row:
                    i = i + 1
                    top_of_stack = self.recv_stack_tx.pop() # 자신이 받은 트랜잭션이라면 output이 자신의 vk
                    tx_out = top_of_stack.vout






    def put_queue(self, tx, queue):
        queue.put(tx)

#print()
