from py2neo import Node, Relationship, Graph


def expand(root,graph):
    maxleft=20
    maxright=20
    #if root in DB
    query = graph.find_one("rebase_enzyme",property_key="pattern",property_value=root["pattern"])
    if query:

        root["real_enzyme"]=True
        root["name"]= query["name"]
    root_pattern_left =root["pattern"].split('^')[0]
    root_pattern_right = root["pattern"].split('^')[1]
    if not (root_pattern_left>maxleft and root_pattern_right>maxright):

        for appendage in ['A', 'T', 'G', 'C']:
            temp_node_left = Node("tree_node")
            temp_pattern_left = appendage + root["pattern"]
            temp_node_left["pattern"] = temp_pattern_left
            graph.create(temp_node_left, (root, "containedby", 0))

            temp_node_right = Node("tree_node")
            temp_pattern_right = root["pattern"]+appendage
            temp_node_right["pattern"] = temp_pattern_right
            graph.create(temp_node_right, (root, "containedby", 0))
            expand(temp_node_left,graph)
            expand(temp_node_right,graph)



def run():
    DB_graph = Graph(password="pass")
    PREMU = ["A^T","A^G","A^C","T^G","T^C","G^C","T^A","G^A","C^A","G^T","C^T","C^G"]
    roots = [Node("tree_node") for p in PREMU]
    for i in range(0,len(roots)):
        roots[i]["pattern"] =PREMU[i]
    for r in roots:
        expand(r,DB_graph)

run()