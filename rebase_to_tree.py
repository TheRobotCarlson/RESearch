from py2neo import Node, Relationship, Graph
import sys

def expand(root,graph):
    maxleft=5
    maxright=5
    #if root in DB
    query = graph.find_one("rebase_enzyme",property_key="pattern",property_value=root["pattern"])
    if query:

        root["real_enzyme"]=True
        root["name"]= query["name"]
    root_pattern_left =root["pattern"].split('^')[0]
    root_pattern_right = root["pattern"].split('^')[1]
    if (len(root_pattern_left)<maxleft and len(root_pattern_right)<maxright):

        for appendage in ['A', 'T', 'G', 'C']:
            temp_node_left = Node("tree_node")
            temp_pattern_left = appendage + root["pattern"]
            temp_node_left["pattern"] = temp_pattern_left
            relationship_left = Relationship(root ,"containedby",temp_node_left)
            #graph.create(temp_node_left, relationship_left)
            graph.create(temp_node_left)
            graph.create(relationship_left)
            temp_node_right = Node("tree_node")
            temp_pattern_right = root["pattern"]+appendage
            temp_node_right["pattern"] = temp_pattern_right
            relationship_right = Relationship(root, "containedby", temp_node_right)
            graph.create(temp_node_right)
            graph.create(relationship_right)
            expand(temp_node_left,graph)
            expand(temp_node_right,graph)



def run():
    sys.setrecursionlimit(100000)
    DB_graph = Graph(password="pass")
    PREMU = ["A^T","A^G","A^C","T^G","T^C","G^C","T^A","G^A","C^A","G^T","C^T","C^G"]
    roots = [Node("tree_node") for p in PREMU]
    for i in range(0,len(roots)):
        roots[i]["pattern"] =PREMU[i]
    for r in roots:
        expand(r,DB_graph)

run()