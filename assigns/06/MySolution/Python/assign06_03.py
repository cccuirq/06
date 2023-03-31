####################################################
#!/usr/bin/env python3
####################################################
import sys
sys.path.append('./../../../../mypylib')
from mypylib_cls import *
import queue
####################################################
"""
HX-2023-03-24: 20 points
Solving the N-queen puzzle
"""
####################################################
"""
fom test
"""
def nqueen(bd):
    """size of bd"""
    res = 0
    for j0 in bd:
        if j0 <= 0:
            break
        else:
            res = res + 1
    return res
def board_safety_all(bd):
    return \
        int1_forall\
        (nqueen(bd), \
         lambda i0: board_safety_one(bd, i0))
def board_safety_one(bd, i0):
    def helper(j0):
        pi = bd[i0]
        pj = bd[j0]
        return pi != pj and abs(i0-j0) != abs(pi-pj)
    return int1_forall(i0, helper)
####################################################
def place_checker(bd,i0,j0):
    def helper(k0):
        pk = bd[k0]
        return pk != j0 and abs(i0-k0) != abs(j0-pk)
    return int1_forall(i0, helper)

def sets(bd,i0,j0):
    lst = list(bd)
    lst[i0] = j0
    return tuple(lst)

def ychildren (node, size, q):
    queen = nqueen(node)
    def helps(i):
        if place_checker(node, queen, i):
            temp = sets(node, queen, i)
            q.put(temp)
    int1_foreach(size + 1, lambda x: () if x == 0 else helps(x))
    return None
####################################################
def gtree_dfs(nxs, fchildren,N):
    def helps(nodes):
        if nxs.empty():
            return strcon_nil()
        else:
            nx1 = nxs.get()
            fchildren(nx1,N,nodes)
            return strcon_cons(nx1,lambda: helps(nxs))
    return lambda: helps(nxs)
####################################################
def solve_N_queen_puzzle(N):
    """
    Please revisit assign04-04.sml.
    A board of size N is a tuple of length N.
    ######
    For instance, a tuple (0, 0, 0, 0) stands
    for a board of size 4 (that is, a 4x4 board)
    where there are no queen pieces on the board.
    ######
    For instance, a tuple (2, 1, 0, 0) stands
    for a board of size 4 (that is, a 4x4 board)
    where there are two queen pieces; the queen piece
    on the 1st row is on the 2nd column; the queen piece
    on the 2nd row is on the 1st column; the last two rows
    contain no queen pieces.
    ######
    This function [solve_N_queen_puzzle] should return
    a stream of ALL the boards of size N that contain N
    queen pieces (one on each row and on each column) such
    that no queen piece on the board can catch any other ones
    on the same board.
    """
    q1 = queue.LifoQueue()
    q1.put((0,)*N)
    return stream_make_filter(gtree_dfs(q1,ychildren,N), lambda bd: nqueen(bd) == N)
####################################################
