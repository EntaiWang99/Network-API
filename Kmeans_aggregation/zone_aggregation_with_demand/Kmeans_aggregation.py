'''
    Zone aggregation with demand generation
    Author: Entai Wang (https://github.com/EntaiWang99), Beijing Jiaotong University
            Xuesong Zhou (https://github.com/xzhou99), Arizona State University
    Date: 30/10/2020
'''

import networkx as nx
import numpy as np
import pandas as pd
import datetime  
import os
import csv
from numpy import *  
import matplotlib.pyplot as plt 
import KMeans


class microNode:
    def __init__(self):
        self.name = ''
        self.node_id = 0
        self.osm_node_id = ''
        self.original_node_id = 0
        self.node_seq_no = 0
        self.zone_id = None
        self.control_type = ''
        self.x_coord = 0.0
        self.y_coord = 0.0
        self.node_type = ''
        self.geometry = ''
        self.m_outgoing_link_list = []
        self.m_incoming_link_list = []

        self.activity_type = ''
        self.adjacent_link_type_count_dict = {}
        self.is_boundary = False
        self.super_zone = None

        self.prodction = 0
        self.attraction = 0


class microLink:
    def __init__(self):
        self.name = ''
        self.link_id = 0
        self.osm_way_id = ''

        self.from_node_id = 0
        self.to_node_id = 0

        self.dir_flag = ''
        self.length = 0.0   
        self.lanes = 0     
        self.free_speed = 0
        self.capacity = 0

        self.link_type_name = ''
        self.geometry = ''

class macroZone:
    def __init__(self):
        self.zone_id = 0
        self.x_coord = 0
        self.y_coord = 0
        self.production = 0
        self.attraction = 0
        self.micro_node_list = []

class microDemand:
    def __init__(self):
        self.o_node_id = 0
        self.d_node_id = 0
        self.value = 0

class macroDemand:
    def __init__(self):
        self.o_zone_id = 0
        self.d_zone_id = 0
        self.value = 0

g_number_of_micro_nodes = 0
g_number_of_micro_links = 0
g_number_of_zones = 0
g_number_of_macro_demands = 0
g_number_of_micro_demands = 0

g_micro_node_list = []
g_micro_link_list = []
g_micro_demand_list = [] 
g_macro_demand_list = []
g_zone_list = []

g_node_zone_map = {}

cluster_zone = 10

def ReadData():
    print ("step 1: Reading data..." ) 

    file_link = 'link.csv'
    file_node = 'node.csv'
    file_demand = 'demand.csv'

    csv_file_node = open(file_node) 
    csv_reader_node = csv.reader(csv_file_node)
    k = 0
    for one_line in csv_reader_node:
        if (one_line[0]=='name'):
            continue
        g_micro_node_list.append(k)
        g_micro_node_list[k] = microNode()
        g_micro_node_list[k].name = str(one_line[0])
        g_micro_node_list[k].node_id = int(one_line[1])
        g_micro_node_list[k].osm_node_id = str(one_line[2])       
        # g_micro_node_list[k].zone_id = int(one_line[3])
        g_micro_node_list[k].control_type = str(one_line[4])
        g_micro_node_list[k].node_type = str(one_line[5])
        g_micro_node_list[k].activity_type = str(one_line[6])

        if(one_line[7] == 0):
            g_micro_node_list[k].is_boundary = False
        if(one_line[7] == 1):
            g_micro_node_list[k].is_boundary = True
        g_micro_node_list[k].x_coord = float(one_line[8])
        g_micro_node_list[k].y_coord = float(one_line[9])
        g_micro_node_list[k].geometry = str(one_line[10])
        k = k + 1
    g_number_of_micro_nodes = k


    csv_file_link = open(file_link) 
    csv_reader_link = csv.reader(csv_file_link)
    k = 0
    for one_line in csv_reader_link:
        if (one_line[0]=='name'):
            continue
        g_micro_link_list.append(k)
        g_micro_link_list[k] = microLink()
        g_micro_link_list[k].name = str(one_line[0])
        g_micro_link_list[k].link_id = int(one_line[1])
        g_micro_link_list[k].osm_way_id = str(one_line[2])  

        g_micro_link_list[k].from_node_id = int(one_line[3])
        g_micro_link_list[k].to_node_id = int(one_line[4])

        g_micro_link_list[k].dir_flag= str(one_line[5])
        g_micro_link_list[k].length = float(one_line[6])

        g_micro_link_list[k].lanes = int(one_line[7])
        g_micro_link_list[k].free_speed = int(one_line[8])

        k = k + 1
    g_number_of_micro_links = k    


def Cluster(cluster_zone):
    print ("step 2: Building Dataset..." ) 
    dataSet = [] 
    for i in g_micro_node_list:
        temp = []
        temp.append(float(i.x_coord))
        temp.append(float(i.y_coord))
        dataSet.append(temp)

    dataSet = mat(dataSet)

    print ("step 3: Clustering..." ) 
    centroids, clusterAssment = KMeans.kmeans(dataSet, cluster_zone)     
    
    print ("step 4: Showing the result...")
    KMeans.showCluster(dataSet, cluster_zone, centroids, clusterAssment)
    return centroids, clusterAssment, dataSet

def Output(clusterAssment, dataSet):
    print ("step 6: Output the result...")

    with open('node_with_zone.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name','node_id','zone_id','ctrl_type','node_type','activity_type','is_boundary','x_coord','y_coord','geometry','production_value','attraction_value'])
        for p_node in g_micro_node_list:
            is_boundary = 1 if p_node.is_boundary else 0
            line = [p_node.name,p_node.node_id,p_node.zone_id,p_node.control_type, p_node.node_type,p_node.activity_type,
                    is_boundary,p_node.x_coord,p_node.y_coord,p_node.geometry,p_node.production, p_node.attraction]
            writer.writerow(line)
        
    with open('zone.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name','zone_id','zone_x_coord','zone_y_coord', 'zone_production', 'zone_attraction'])
        for zone in g_zone_list:
            line = ['', str(zone.zone_id), str(zone.x_coord), str(zone.y_coord), str(zone.production), str(zone.attraction)]
            writer.writerow(line)
    
    with open('zone_demand.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name','demand_id','from_zone_id','from_zone_id', 'OD_zone_value'])
        cont = 0
        for demand in g_macro_demand_list:
            line = ['', str(cont), str(demand.o_zone_id), str(demand.o_zone_id), str(demand.value)]
            cont += 1
            writer.writerow(line)


def Generate_zone(clusterAssment, dataSet):  
    print ("step 5: Generating demand...")
    for i in range(0,size(g_micro_node_list)):
        index = int(clusterAssment[i, 0]) 
        temp_x = dataSet[i, 0]
        temp_y = dataSet[i, 1]
        g_micro_node_list[i].zone_id = index 
        g_node_zone_map[i] = index

    # Zone generation
    for zone_no in range(0, cluster_zone):
        g_zone_list.append(zone_no)
        g_zone_list[zone_no] = macroZone()
        g_zone_list[zone_no].zone_id = zone_no
        x_temp = 0
        y_temp = 0
        for i in g_node_zone_map:
            if (i == zone_no):
                g_zone_list[zone_no].micro_node_list.append(g_node_zone_map[i])
                x_temp += g_micro_node_list[i].x_coord
                y_temp += g_micro_node_list[i].y_coord
        
        g_zone_list[zone_no].x_coord = 1/len(g_zone_list[zone_no].micro_node_list) * x_temp
        g_zone_list[zone_no].y_coord = 1/len(g_zone_list[zone_no].micro_node_list) * y_temp


    # Demand generation
    G1 = nx.DiGraph()
    for link in g_micro_link_list:
        G1.add_edges_from([(link.from_node_id, link.to_node_id)])
    G2 = nx.DiGraph()
    for link in g_micro_link_list:
        G2.add_edges_from([(link.to_node_id, link.from_node_id)])

    for node in g_micro_node_list:
        node.production = len(nx.bfs_tree(G1,node.node_id))
        node.attraction = len(nx.bfs_tree(G2,node.node_id))
        g_zone_list[node.zone_id].production += node.production 
        g_zone_list[node.zone_id].attraction += node.attraction 
        
'''
    # Micro-Demand
    demand_no = 0
    for node_i in g_micro_node_list:
        for node_j in g_micro_node_list:
            if (node_i != node_j):
                if (nx.has_path(G1,node_i.node_id,node_j.node_id)):
                    g_micro_demand_list.append(demand_no)
                    g_micro_demand_list[demand_no] = microDemand()

                    g_micro_demand_list[demand_no].o_node_id = node_i.node_id
                    g_micro_demand_list[demand_no].d_node_id = node_j.node_id
                    g_micro_demand_list[demand_no].value = 1
                    demand_no = demand_no + 1
                if (nx.has_path(G2,node_j.node_id,node_i.node_id)):
                    g_micro_demand_list.append(demand_no)
                    g_micro_demand_list[demand_no] = microDemand()

                    g_micro_demand_list[demand_no].o_node_id = node_j.node_id
                    g_micro_demand_list[demand_no].d_node_id = node_i.node_id
                    g_micro_demand_list[demand_no].value = 1
                    demand_no = demand_no + 1
                if(demand_no % 1000 == 0):
                    print(demand_no)
    

    demand_no = 0
    for zone_i in g_zone_list:     
        for zone_j in g_zone_list:    
            g_macro_demand_list.append(demand_no)
            g_macro_demand_list[demand_no] = macroDemand()
            g_macro_demand_list[demand_no].o_zone_id = zone_i.zone_id
            g_macro_demand_list[demand_no].d_zone_id = zone_j.zone_id       
            for demand in g_micro_demand_list:            
                if ((g_micro_node_list[demand.o_node_id].zone_id == zone_i.zone_id) & \
                    (g_micro_node_list[demand.d_node_id].zone_id == zone_j.zone_id)):
                    g_macro_demand_list[demand_no].value += demand.value
            demand_no += 1
'''

if __name__ == '__main__':    
    os.chdir('C:/Users/Entai Wang/OneDrive - bjtu.edu.cn/zone aggregation/zone_aggregation_with_demand')
    start = datetime.datetime.now()
    ReadData()
    centroids, clusterAssment, dataSet = Cluster(cluster_zone)
    Generate_zone(clusterAssment, dataSet)

    Output(clusterAssment, dataSet)
    end = datetime.datetime.now()
    print (end - start)