import multiprocessing

import fullnode as fn
import usernode as un
from myBC import myBC

newbc = myBC
full_num = 7
user_num = 4
full_links_num = 10

newbc.initialize(newbc,7, 4, 10)

# ----노드 생성----

# 이 모듈이 직접 실행될 때에만 다음 코드를 실행
if __name__ == "__main__":
    print("hi")

    # 노드 잇기 - 두 노드 간 공유하는 스택 및 큐로써.
    m = multiprocessing.Manager()

    # stack_matrix_block[i][j] :
    # "A stack" shared between full_node_i, full_node_j
    # contains messages from full_node_j to full_node_i propagating mined blocks
    # so that full_node_i can search all stack_matrix_block[i][*] before every hash operation
    stack_matrix_block = [[m.list() for _ in range(full_num)] for _ in range(full_num)]
    for i in range(full_num):
        for j in range(full_num):
            if newbc.matrix_full[i][j] != 1:
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
            if newbc.matrix_full[i][j] != 1:
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

    # full node 생성
    # 자신의 노드 번호 i, stack_matrix_block, stack_matrix_tx, queue_user[i]를 인자로 받음
    for i in range(full_num):
        if i < user_num:
            list_full.append(fn.full_node(i, stack_matrix_block, stack_matrix_tx, queue_user[i]))
        else:
            # __init__ 형식을 맞추기 위해 m.Queue()를 전달
            list_full.append(fn.full_node(i, stack_matrix_block, stack_matrix_tx, m.Queue()))

    for i in range(user_num):
        list_user.append(un.user_node(i, queue_user[i]))

print("set")