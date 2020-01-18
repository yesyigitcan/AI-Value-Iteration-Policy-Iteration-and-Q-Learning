from VI import value_iteration
from PI import policy_iteration
from QL import qlearning

# Implementation:
#   1) Agent gets zero (0) for value of a block
#   2) For last randomness of Q-Learning agent updates value of straight with value of the new random way
#      If it decides to go up and gets left from randomness between 0.8 and 0.9
#      it updates value of up with the output of formula which takes value of left
# E: empty space    B: block    T: target
map_matrix = [
    [["E",0.0],   ["E",0.0],    ["E",0.0],    ["T",1.0]],
    [["E",0.0],   ["B",0.0],    ["E",0.0],    ["E",0.0]],
    [["E",0.0],   ["E",0.0],    ["E",0.0],    ["E",0.0]],
    [["E",0.0],   ["T",1.0],    ["T",-10.0],  ["T",10.0]]
]

r = -0.01
d = 1
p = 0.8
a = 0.1
e = 0.78
N = 1000000

vi_map_value = value_iteration(map_matrix, r=r, d=d, p=p, showPolicy = 1)

pi_map_policy = policy_iteration(map_matrix, r=r, d=d, p=p, showPolicy = 1)

qlearning(map_matrix, r=r, d=d, a=a, e=e, N=N, start_location=[2, 0], vi_map_value = vi_map_value, pi_map_policy = pi_map_policy, isAlphaByCount=1, showPolicy = 1)

