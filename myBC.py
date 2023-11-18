import fullnode as fn
import usernode as un
import random as rd
import multiprocessing

class myBC(fn.full_node, un.user_node):
    def initialize(self, full_num, user_num, full_links_num):    # number of full/user nodes, number of full-full links

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

