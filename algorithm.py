import numpy as np
from tkinter import *

class Node:
    
    def __init__(self, name):
        self.name        = name
        self.connections = {}
        self.tent        = False
        self.x = None
        self.y = None
        
    
    def __repr__(self):
        return(self.name)

    def draw(self, can, x, y):
        self.x, self.y = x, y
        self.avi  = can.create_oval(x-10, y-10, x+10, y+10, fill="red", outline="red")
        self.text = can.create_text(x + 15 , y + 15, text=self.name, fill = "red")
        return (self.avi, self.text)

    def delete(self, can):
        can.delete(self.avi)
        can.delete(self.text)


            
class Graph:
    
    def __init__(self, name, nodes):
        self.name  = name
        self.nodes = nodes
        
    def __repr__(self):

        names = []
        for node in self.nodes:
            names.append(node.name)

        return("Graph, {}, contains nodes: {}".format(self.name, names))
            
    def add_node(self, node):
        self.nodes.append(node)
    
    def delete_node(self, node):
        self.nodes.remove(node)

    def form_connection(self, node1, node2, weight):
        node1.connections[node2] = [weight, False]  
        node2.connections[node1] = [weight, False]
    
    def delete_connection(self, node1, node2):
        if node1 in node2.connections:
            node1.connections.pop(node2)
            node2.connections.pop(node1)
        else:
            pass
        
    def purge_node_connections(self, node):
        for connection in node.connections:
            node.connections[connection][1] = False
            connection.connections[node][1] = False
    
    def purge_all_connections(self):
        for node in self.nodes:
            self.purge_node_connections(node)
    
    def purge_all_nodes(self):
        for node in self.nodes:
            node.tent = False
                 
    def multi_split_path(self, path, splits):
        outpaths = []
        for splitnode in splits:
            outpaths.append(path + [splitnode])
        return(outpaths)
    
    def multi_split_path_self(self, paths1, path1, splits1):
        if splits1 == []:
            pass
        else:
            paths1.remove(path1)
            for splitnode in splits1:
                paths1.append(path1 + [splitnode])
            
    def list_paths(self, start, end):
        
        paths = [[start]]
        next_nodes = []
        paths_temp = []

        _cancel = True
        for connection in end.connections:
            if end.connections[connection][1]:
                _cancel = False
        if _cancel == True:
            return (None)
        
        while True: 
            
            paths_temp = paths 
            for path in paths:
                for connection in path[-1].connections:
                    if (path[-1].connections[connection][1]) and (connection.tent == path[-1].tent + path[-1].connections[connection][0]):
                        next_nodes.append(connection)
                        
                self.multi_split_path_self(paths_temp, path, next_nodes)
                next_nodes = []
            
            paths = paths_temp
            n = 0
            for path in paths:
                if path[-1] == end:
                    n += 1
            if n == len(paths):
                return(paths)  
        
    def dijkstras(self, start, end):
        
        assert start in self.nodes
        assert end   in self.nodes
        start.tent = 0 
        nodes_in_use = [start]
        next_niu = []
        number = 0
        
        while number < len(end.connections): 

            if end in nodes_in_use:
                number += 1

            for node in nodes_in_use:
                for partner in node.connections:
                    if ((node.tent + node.connections[partner][0] < partner.tent) or (partner.tent is False)):                         
                        partner.tent = node.tent + node.connections[partner][0]
                        next_niu.append(partner)                        
                    else:
                        next_niu.append(partner) 
                        
            nodes_in_use = next_niu
            next_niu = []
        
        nodes_in_use = [end]
        next_niu = []
        
        while True:
            for node in nodes_in_use:
                for partner in node.connections:
                    if (partner.tent == node.tent - node.connections[partner][0]):
                        next_niu.append(partner)
                        node.connections[partner][1] = True
                        partner.connections[node][1] = True
            nodes_in_use = next_niu
            next_niu = []
            if nodes_in_use == []:
                break
        
        path_length = end.tent
        pathsu = self.list_paths(start, end)

        self.purge_all_connections()
        self.purge_all_nodes()

        if pathsu == None:
            return (None, None)

        pathss = sorted(pathsu, key = lambda path: len(path))

        return (path_length, pathss)
        
    
#test
    ##########################################################################################



    #a = Node("NodeA")
    #b = Node("NodeB")
    #c = Node("NodeC")
    #d = Node("NodeD")
    #e = Node("NodeE")
    #f = Node("NodeF")
    #g = Node("NodeG")
    #h = Node("NodeH")
    #i = Node("NodeI")
    #j = Node("NodeJ")

    #graph1 = Graph("Graph 1", (a, b, c, d, e, f, g, h, i, j))

    #graph1.form_connection(a, b, 100)
    #graph1.form_connection(a, c, 2)
    #graph1.form_connection(f, c, 100)
    #graph1.form_connection(f, g, 100)
    #graph1.form_connection(d, g, 16)
    #graph1.form_connection(h, g, 4)
    #graph1.form_connection(j, g, 100)
    #graph1.form_connection(h, i, 4)
    #graph1.form_connection(j, b, 100)
    #graph1.form_connection(i, b, 4)
    #graph1.form_connection(d, b, 4)
    #graph1.form_connection(e, b, 100)
    #graph1.form_connection(d, e, 1)
    #graph1.form_connection(c, d, 2)
    #graph1.form_connection(c, e, 1)


    #print(graph1.dijkstras(a, g))

