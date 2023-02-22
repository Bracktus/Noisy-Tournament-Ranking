import sys 
sys.path.append('..')
import distribute_papers as pd
from graph_utils import connected_graph

n = 7
pairs = connected_graph(n, 3)
pd = pd.PaperDistributor(n, pairs)
t = pd.get_solution()

print("graph{")
print("\tnode [colorscheme=set28]")
print("\tedge [colorscheme=set28, len=3]")
for plr in t:
    print(f"\t{plr} [color={plr + 1}]")
for plr in t:
    for p1, p2 in t[plr]:
        print(f'\t{p1}--{p2} [color={plr + 1}]')

print("}")


