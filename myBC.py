import block as bl
import fullnode as fn
import usernode as un
import random as rd
import ecdsa as ec
from hashlib import sha256
import multiprocessing as mp

class myBC(fn.full_node, un.user_node):
    def __init__(self, full_num, user_num, full_links_num, genesis):    # number of full/user nodes, number of full-full links

        #----random topology 구성하기----

        shuffled_index = [i for i in range(full_num)]
        rd.shuffle(shuffled_index)

        # full-full link를 저장한 행렬
        self.matrix_full = [[0 for _ in range(full_num)] for _ in range(full_num)]
        # user-full link는 list_user[i]와 list_full[i]의 연결로 한다. 즉, 추가적으로 저장할 필요 없음.

        # matrix_full 초기화하기
        for i in range(full_num - 1):
            # 주대각선 초기화
            self.matrix_full[i][i] = 1
            # 섞어 만든 리스트에서, 앞뒤로 이어진 노드들 연결하기(행렬에서 1로 표시)
            self.matrix_full[shuffled_index[i]][shuffled_index[i + 1]] = 1
            # 대칭행렬로 만들기
            self.matrix_full[shuffled_index[i + 1]][shuffled_index[i]] = 1
        # 주대각선 초기화 - 마지막 노드.
        self.matrix_full[full_num - 1][full_num - 1] = 1
        # 0번째 원소와 full_num번째 원소 잇기
        self.matrix_full[shuffled_index[0]][shuffled_index[full_num - 1]] = 1
        self.matrix_full[shuffled_index[full_num - 1]][shuffled_index[0]] = 1

        # 추가 링크 연결, 이미 연결되어 있던 링크라면 다시 고르기.
        i = 0
        extra_link = full_links_num - full_num
        while i < extra_link:
            temp_link = rd.sample(shuffled_index, 2)
            if self.matrix_full[temp_link[0]][temp_link[1]] == 0:
                i = i + 1
                self.matrix_full[temp_link[0]][temp_link[1]] = 1
                self.matrix_full[temp_link[1]][temp_link[0]] = 1



        # ----노드 생성----

        # 이 모듈이 직접 실행될 때에만 다음 코드를 실행
        if __name__ == "__main__":
            print("hi")

            # 노드 잇기 - 두 노드 간 공유하는 스택 및 큐로써.
            m = mp.Manager()

            # stack_matrix_block[i][j] :
            # "A stack" shared between full_node_i, full_node_j
            # contains messages from full_node_j to full_node_i propagating mined blocks
            # so that full_node_i can search all stack_matrix_block[i][*] before every hash operation
            stack_matrix_block = [[m.list() for _ in range(full_num)] for _ in range(full_num)]
            for i in range(full_num):
                for j in range(full_num):
                    if self.matrix_full[i][j] != 1:
                        # matrix_full에서 해당하는 위치가 1이 아니라면 stack 삭제
                        stack_matrix_block[i][j] = None
                    """else:
                        stack_matrix_block[i][j].append("hi")"""

            # stack_matrix_tx[i][j] :
            # "A stack" shared between full_node_i, full_node_j
            # contains messages from full_node_j to full_node_i propagating valid transactions
            # so that full_node_i can search all stack_matrix_tx[i][*] before every block building
            stack_matrix_tx = [[m.list() for _ in range(full_num)] for _ in range(full_num)]
            for i in range(full_num):
                for j in range(full_num):
                    if self.matrix_full[i][j] != 1:
                        # matrix_full에서 해당하는 위치가 1이 아니라면 stack 삭제
                        stack_matrix_tx[i][j] = None
                    """else:
                        stack_matrix_tx[i][j].append("hi")"""

            # queue_user[i] :
            # "A queue" shared between user_node_i, full_node_i
            # This queue is used when user_node_i generates a transaction and sends it to full_node_i
            queue_user = [m.Queue() for _ in range(user_num)]

            list_full = []
            list_user = []

            # 트랜잭션 상의 거래 기록을 각 노드가 알아야 함
            # myBC 상의 거래와는 별개로, 각 사용자 노드가 자신이 소유한 자동차를 추적하고 있기 위해서 stack_matrix_user 노드가 필요함
            # 각 사용자는 자동차를 판매한 뒤, 그 자동차의 구매자의 stack에 해당 트랜잭션의 정보를 공유함

            stack_matrix_user = [[m.list() for _ in range(user_num)] for _ in range(user_num)]

            #----full node 생성----
            # 자신의 노드 번호 i, stack_matrix_block, stack_matrix_tx, queue_user[i]를 인자로 받음
            for i in range(full_num):
                if i < user_num:
                    temp_full = fn.full_node(i, stack_matrix_block, stack_matrix_tx, queue_user[i])
                    list_full.append(temp_full)
                else:
                    # __init__ 형식을 맞추기 위해 m.Queue()를 전달
                    temp_full = fn.full_node(i, stack_matrix_block, stack_matrix_tx, m.Queue())
                    list_full.append(temp_full)
                list_full[i] = mp.Process(target=list_full[i].run_full, args=(genesis, ))
                list_full[i].start()

            for i in range(full_num):
                list_full[i].join()

            #----user node 생성----

            # 다른 user node의 vk 정보도 전달받음 ---- 일차원 배열 other_users로.
            # 프로세스 간에 키를 전달하기 위해 string 형태로 변환한 뒤 전달
            # 각 객체 생성 시 string 형태를 다시 키로 변환하여 사용

            other_users = ["" for _ in range(user_num)]

            for i in range(user_num):

                temp_user = un.user_node(i, queue_user[i], stack_matrix_user, other_users)
                list_user.append(temp_user)

                list_user[i] = mp.Process(target=list_user[i].run_user, args=("", ""))
                list_user[i].start()

            for i in range(user_num):
                list_user[i].join()

            print("end")




genesis = bl.block([])

newbc = myBC(7, 4, 10, genesis)
