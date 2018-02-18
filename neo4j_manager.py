from py2neo import Node, Relationship, Graph

graph = Graph(password="pass")

#
# temp_node = Node("test", id="AAATG")
# temp_node["stuff"] = "things"
#
# graph.merge(temp_node)
#
# for res in graph.run("MATCH (n) RETURN n"):
#     print(res)
#
# temp_node_2 = Node("test", id="AAATG")
# graph.merge(temp_node_2)
#
# pairs = ['A^A', 'A^C', 'A^G', 'A^T', 'C^A', 'C^C', 'C^G', 'C^T',
#          'G^A', 'G^C', 'G^G', 'G^T', 'T^A', 'T^C', 'T^G', 'T^T']
# for res in graph.run("MATCH (n) where RETURN n"):
#     print(res)

for res in graph.data("MATCH (c) RETURN c LIMIT 4"):
    print(res)

pairs = ['A^A', 'A^C', 'A^G', 'A^T', 'C^A', 'C^C', 'C^G', 'C^T',
         'G^A', 'G^C', 'G^G', 'G^T', 'T^A', 'T^C', 'T^G', 'T^T']

pairs_second_tier = ['C^CA', 'AC^C', 'AC^G', 'C^GA']

# for pair in pairs_second_tier:
#     parent = Node("rebase_enzyme")
#     parent["pattern"] = pair
#     parent["real_enzyme"] = False
#     print(pair, "-----------------------")
#     graph.merge(parent)
#     for res in graph.data("MATCH (c) WHERE c.pattern CONTAINS \"" + pair + "\" RETURN c LIMIT "):
#         relationship = Relationship(parent, "CONTAINEDBY", res["c"])
#         graph.merge(relationship)

for pair in pairs:
    parent = Node("rebase_enzyme")
    parent["pattern"] = pair
    parent["real_enzyme"] = False
    print(pair, "-----------------------")
    graph.merge(parent)
    for res in graph.data("MATCH (c) WHERE c.pattern CONTAINS \"" + pair + "\" AND length(c.pattern) = 4 RETURN c LIMIT 25"):
        relationship = Relationship(parent, "CONTAINEDBY", res["c"])
        graph.merge(relationship)


def get_enzyme(dna_str, pos):
    left_pos = pos
    right_pos = pos + 1
