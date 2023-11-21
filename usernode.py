from multiprocessing import Process
import transaction as tx
import random as rd
import ecdsa as ec
from hashlib import sha256
class user_node(tx.transaction):
    def __init__(self, node_num, queue_user, stack_matrix_user, other_users):
        super().__init__()

        self.node_num = node_num

        #----비대칭키 생성----
        # sk: signing key(private key)
        # vk: verifying key(public key)
        self.sk = ec.SigningKey.generate()
        self.vk = self.sk.verifying_key

        # 프로세스 실행 시 pickle 오류 방지를 위한 형태 변환
        self.sk = self.sk.to_string()
        self.vk = self.vk.to_string()

        # send_queue로 네트워크에 트랜잭션 전파
        self.send_queue = queue_user

        # 사용자끼리의 거래 기록을 stack_matrix_user에 저장
        # stack_matrix_user i번째 열의 원소들을 자신의 send_stack_tx에 저장
        # 여기에 자신이 판매자인 transaction을 공유
        self.send_stack_tx = []
        for row in stack_matrix_user:
            self.send_stack_tx.append(row[self.node_num])

        # stack_matrix_user i번째 행을 자신의 send_stack_tx에 저장
        # 여기서 자신이 구매자인 transaction을 공유받음
        self.recv_stack_tx = stack_matrix_user[self.node_num]

        self.other_users = other_users

        #----무작위 개수만큼 자동차 생성----
        # 자동차 개수 설정
        self.cars_num = rd.randint(3, 11)
        # 자동차 개수만큼 자동차 생성 및 저장
        # self.cars = [] ... 필요 없을 것 같음
        # self.txs = []도 필요없음. recv_stack_tx에 저장됨
#        self.run_user("", "")


    def run_user(self, txid, sig):
        # 처음 실행할 때
        # user node가 소유한 자동차 별로 트랜잭션을 생성하고, full node와 공유하는 queue에 put
        for i in range(self.cars_num):
            car = tx.vehicle()
            Vid, modelName, manufacturedTime = car.get_vehicle_data()

            new_tx_in = tx.tx_in(txid, sig)
            new_tx_out = tx.tx_out(self.vk, Vid, modelName, manufacturedTime)
            new_tx = tx.transaction(new_tx_in, new_tx_out)
            self.recv_stack_tx[0].append(new_tx)    # 첫번째 recv 배열에 자신이 가진 차들을 저장

        # 그 이후
        # 약 15초 간격으로 트랜잭션 발생
        # 자신이 관리하는 자동차 라면 자신이 그 구매 트랜잭션을 알고 있어야. ...

        # while True:
        #i = 0
        #while i < 10: # 임시로 10번만
        """if i == 2:
                print()"""
        for i in range(len(self.recv_stack_tx)):    # 자기가 트랜잭션 받을 배열들의 개수만큼
            # 트랜잭션 생성 후 랜덤한 사용자에게 보내기
            count = 0
            while self.recv_stack_tx[i]:
                count = count + 1
                #print(str(count) + ' ' + str(self.node_num))
                top_of_stack = self.recv_stack_tx[i].pop() # 자신이 받은 트랜잭션이라면 output이 자신의 vk
                tx_out = top_of_stack.vout  # vout이 tx를 보낼 대상?

            if tx_out.vk != "":
                #if tx_out.vk.verify(top_of_stack.vin.sig, """여기에 메세지"""):   # 트랜잭션 전파 전 직접 검증해 보기
                tx_to_redeem = top_of_stack.tx_id  # redeem 대상
                print('.')
        print("out of loop")








    def put_queue(self, tx, queue):
        queue.put(tx)

#print()
