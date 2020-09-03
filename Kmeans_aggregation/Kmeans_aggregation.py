import networkx as nx
import numpy as np
import pandas as pd
import datetime  
import os
import csv
from numpy import *  
import matplotlib.pyplot as plt 
import KMeans


class MacroNode:
    def __init__(self):
        self.name = ''
        self.node_id = 0
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


class MacroLink:
    def __init__(self):
        self.name = ''
        self.link_id = ''
        self.original_link_id = ''
        self.link_key = ''
        self.from_node_id = 0
        self.to_node_id = 0
        self.link_type = ''
        self.link_type_code = 0
        self.direction = 1
        self.length = 0.0

        self.number_of_lanes = None
        self.speed_limit = None
        self.capacity = None
        self.geometry = None
        self.from_node = None
        self.to_node = None


class Demand:
    def __init__(self):
        self.o_zone_id = None
        self.d_zone_id = None
        self.value = None
        self.demand_type = ''

g_number_of_macro_nodes = 0
g_number_of_macro_links = 0
g_number_of_zones = 0

g_macro_node_list = []
g_macro_link_list = []
g_demand_list = [] 
g_zone_list = []


cluster_zone = 8

def ReadData():
    print ("step 1: Reading data..." ) 

    file_link = 'road_link.csv'
    file_node = 'node.csv'
    file_demand = 'demand.csv'

    csv_file_node = open(file_node) 
    csv_reader_node = csv.reader(csv_file_node)
    k = 0
    for one_line in csv_reader_node:
        if (one_line[0]=='name'):
            continue
        g_macro_node_list.append(k)
        g_macro_node_list[k] = MacroNode()
        g_macro_node_list[k].name = str(one_line[0])
        g_macro_node_list[k].node_id = int(one_line[1])
        if(one_line[2] != ''):
            g_macro_node_list[k].zone_id = int(one_line[2])
        g_macro_node_list[k].control_type = str(one_line[3])
        g_macro_node_list[k].node_type = str(one_line[4])
        g_macro_node_list[k].activity_type = str(one_line[5])
        if(one_line[6] == 0):
            g_macro_node_list[k].is_boundary = False
        if(one_line[6] == 1):
            g_macro_node_list[k].is_boundary = True
        g_macro_node_list[k].x_coord = float(one_line[7])
        g_macro_node_list[k].y_coord = float(one_line[8])
        g_macro_node_list[k].geometry = str(one_line[9])
        k = k + 1
    g_number_of_macro_nodes = k

    # csv_file_demand = open(file_demand) 
    # csv_reader_demand = csv.reader(csv_file_demand)    
    # k = 0
    # for one_line in csv_reader_demand:
    #     if (one_line[0]=='o'):
    #         continue
    #     g_demand_list.append(k)
    #     g_demand_list[k] = Demand()        
    #     g_demand_list[k].o_zone_id = float(one_line[0])
    #     g_demand_list[k].d_zone_id = float(one_line[1])
    #     g_demand_list[k].value = float(one_line[2])
    #     g_demand_list[k].demand_type = ''
    #     k = k + 1

def Cluster(cluster_zone):
    print ("step 2: Building Dataset..." ) 
    dataSet = [] 
    for i in g_macro_node_list:
        temp = []
        temp.append(float(i.x_coord))
        temp.append(float(i.y_coord))
        dataSet.append(temp)

    dataSet = mat(dataSet)

    print ("step 3: Clustering..." ) 
    centroids, clusterAssment = KMeans.kmeans(dataSet, cluster_zone)     
    
    print ("step 3: show the result...")
    KMeans.showCluster(dataSet, cluster_zone, centroids, clusterAssment)
    return centroids, clusterAssment, dataSet

def Output(clusterAssment, dataSet):
    print ("step 4: Output the result...")
    for i in range(0,size(g_macro_node_list)):
        index = int(clusterAssment[i, 0]) 
        temp_x = dataSet[i, 0]
        temp_y = dataSet[i, 1]
        g_macro_node_list[i].super_zone = index 

    with open('node_with_super_zone.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name','node_id','zone_id','ctrl_type','node_type','activity_type','is_boundary','x_coord','y_coord','geometry','super_zone_id'])
        for p_node in g_macro_node_list:
            is_boundary = 1 if p_node.is_boundary else 0
            line = [p_node.name,p_node.node_id,p_node.zone_id,p_node.control_type, p_node.node_type,p_node.activity_type,
                    is_boundary,p_node.x_coord,p_node.y_coord,p_node.geometry,p_node.super_zone]
            writer.writerow(line)


if __name__ == '__main__':    
    start = datetime.datetime.now()
    ReadData()
    centroids, clusterAssment, dataSet = Cluster(cluster_zone)
    Output(clusterAssment, dataSet)

    end = datetime.datetime.now()
    print (end - start)