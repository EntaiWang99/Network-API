'''
    Grid Network Creator
    @ Entai Wang, Beijing Jiaotong University
    02/2020
'''

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime  

class dot:
    def __init__(self):
        self.id = 0
        self.x = 0
        self.y = 0
        self.degree = 0
        self.type = ''

class node:
    def __init__(self):
        self.node_id = 0
        self.node_x = 0
        self.node_y = 0
        self.fromdot = 0
        self.type = ''

class link:
    def __init__(self):
        self.linkID_id = 0
        self.link_x = 0
        self.link_y = 0
        self.fromdot = 0

class biglink:
    def __init__(self):
        self.link_id = 0
        self.link_origin_node = 0
        self.link_des_node = 0
        self.link_lenth = 0
        self.capacity = 10


g_dot_list = []
g_node_list = []
g_link_list = []
g_biglink_list = []
x0 = 0
y0 = 0

def TransferToNodeLink():

    OriginMatrix = pd.read_csv("input1.1.csv")
    OriginMatrix_1 = np.matrix(OriginMatrix.fillna(0))             

    k = 0
    for i in range(0,OriginMatrix_1.shape[0]):
        for j in range(0,OriginMatrix_1.shape[1]):
            if OriginMatrix_1[i,j] != 0:
                g_dot_list.append(k)
                g_dot_list[k] = dot()
                g_dot_list[k].id = k
                g_dot_list[k].x = i
                g_dot_list[k].y = j
                k = k + 1

    AdjacencyMatrix =  np.zeros((len(g_dot_list),len(g_dot_list)))
    for i in range(0,len(g_dot_list)):
        for j in range(0,len(g_dot_list)):
            if (g_dot_list[i].x + 1 == g_dot_list[j].x)&(g_dot_list[i].y == g_dot_list[j].y):
                AdjacencyMatrix[i,j] = 1
            if (g_dot_list[i].y + 1 == g_dot_list[j].y)&(g_dot_list[i].x == g_dot_list[j].x):
                AdjacencyMatrix[j,i] = 1
            if (g_dot_list[i].x - 1 == g_dot_list[j].x)&(g_dot_list[i].y == g_dot_list[j].y):
                AdjacencyMatrix[i,j] = 1
            if (g_dot_list[i].y - 1 == g_dot_list[j].y)&(g_dot_list[i].x == g_dot_list[j].x):
                AdjacencyMatrix[j,i] = 1                
    # print(AdjacencyMatrix) 

    G = nx.Graph()
    Matrix = AdjacencyMatrix
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i,j] == 1:
                G.add_edge(i, j)
    nx.draw(G)

    k_node = 0
    k_link = 0
    graph_dgree = nx.degree(G)
    for i in range(0,len(g_dot_list)):
        g_dot_list[i].degree = graph_dgree[i]
        if g_dot_list[i].degree == 1:
            g_dot_list[i].type = 'Gate_Node'
            g_node_list.append(k_node)
            g_node_list[k_node] = node()
            g_node_list[k_node].node_id = k_node
            g_node_list[k_node].node_x = g_dot_list[i].x
            g_node_list[k_node].node_y = g_dot_list[i].y
            g_node_list[k_node].fromdot = g_dot_list[i].id
            g_node_list[k_node].type = 'Gate_node'
            k_node = k_node + 1

        if g_dot_list[i].degree == 2:
            g_dot_list[i].type = 'Link'
            g_link_list.append(k_link)
            g_link_list[k_link] = link()
            g_link_list[k_link].linkID_id = k_link
            g_link_list[k_link].link_x = g_dot_list[i].x
            g_link_list[k_link].link_y = g_dot_list[i].y
            g_link_list[k_link].fromdot = g_dot_list[i].id
            k_link = k_link + 1
            

        if g_dot_list[i].degree == 4:
            g_dot_list[i].type = 'Node'
            g_node_list.append(k_node)
            g_node_list[k_node] = node()
            g_node_list[k_node].node_id = k_node
            g_node_list[k_node].node_x = g_dot_list[i].x +x0
            g_node_list[k_node].node_y = g_dot_list[i].y +y0
            g_node_list[k_node].fromdot = g_dot_list[i].id
            g_node_list[k_node].type = 'Common_node'
            k_node = k_node + 1
      
    # plt.show()

    f = open("node.csv","w")
    f.write("node_id,node_x,node_y,node_type\n")
    for i in range(0,len(g_node_list)): 
        f.write(
        str(g_node_list[i].node_id) + "," + 
        str(g_node_list[i].node_x) + "," + 
        str(g_node_list[i].node_y) + "," +
        str(g_node_list[i].type) + "\n"
        )

    pred_node = 0
    to_node = 0
    k_biglink = 0
    for i in range(0,len(g_node_list)):
        lenth = 0
        pred_node = i
        temp_pred = i
        temp_pred_dot = g_node_list[i].fromdot
        g_link_list_temp = len(g_link_list)
        flagflag = 0
        flag = 0
        while(1):
            for j in range(0,g_link_list_temp):
                #for(int i; i<g_link_list_temp; i++)
                temp_to = j
                temp_to_dot = g_link_list[j].fromdot
                
                if (AdjacencyMatrix[temp_pred_dot,temp_to_dot] == 1):
                    temp_pred = j
                    temp_pred_dot = g_link_list[j].fromdot
                    g_link_list.remove(g_link_list[j])
                    g_link_list_temp = g_link_list_temp - 1
                    flag = 0
                    lenth = lenth + 1
                    break
                else:
                    flag = flag + 1
                    if (flag == g_link_list_temp):
                        flag = 0
                        flagflag = 1
                        break   
            if (flagflag == 1):
                break
            
        for k in range(0,len(g_node_list)):
            temp_to = k
            temp_to_dot = g_node_list[k].fromdot
            if (AdjacencyMatrix[temp_pred_dot,temp_to_dot] == 1):
                to_node = k
                break

        if (lenth != 0):
            g_biglink_list.append(k_biglink)
            g_biglink_list[k_biglink] = biglink()
            g_biglink_list[k_biglink].link_id = k_biglink
            g_biglink_list[k_biglink].link_origin_node = pred_node 
            g_biglink_list[k_biglink].link_des_node = to_node
            g_biglink_list[k_biglink].link_lenth = lenth  
            k_biglink = k_biglink + 1
    

    f = open("link.csv","w")
    f.write("link_id,link_origin_node,link_des_node,link_lenth,link_capacity\n")
    for i in range(0,len(g_biglink_list)): 
        f.write(
        str(g_biglink_list[i].link_id) + "," + 
        str(g_biglink_list[i].link_origin_node) + "," + 
        str(g_biglink_list[i].link_des_node) + "," +
        str(g_biglink_list[i].link_lenth) + "," +
        str(g_biglink_list[i].capacity) + "\n"
        )

#void main
start = datetime.datetime.now()
TransferToNodeLink()
end = datetime.datetime.now()
print (end-start)