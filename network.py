import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt
from ford_fulkerson import ford_fulkerson
from busacker_gowen import min_cost_max_flow

class Network:
    def __init__(self) -> None:
        
        #basic graph
        self.graph = self.__gen_graph()
        self.pos = [(x,y) for x,y in zip(
            [-20, -10, -10, 0, 10, 10, 10, 20], 
            [0, 10, -10, 0, 10, 0, -10, 0])]
        
        #ford-fulkerson
        self.graph_ff = self.graph.copy()
        self.max_flow = ford_fulkerson(self.graph_ff, 0 , 7)
        
        #max flow min cost
        self.graph_bg = self.graph.copy()
        self.flow_bg, self.cost_bg = min_cost_max_flow(self.graph_bg, 0, 7)
    
    def __gen_graph(self):
        G = nx.DiGraph()
        u_edge = [0,0,0,1,1,1,2,2,2,3,3,4,4,5,6,6]
        v_edge = [1,2,3,2,3,4,3,5,6,4,5,5,7,7,5,7]

        for node in range(8):
            G.add_node(node)

        for u, v in zip(u_edge, v_edge):
            capacity = random.randint(1, 7)
            weight = random.randint(1, 4)
            G.add_edge(u, v, capacity=capacity, flow=0, weight=weight)

        return G

    def draw_graph(self, G, draw_weights=False):
        '''
        Function for drawing graph
        '''
        caps: dict = nx.get_edge_attributes(G, 'capacity')
        flows: dict = nx.get_edge_attributes(G, 'flow')
        label: dict = {key: (flow,cap)
                        for cap, flow, key 
                        in zip(caps.values(), flows.values(), caps.keys())}

        plt.figure()
        nx.drawing.draw_networkx(G,
                                with_labels=True, pos=self.pos)
        nx.drawing.draw_networkx_edge_labels(
            G, pos=self.pos, edge_labels=label, label_pos = 0.4
        )
        if not draw_weights:
            weights: dict = nx.get_edge_attributes(G, 'weight')
            nx.drawing.draw_networkx_edge_labels(
                G, pos=self.pos, edge_labels=weights, label_pos = 0.75, font_color="green"
            )
    