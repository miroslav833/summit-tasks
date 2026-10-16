"""Redraws image.png from the stored positions (work/figB_pos.pkl, found by work/layout.py: simulated annealing over
positions minimising crossings with penalties for close vertices, edges passing near vertices and near-straight
two-edge paths). Vertices in the pickle are 1-based."""
import pickle, pathlib, sys, networkx as nx
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, "/home/Trustvs/Turing/AQ_Summit/tasks/task06-bandwidth-fourteen/work")
from draw_graph import draw, crossings
EDGES = [(1, 3), (1, 10), (2, 3), (2, 9), (2, 12), (2, 13), (3, 10), (3, 12), (3, 14), (3, 15), (4, 8), (4, 16), (5, 6), (5, 7), (6, 9), (6, 14), (6, 15), (7, 12), (7, 16), (8, 9), (8, 10), (8, 13), (9, 15), (11, 13), (11, 14), (12, 15), (13, 16)]
G = nx.Graph(EDGES); pos = pickle.load(open(HERE / "work" / "figB_pos.pkl", "rb"))
print("crossings:", crossings(G, pos)); draw(G, pos, str(HERE / "image.png"))
