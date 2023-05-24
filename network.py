import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt

class Network:
    def __init__(self) -> None:
        #basic graph
        self.graph = self.__gen_graph()
        self.pos = [(x,y) for x,y in zip(
            [-20, -10, -10, 0, 10, 10, 10, 20], 
            [0, 10, -10, 0, 10, 0, -10, 0])]
        
        #ford-fulkerson
        self.max_flow, self.residual_graph_flow = nx.maximum_flow(self.graph, 0, 7)
        self.min_cost_flow = nx.max_flow_min_cost(self.graph, 0, 7)
        self.min_cost = nx.cost_of_flow(self.graph, self.min_cost_flow)
        self.res_graph = self.__gen_res_graph()
        self.min_cost_graph = self.__gen_min_cost_graph()
    
    def __gen_graph(self):
        G = nx.DiGraph()
        u_edge = [0,0,0,1,1,1,2,2,2,3,3,4,4,5,6,6]
        v_edge = [1,2,3,2,3,4,3,5,6,4,5,5,7,7,5,7]
        nodes = [(i) for i in range(8)]

        G.add_nodes_from(nodes)
        G.add_edges_from([
            (u,v,{'weight': random.randint(1,7), 'capacity': random.randint(1,7), 'flow':0}) 
            for u,v in zip(u_edge, v_edge)
            ])
        return G

    def __gen_res_graph(self):
        G = self.graph.copy()
        flow_attr = {}
        for u_node in self.residual_graph_flow.keys():
            for v_node in self.residual_graph_flow[u_node]:
                flow_attr[(u_node, 
                           v_node)] = self.residual_graph_flow[u_node][v_node]
        nx.set_edge_attributes(G, flow_attr, "flow")
        return G
    
    def __gen_min_cost_graph(self):
        G = self.graph.copy()
        flow_attr = {}
        for u_node in self.min_cost_flow.keys():
            for v_node in self.min_cost_flow[u_node]:
                flow_attr[(u_node, 
                           v_node)] = self.min_cost_flow[u_node][v_node]
        nx.set_edge_attributes(G, flow_attr, "flow")
        return G

    def draw_graph(self, G):
        '''
        Function for drawing graph
        '''
        caps: dict = nx.get_edge_attributes(G, 'capacity')
        flows: dict = nx.get_edge_attributes(G, 'flow')
        weights: dict = nx.get_edge_attributes(G, 'weight')
        label: dict = {key: (flow,cap)
                        for cap, flow, key 
                        in zip(caps.values(), flows.values(), caps.keys())}

        plt.figure()
        nx.drawing.draw_networkx(G,
                                with_labels=True, pos=self.pos)
        nx.drawing.draw_networkx_edge_labels(
            G, pos=self.pos, edge_labels=label, label_pos = 0.4
        )
        nx.drawing.draw_networkx_edge_labels(
            G, pos=self.pos, edge_labels=weights, label_pos = 0.75, font_color="green"
        )
    