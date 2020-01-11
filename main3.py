from VI import value_iteration
from PI import policy_iteration
from QL import qlearning

# E: empty space    B: block    T: target
map_matrix = [
    [["E",0.0],   ["E",0.0],    ["E",0.0],    ["T",1.0]],
    [["E",0.0],   ["B",0.0],    ["E",0.0],    ["E",0.0]],
    [["E",0.0],   ["E",0.0],    ["E",0.0],    ["E",0.0]],
    [["E",0.0],   ["T",1.0],    ["T",-10.0],  ["T",10.0]]
]

r = -0.01
d = 1
p = 0.5
a = 0.1
e = 0
N = 100000

value_iteration(map_matrix, r=r, d=d, p=p)

policy_iteration(map_matrix, r=r, d=d, p=p)

#qlearning(map_matrix, r=r, d=d, a=a, e=e, N=N, start_location=[2, 0])

