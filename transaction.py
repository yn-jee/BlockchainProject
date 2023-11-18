import random as rd
import uuid
from datetime import datetime, timedelta


class vehicle:
    def __init__(self):
        self.Vid = uuid.uuid4()
        self.modelName = self.generate_model()
        self.manufacturedTime = self.generate_manufactured_time()

    # modelName을 랜덤하게 선택
    def generate_model(self):
        car_models = [
            "Hyundai Sonata", "Hyundai Elantra", "Hyundai Santa Fe",
            "Hyundai Tucson", "Hyundai Palisade",

            "Genesis G70", "Genesis G80", "Genesis G90",
            "Genesis GV70", "Genesis GV80",

            "Tesla Model S", "Tesla Model X", "Tesla Model 3",
            "Tesla Roadster", "Tesla Cybertruck",

            "BMW 3 Series", "BMW 5 Series", "BMW X5",
            "BMW X1", "BMW X6",

            "Mercedes-Benz E-Class", "Mercedes-Benz S-Class",
            "Mercedes-Benz GLE", "Mercedes-Benz GLC", "Mercedes-Benz GLS"
        ]

        return rd.choice(car_models)

    # manufacturedTime을 랜덤하게 생성
    def generate_manufactured_time(self):
        # 2016-01-01 이상, 2022-12-31 이하인 임의의 날짜 선택하기
        start_date = datetime(2016, 1, 1)
        end_date = datetime(2022, 12, 31)

        # 전체 날짜 범위 계산
        delta = end_date - start_date

        # 랜덤한 일 수 생성
        random_days = rd.randint(0, delta.days)

        # 시작 날짜에 랜덤한 일 수 더하기
        random_date = start_date + timedelta(days=random_days)
        return random_date

    def get_vehicle_data(self):
        return self.Vid, self.modelName, self.manufacturedTime




class transaction(vehicle):
    # 자식 클래스에서의 super().__init__() 실행 시 오류 방지를 위한 default 값들
    def __init__(self, Vid = -1, modelName = -1, manufacturedTime = datetime(1970, 1, 1)):
        super().__init__()
        self.Vid = Vid
        self.modelName = modelName
        self.manufacturedTime = manufacturedTime
        #self.trID
        self.tradeCnt = 1   # 시작 값은 1
        self.tradingTime = datetime(1970, 1, 1)
        self.tradingTime = self.generate_trading_time()
        self.price = 0
        self.generate_price()
        self.others = {}
        self.others = self.generate_others()

    # 거래 날짜를 랜덤하게 생성
    def generate_trading_time(self):
        # 기존의 값이 1970-01-01인 경우(객체를 처음 생성하는 경우, 1차 판매인 경우)
        # 제조 날짜에 180일 이하의 날짜를 랜덤하게 추가
        if self.tradingTime == datetime(1970, 1, 1):
            # 랜덤한 일 수 생성
            random_days = rd.randint(0, 180)

            # 제조 날짜에 랜덤한 일 수 더하기
            random_date = self.manufacturedTime + timedelta(days=random_days)
            return random_date

        # 기존의 값이 1970-01-01인 경우(2차 이상의 판매인 경우)
        # 기존의 tradingTime에 30일 이하의 날짜를 랜덤하게 추가
        else:
            random_days = rd.randint(0, 30)

            # 제조 날짜에 랜덤한 일 수 더하기
            random_date = self.tradingTime + random_days
            return random_date

    # 달러 단위 가격을 랜덤하게 생성
    def generate_price(self):
        # 기존의 값이 0인 경우(객체를 처음 생성하는 경우)
        # 20,000 이상 60,000 이하의 값을 리턴
        if self.price == 0:
            self.price = rd.randint(20, 60) * 1000

        # 기존의 값이 0이 아닌 경우(자동차의 가격이 변동되는 경우)
        # 기존의 가격에 0.8 ~ 1.2 중 랜덤한 값을 곱해 만든 새로운 가격을 리턴
        else:
            self.price = int(rd.randint(80, 120) / 100 * self.price)

    # others를 랜덤하게 생성
    def generate_others(self):
        parts = [
            "front left fender", "front right fender", "rear left fender", "rear right fender",
            "left rocker panel", "right rocker panel",
            "front bumper", "rear bumper",
            "radiator grille",
            "bonnet",
            "front left door", "front right door", "rear left door", "rear right door",
            "front left wheel", "front right wheel", "rear left wheel", "rear right wheel",
            "left head lamp", "right head lamp",
            "left turn signal lamp", "right turn signal lamp"
        ]
        states = ["damaged", "replaced"]

        # 파손 및 교체가 추가되지 않을 확률 0.5
        # 파손 및 교체가 한 번 추가될 확률 0.25
        # 파손 및 교체가 두 번 추가될 확률 0.25
        add_to_others = rd.choices(range(0, 3), weights=[0.5, 0.25, 0.25])[0]

        if add_to_others == 0:
            return self.others

        else:
            i = 0

            while i < add_to_others:
                part = rd.choice(parts)

                if part not in self.others:
                    state = rd.choice(states)
                    self.others[part] = state
                    i = i + 1
            return self.others


"""new_tx = transaction()
print()
new_tx.generate_price()
new_tx.generate_others()
print()"""