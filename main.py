from IterationLibrary import ValueIterationMap
import numpy
numpy.random.seed(62)
map_matrix = [
    ["W",    "W",   "W",    "W",    "W",    "W"],
    ["W",    ".",   ".",    ".",     1,     "W"],
    ["W",    ".",   "B",    ".",    ".",    "W"],
    ["W",    ".",   ".",    ".",    ".",    "W"],
    ["W",    ".",    1,     -10,     10,    "W"],
    ["W",    "W",   "W",    "W",    "W",    "W"]
]

# np.argmax listteki max ın index ini veriyor
#   d: discount factor
#   e (epsilon): exploration probability
#   a (alpha): learning rate
#   N: number of experiments for Q-learning

map = ValueIterationMap(map_matrix, r=0, d=1, p=1, N =8)
map.getUtilityCalculatedMap()
#map.printUtilityMap()
#map.printArrowMap()