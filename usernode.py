from multiprocessing import Process
import transaction as tx
import random as rd
import ecdsa as ec
class user_node(tx.transaction):
    def __init__(self, node_num = 0):
        super().__init__()
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

new_user = user_node()
print()
