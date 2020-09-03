'''
    Multi-level Decomposition in Space Time Network(Railway Timetable) / V0.5
    @Entai Wang, Beijing Jiaotong University
    2020.4 
'''
import networkx as nx
import numpy as np
import pandas as pd
import datetime  
import os
import csv

class level:
    def __init__(self):
        self.id = 0
        self.block_list = []
        self.bridge_list = []

class block:
    def __init__(self):
        self.level = None
        self.id = 0
        self.node_list = []
        self.in_node_list = []
        self.gate_node_list = []
        self.link_list = []
        self.in_to_gate_SPP = []
        self.gate_to_gate_SPP = []
        self.inside_block = []
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0

class node:
    def __init__(self): 
        self.g_id = 0
        self.level = []
        self.block = []
        self.type = ''
        self.x = 0
        self.y = 0

class link:
    def __init__(self): 
        self.level = 0
        self.pred_node = 0
        self.to_node = 0
        self.lenth = 0
        self.capacity = 0
        self.path = []

origin_node_list = []
origin_link_list = []
level_list = []

def network_partition():
    # init
    level_number = 3
    block_number = 4
    scale = 16
    for i in range(0,level_number):
        level_list.append(i)
        level_list[i] = level()
        level_list[i].id = i
        x_temp = 1
        y_temp = 1
        for j in range(0,block_number**i):
            level_list[i].block_list.append(j)
            level_list[i].block_list[j] = block()
            level_list[i].block_list[j].level = i
            level_list[i].block_list[j].id = j
            level_list[i].block_list[j].xmin = int(x_temp)
            level_list[i].block_list[j].xmax = int(x_temp + scale/(2**i) - 1)
            level_list[i].block_list[j].ymin = int(y_temp)
            level_list[i].block_list[j].ymax = int(y_temp + scale/(2**i) - 1)
            if (x_temp + scale/(2**i) - 1 < scale):
                x_temp = x_temp + scale/(2**i)
            else:
                x_temp = 1
                y_temp = y_temp + scale/(2**i)
    for i in range(0,len(level_list) - 1):
        for j in level_list[i].block_list:
            for n in level_list[i + 1].block_list:
                if (n != j):
                    if ((j.xmin <= n.xmin) & (n.xmax <= j.xmax) & \
                        (j.ymin <= n.ymin) & (n.ymax <= j.ymax)):
                        j.inside_block.append(n.id)

    for i in level_list:
        for j in i.block_list:
            k_node = 0
            for k in origin_node_list:
                if ((k.x <= j.xmax) & (k.x >= j.xmin) & (k.y <= j.ymax) & (k.y >= j.ymin)):
                    j.node_list.append(k_node)
                    j.node_list[k_node] = k
                    k.level.append(i.id)
                    k.block.append(j.id)
                    k_node = k_node + 1
    
    for i in level_list:
        # i = level_list[i.id + 1]
        k_in_node = [0]*len(i.block_list)
        k_gate_node = [0]*len(i.block_list)
        k_link = [0]*len(i.block_list) 
        k_bridge = 0

        for j in origin_link_list:
            pred_node_temp = to_node_temp = None
            for s in origin_node_list:#找起点
                if s.g_id == j.pred_node:
                    pred_node_temp = s
            for t in origin_node_list:#找终点
                if t.g_id == j.to_node:
                    to_node_temp = t

            if(pred_node_temp.block[i.id] == to_node_temp.block[i.id]):#起终点在一个block,代表是内部link
                for k in i.block_list:    
                    if (k.id == pred_node_temp.block[i.id]):    
                        # if len(k.in_node_list) == 0:#表中为空，可以直接加进去
                        #     k.in_node_list.append(k_in_node[k.id])
                        #     k.in_node_list[k_in_node[k.id]] = pred_node_temp
                        #     k_in_node[k.id] =k_in_node[k.id] + 1
                        #     k.in_node_list.append(k_in_node[k.id])
                        #     k.in_node_list[k_in_node[k.id]] = to_node_temp
                        #     k_in_node[k.id] =k_in_node[k.id] + 1
                        # else:
                        #     for s in k.in_node_list:#对于link起点, 找现存表中有无一样的，没有的话填进去block.in_node
                        #         flag = 0 #没找到相同的
                        #         if (pred_node_temp == s):
                        #             flag = 1
                        #             break
                        #     if (flag == 0):
                        #         k.in_node_list.append(k_in_node[k.id])
                        #         k.in_node_list[k_in_node[k.id]] = pred_node_temp
                        #         k_in_node[k.id] =k_in_node[k.id] + 1
                        #     for s in k.in_node_list:#对于link终点, 找现存表中有无一样的，没有的话填进block.in_node
                        #         flag = 0 #没找到相同的
                        #         if (to_node_temp == s):
                        #             flag = 1
                        #             break
                        #     if (flag == 0):
                        #         k.in_node_list.append(k_in_node[k.id])
                        #         k.in_node_list[k_in_node[k.id]] = to_node_temp
                        #         k_in_node[k.id] =k_in_node[k.id] + 1
                        k.link_list.append(k_link[k.id])#把link填入block.link
                        k.link_list[k_link[k.id]] = j
                        k_link[k.id] = k_link[k.id] + 1 
            else:       #起终点不在一个block,代表是内部bridge      
                for k in i.block_list:    
                    if (k.id == pred_node_temp.block[i.id]):#起点        
                        if len(k.gate_node_list) == 0:
                            k.gate_node_list.append(k_gate_node[k.id])
                            k.gate_node_list[k_gate_node[k.id]] = pred_node_temp
                            k_gate_node[k.id] = k_gate_node[k.id] + 1
                        else:
                            for s in k.gate_node_list:#对于link起点, 找现存表中有无一样的，没有的话填进去
                                flag = 0
                                if (pred_node_temp == s):
                                    flag = 1
                                    break
                            if (flag == 0):
                                k.gate_node_list.append(k_gate_node[k.id])
                                k.gate_node_list[k_gate_node[k.id]] = pred_node_temp
                                k_gate_node[k.id] = k_gate_node[k.id] + 1
                
                for k in i.block_list:    
                    if (k.id == to_node_temp.block[i.id]):#终点        
                        if len(k.gate_node_list) == 0:
                            k.gate_node_list.append(k_in_node[k.id])
                            k.gate_node_list[k_gate_node[k.id]] = to_node_temp
                            k_gate_node[k.id] = k_gate_node[k.id] + 1
                        else:
                            for s in k.gate_node_list:#对于link终点, 找现存表中有无一样的，没有的话填进去
                                flag = 0
                                if (to_node_temp == s):
                                    flag = 1
                                    break
                            if (flag == 0):
                                k.gate_node_list.append(k_gate_node[k.id])
                                k.gate_node_list[k_gate_node[k.id]] = to_node_temp
                                k_gate_node[k.id] = k_gate_node[k.id] + 1
                
                i.bridge_list.append(k_bridge)
                i.bridge_list[k_bridge] = j
                k_bridge = k_bridge + 1

    for i in level_list:
        for j in i.block_list:
            for k in j.node_list:
                flag = 1
                for t in j.gate_node_list:
                    if (k == t):
                        flag = 0
                        break
                if (flag == 1):    
                    j.in_node_list.append(k)

def Stage_1_bottom_level():
    i = len(level_list) - 1 #最底层
    for j in level_list[i].block_list:
        link_temp = j.link_list
        in_node_temp = j.in_node_list
        gate_node_temp = j.gate_node_list

        G = nx.Graph()
        for k in link_temp:
            G.add_weighted_edges_from([(k.pred_node,k.to_node,k.lenth)])
        
        k_in_path = 0
        k_g_path = 0
        # Find the shortest path in one block: from in_node to gate_node
        for m in in_node_temp:
            for n in gate_node_temp:
                    try: 
                        distance = nx.dijkstra_path_length(G, source = m.g_id, target = n.g_id)
                        path = nx.dijkstra_path(G, source = m.g_id, target = n.g_id)
                        SPP_temp = link()
                        SPP_temp.pred_node = m.g_id
                        SPP_temp.to_node = n.g_id
                        SPP_temp.path = path
                        SPP_temp.lenth = distance
                        level_list[i].block_list[j.id].in_to_gate_SPP.append(k_in_path)
                        level_list[i].block_list[j.id].in_to_gate_SPP[k_in_path] = SPP_temp
                        k_in_path = k_in_path + 1
                    except:
                        print("can not find the feasible path between", (m.g_id), "and", (n.g_id))
        
        # Find the gate_node to gate_node SPP (Passing through the block
        for m in gate_node_temp:
            for n in gate_node_temp:
                if m != n:
                    try: 
                        distance = nx.dijkstra_path_length(G, source = m.g_id, target = n.g_id)
                        path = nx.dijkstra_path(G, source = m.g_id, target = n.g_id)
                        SPP_temp = link()
                        SPP_temp.pred_node= m.g_id
                        SPP_temp.to_node = n.g_id
                        SPP_temp.path = path
                        SPP_temp.lenth = distance
                        level_list[i].block_list[j.id].gate_to_gate_SPP.append(k_g_path)
                        level_list[i].block_list[j.id].gate_to_gate_SPP[k_g_path] = SPP_temp
                        k_g_path = k_g_path + 1
                    except:
                        print("can not find the feasible path between", (m.g_id), "and", (n.g_id))  

def Stage_2_middle_level():
    for i in range((len(level_list) - 2), -1, -1):
        for j in level_list[i].block_list:
            link_temp = []
            in_node_temp = []
            gate_node_temp = []
            for k in level_list[i + 1].bridge_list:
                for m in j.node_list:
                    for n in j.node_list:
                        if (k.pred_node == m.g_id) & (k.to_node == n.g_id):
                            link_temp.append(k)
                            break
            # level_list[i].bridge_list = link_temp
            for k in j.inside_block:
                for t in level_list[i + 1].block_list[k].gate_to_gate_SPP:
                    link_temp.append(t)
                in_node_temp = in_node_temp + level_list[i + 1].block_list[k].gate_node_list
            gate_node_temp = j.gate_node_list
            for n in gate_node_temp:
                for m in in_node_temp:
                    if (m.g_id == n.g_id):
                        in_node_temp.remove(m)
            j.link_list = link_temp
            j.in_node_list = in_node_temp

            G2 = nx.Graph()
            for k in link_temp:
                G2.add_weighted_edges_from([(k.pred_node,k.to_node,k.lenth)])

            k_in_path = 0
            k_g_path = 0
            # Find the shortest path in one block: from in_node to gate_node
            for m in in_node_temp:
                for n in gate_node_temp:
                        try: 
                            distance = nx.dijkstra_path_length(G2, source = m.g_id, target = n.g_id)
                            path = nx.dijkstra_path(G2, source = m.g_id, target = n.g_id)
                            SPP_temp = link()
                            SPP_temp.pred_node = m.g_id
                            SPP_temp.to_node = n.g_id
                            # SPP_temp.path = path
                            path_temp = []
                            for s in range(0,len(path) - 1):
                                for t in link_temp:
                                    if (path[s] == t.pred_node) & (path[s + 1] == t.to_node):
                                        for r in t.path:
                                            path_temp.append(r)
                            SPP_temp.path = path_temp
                            SPP_temp.lenth = distance
                            level_list[i].block_list[j.id].in_to_gate_SPP.append(k_in_path)
                            level_list[i].block_list[j.id].in_to_gate_SPP[k_in_path] = SPP_temp
                            k_in_path = k_in_path + 1
                        except:
                            print("can not find the feasible path between", (m.g_id), "and", (n.g_id))

                    
            # Find the gate_node to gate_node SPP (Passing through the block
            for m in gate_node_temp:
                for n in gate_node_temp:
                    if m != n:
                        try: 
                            distance = nx.dijkstra_path_length(G2, source = m.g_id, target = n.g_id)
                            path = nx.dijkstra_path(G2, source = m.g_id, target = n.g_id)
                            SPP_temp = link()
                            SPP_temp.pred_node= m.g_id
                            SPP_temp.to_node = n.g_id
                            # SPP_temp.path = path
                            path_temp = []
                            for s in range(0,len(path) - 1):
                                for t in link_temp:
                                    if (path[s] == t.pred_node) & (path[s + 1] == t.to_node):
                                        for r in t.path:
                                            path_temp.append(r)
                            SPP_temp.path = path_temp
                            SPP_temp.lenth = distance
                            level_list[i].block_list[j.id].gate_to_gate_SPP.append(k_g_path)
                            level_list[i].block_list[j.id].gate_to_gate_SPP[k_g_path] = SPP_temp
                            k_g_path = k_g_path + 1
                        except:
                            print("can not find the feasible path between", (m.g_id), "and", (n.g_id)) 

def Stage_2_top_level():
    link_temp = level_list[0].block_list[0].link_list
    node_temp = []
    for i in level_list[1].block_list:
        for j in i.gate_node_list:
            node_temp.append(j)
    level_list[0].block_list[0].node_list = node_temp
    G3 = nx.Graph()
    for k in link_temp:
        G3.add_weighted_edges_from([(k.pred_node,k.to_node,k.lenth)])
    k_g_path = 0
    for m in node_temp:
        for n in node_temp:
            if m != n:
                try: 
                    distance = nx.dijkstra_path_length(G3, source = m.g_id, target = n.g_id)
                    path = nx.dijkstra_path(G3, source = m.g_id, target = n.g_id)
                    SPP_temp = link()
                    SPP_temp.pred_node= m.g_id
                    SPP_temp.to_node = n.g_id
                    # SPP_temp.path = path
                    path_temp = []
                    for s in range(0,len(path) - 1):
                        for t in link_temp:
                            if (path[s] == t.pred_node) & (path[s + 1] == t.to_node):
                                for r in t.path:
                                    path_temp.append(r)
                    SPP_temp.path = path_temp
                    SPP_temp.lenth = distance
                    level_list[0].block_list[0].in_to_gate_SPP.append(k_g_path)
                    level_list[0].block_list[0].in_to_gate_SPP[k_g_path] = SPP_temp
                    k_g_path = k_g_path + 1
                except:
                    print("can not find the feasible path between", (m.g_id), "and", (n.g_id)) 

def Stage_3(origin_g_id, des_g_id):
    final_path = link()
    final_path.pred_node = origin_g_id
    final_path.to_node = des_g_id
    for i in level_list[len(level_list) - 1].block_list:
        for j in i.node_list:
            if (origin_g_id == j.g_id):
                origin = j
            if (des_g_id == j.g_id):
                des = j  
    # 构建空树
    left_path_tree = []
    right_path_tree = []
    for i in range(0,len(level_list)):
        temp_array_1 = []
        temp_array_2 = []
        left_path_tree.append(temp_array_1)
        right_path_tree.append(temp_array_2)
    # path_tree_left = path_tree
    # path_tree_right = path_tree

    # 树顶
    for i in level_list[0].block_list[0].in_to_gate_SPP:
        for j in level_list[0].block_list[0].in_node_list:
            for k in level_list[0].block_list[0].in_node_list:
                if (i.pred_node == j.g_id) & (i.to_node == k.g_id) & \
                   (j.block[1] == origin.block[1]) & (k.block[1] == des.block[1]):
                   path_temp = i
                   path_temp.current_path = path_temp.path
                   path_temp.current_lenth = path_temp.lenth
                   left_path_tree[0].append(path_temp)
                   right_path_tree[0].append(path_temp)
                   print('Hi!')
    
    # 左孩子（起点方向）
    for i in range(0,len(left_path_tree)-2):
        for j in left_path_tree[i]:
            for k in level_list[i+1].block_list[origin.block[i+1]].in_to_gate_SPP:
                for t in level_list[i+1].block_list[origin.block[i+1]].in_node_list:
                    if (k.pred_node == t.g_id) & (t.block[i+2] == origin.block[i+2]) & \
                       (k.to_node == j.pred_node):
                        path_temp = k
                        path_temp.current_path = path_temp.path + j.current_path
                        path_temp.current_lenth = path_temp.lenth + j.current_lenth
                        left_path_tree[i+1].append(path_temp)

    # 左树根
    for i in left_path_tree[-2]:
        for j in level_list[-1].block_list[origin.block[-1]].in_to_gate_SPP:
            if (i.pred_node == j.to_node) & (j.pred_node == origin.g_id):
                path_temp = j
                path_temp.current_path = path_temp.path[::-1] + i.current_path
                path_temp.current_lenth = path_temp.lenth + i.current_lenth
                left_path_tree[-1].append(path_temp)

    # 右孩子（终点方向）
    for i in range(0,len(right_path_tree)-2):
        for j in right_path_tree[i]:
            for k in level_list[i+1].block_list[des.block[i+1]].in_to_gate_SPP:
                for t in level_list[i+1].block_list[des.block[i+1]].in_node_list:
                    if (k.pred_node == t.g_id) & (t.block[i+2] == des.block[i+2]) & \
                       (k.to_node == j.to_node):
                        path_temp = k
                        path_temp.current_path = j.current_path + path_temp.path[::-1]
                        path_temp.current_lenth = path_temp.lenth + j.current_lenth
                        right_path_tree[i+1].append(path_temp)
    # 右树根
    for i in right_path_tree[-2]:
        for j in level_list[-1].block_list[des.block[-1]].in_to_gate_SPP:
            if (i.pred_node == j.to_node) & (j.pred_node == des.g_id):
                path_temp = j
                path_temp.current_path = i.current_path + path_temp.path[::-1]
                path_temp.current_lenth = path_temp.lenth + i.current_lenth
                right_path_tree[-1].append(path_temp)
    return [left_path_tree, right_path_tree]


start = datetime.datetime.now()

file_link = 'C:/Users/Entai Wang/Desktop/Readnetwork王恩泰/n-level-SPP-path-tree/input_link.csv'
file_node = 'C:/Users/Entai Wang/Desktop/Readnetwork王恩泰/n-level-SPP-path-tree/input_node.csv' 
csv_file_node = open(file_node) 
csv_reader_node = csv.reader(csv_file_node)
k = 0  
for one_line in csv_reader_node:
    if (one_line[0]=='id'):
        continue
    origin_node_list.append(k)
    origin_node_list[k] = node()
    origin_node_list[k].g_id = int(one_line[0])
    origin_node_list[k].x = int(one_line[1])
    origin_node_list[k].y = int(one_line[2])
    k = k + 1
k = 0
csv_file_link = open(file_link) 
csv_reader_lines = csv.reader(csv_file_link)  
for one_line in csv_reader_lines:
    if (one_line[0]=='id'):
        continue
    origin_link_list.append(k)
    origin_link_list[k] = link()
    origin_link_list[k].pred_node = int(one_line[1])
    origin_link_list[k].to_node = int(one_line[2])
    origin_link_list[k].lenth = int(one_line[3])
    origin_link_list[k].capacity = int(one_line[4])
    k = k + 1

origin_g_id = 1
des_g_id = 256   
network_partition()
Stage_1_bottom_level()
Stage_2_middle_level()
Stage_2_top_level()
final_tree = Stage_3(origin_g_id, des_g_id)
# print(final_path.path)

end = datetime.datetime.now()
print (end - start)
print('Hi!')