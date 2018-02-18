
from py2neo import Graph, NodeSelector,Node, Relationship,NodeSelection
enzymes = []

pairs = ['A^A', 'A^C', 'A^G', 'A^T', 'C^A', 'C^C', 'C^G', 'C^T',
         'G^A', 'G^C', 'G^G', 'G^T', 'T^A', 'T^C', 'T^G', 'T^T']

# def minimum_common_parent(node_1, node_2, root_node):
#     string_1 = node_1["pattern"]
#     string_2 = node_2["pattern"]
#     string_root = root_node["pattern"]
#
#     str_1_pos_start = string_1.find(string_root)
#     str_1_pos_end = str_1_pos_start + len(string_root)
#     str_2_pos_start = string_2.find(string_root)
#     str_2_pos_end = str_2_pos_start + len(string_root)
#
#     while pos_1 >= 0 and
def get_root(graph):
    selector = NodeSelector(graph)
    selected = selector.select("tree_node").where("NOT (a)<-[:containedby]-()")#get the only node in the set
    return selected.first()# the bug says node has no attribute evaluate
def longest_common_substring(s1, s2):
   m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
   longest, x_longest = 0, 0
   for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
   return s1[x_longest - longest: x_longest]
def lcs(root, new_node):
    pr = root["pattern"]
    pn = new_node["pattern"]

    return longest_common_substring(pr,pn)
def tree_making(graph,new_node):
    cs = lcs(get_root(graph), new_node)
    if len(cs)< get_root(graph):
        lcs_node = Node("tree_node")
        lcs_node["pattern"]= cs
        r1 = Relationship(lcs_node,'containedby',graph)
        r2 =Relationship(lcs_node,'containedby',new_node)
        #lcs_node.add(graph)
        #lcs_node.add(new_node)
        return 1
    elif len(lcs(graph.root,new_node))< get_root(graph):
        selector = NodeSelector(get_root(graph))
        childern=selector.select("tree_node").where("NOT (a)<-[:containedby]<-()<-[:containedby]-() AND (a)<-[:containedby]<-()")
        #childern =
        for child_subgraph in childern:
            if (tree_making(child_subgraph,new_node)):
                return 1
def run():
    DB_graph = Graph(password="pass")
    roots =[]
    selector= NodeSelection(DB_graph)
    for pair in pairs:
        node = Node("tree_node")
        node["pattern"]=pair
        roots.append(node)
    for root in roots:
        #"_.name =~ 'J.*'"
        node_set = DB_graph.find('rebase_enzyme')
        #node_set = selector.select("rebase_enzyme").where((root['pattern'] in _.pattern))
        for node in node_set:
            #if node["pattern"] != root["pattern"]:


            print(node['pattern'])
            tree_making(root,node)
run()