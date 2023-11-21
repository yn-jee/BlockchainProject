import transaction as tx
import ecdsa as ec
from hashlib import sha256

class block(tx.transaction):
    def __init__(self, previous_block = 0, list_of_transactions = []):
        # 헤더에는 blockHeight(myBC 상의
        # 블록 순서로서 genesis block은 blockHeight 0, 다음 블록은 1, 그 다음 블록은 2, ... 를 가짐),
        # prevHash(myBC 상 직전 블록에 대한 hash pointer),
        # nonce(hash puzzle 풀 때, 이를 변경시키며 블록 hash 적용 결과가 target number보다 작거나 같아질 때까지 시도함) 및
        # Merkle-root(트랜잭션들을 leaf로 가지는 Merkle-tree의
        # root에 해당하는 hash 값)으로 구성되며,
        #
        #self.blockHeight = previous_block.blockHeight + 1
        if previous_block:  # genesis block의 previous_block은 0
                            # genesis block이 아니면 hash
            self.prevHash = sha256(previous_block)
        self.list_of_transactions = list_of_transactions
