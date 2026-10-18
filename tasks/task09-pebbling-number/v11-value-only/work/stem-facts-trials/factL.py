import sys
sys.setrecursionlimit(100000)
exec(open("../v10-fourteen/work/sides2.py").read().split("SL=[")[0])
print("far part L={7,9,12,13,14}, target 1:", maxfail(1, [7,9,12,13,14])[0])
print("L plus 8:", maxfail(1, [7,8,9,12,13,14])[0], " L plus 5,8:", maxfail(1, [5,7,8,9,12,13,14])[0])
