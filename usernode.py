from multiprocessing import Process
import transaction as tx
import random as rd
import ecdsa as ec
class user_node(tx.transaction):
    def __init__(self, node_num, queue_user):
        super().__init__()
        self.send_queue = queue_user

        #----비대칭키 생성----
        # sk: signing key(private key)
        # vk: verifying key(public key)
        self.sk = ec.SigningKey.generate()
        self.vk = self.sk.verifying_key

        #----무작위 개수만큼 자동차 생성----
        # 자동차 개수 설정
        self.cars_num = rd.randint(3, 11)
        # 자동차 개수만큼 자동차 생성 및 저장
        self.cars = []
        self.txs = []
        for i in range(self.cars_num):
            car = tx.vehicle()
            Vid, modelName, manufacturedTime = car.get_vehicle_data()
            new_tx = tx.transaction(Vid, modelName, manufacturedTime)
            self.cars.append(car)
            self.txs.append(new_tx)
            # 새로 생성한 트랜잭션 모두를 자신과 연결된 full node에 put
            queue_user.put(new_tx)


#print()
