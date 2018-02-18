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

# for pair in pairs:
#     parent = Node("rebase_enzyme")
#     parent["pattern"] = pair
#     parent["real_enzyme"] = False
#     print(pair, "-----------------------")
#     graph.merge(parent)
#     for res in graph.data("MATCH (c) WHERE c.pattern CONTAINS \"" + pair + "\" AND length(c.pattern) = 4 RETURN c LIMIT 25"):
#         relationship = Relationship(parent, "CONTAINEDBY", res["c"])
#         graph.merge(relationship)

# def get_enzyme_recur():


def get_enzyme(dna_str, pos):
    left_pos = pos
    right_pos = pos + 1

    dna_str_copy = dna_str[:pos + 1] + "^" + dna_str[pos + 1:]
    print(dna_str_copy)
    str_piece_mid = dna_str[left_pos] + "^" + dna_str[right_pos]
    str_piece_left = str_piece_mid[:2]
    str_piece_right = str_piece_mid[1:]
    next_node = graph.find_one(label="rebase_enzyme", property_key="pattern", property_value=str_piece_mid)

    next_node = list(graph.match(start_node=next_node, rel_type="CONTAINEDBY"))

    next_nodes = [c.nodes()[1] for c in next_node if c.nodes()[1]["pattern"] in dna_str_copy]

    while len(next_nodes) > 0 and any([not node["real_enzyme"] for node in next_nodes]):
        print(next_nodes)
        for node in next_nodes:
            next_node = list(graph.match(start_node=node, rel_type="CONTAINEDBY"))
            # print(next_node[1].nodes())
            next_nodes = [c.nodes()[1] for c in next_node if c.nodes()[1]["pattern"] in dna_str_copy and c.nodes()[1]["pattern"] not in node["pattern"]]

            print(next_nodes)

    # print([(x["pattern"], x["name"]) for x in next_nodes])
    
    return [(x["pattern"], x["name"]) for x in next_nodes][0]

get_enzyme(dna_str="GACCTTCGAGTC", pos=6)
