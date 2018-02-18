from py2neo import Node, Relationship, Graph, GraphError
from datetime import datetime
graph = Graph(password="pass")

label_word = "node_test"
edge_word = "contained_by"
# label_word = "tree_node"
# edge_word = "containedby"
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

# for res in graph.data("MATCH (c) RETURN c LIMIT 4"):
#     print(res)

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


def min_common_pattern(node_root, node_1, node_2):
    str_1 = node_1["pattern"]
    str_2 = node_2["pattern"]
    str_root = node_root["pattern"]

    pos_1 = str_1.find(str_root)
    pos_2 = str_2.find(str_root)

    beg_1 = pos_1
    beg_2 = pos_2

    while str_1[beg_1] == str_2[beg_2]:
        beg_1 -= 1
        beg_2 -= 1
        if beg_1 == 0 or beg_2 == 0:
            break

    if str_1[beg_1] != str_2[beg_2]:
        beg_1 += 1
        beg_2 += 1

    end_1 = pos_1
    end_2 = pos_2

    while str_1[end_1] == str_2[end_2]:
        end_1 += 1
        end_2 += 1
        if end_1 == len(str_1) - 1 or end_2 == len(str_2) - 1:
            break

    if str_1[end_1] != str_2[end_2]:
        end_1 -= 1
        end_2 -= 1

    if end_1 - beg_1 < 2:
        return None
    return str_1[beg_1:end_1 + 1]


def get_children(node_root, constraint=None):
    next_node = list(graph.match(start_node=node_root, rel_type=edge_word))
    # print(next_node[0].nodes()[1])
    # these are the children, exclude this node
    if constraint is None:
        return [c.nodes()[1] for c in next_node if c.nodes()[1]["pattern"] not in node_root["pattern"]]
    else:
        return [c.nodes()[1] for c in next_node if c.nodes()[1]["pattern"] in constraint and
                c.nodes()[1]["pattern"] not in node_root["pattern"]]


def make_child(node_parent, node_child):
    # print("make child?")
    relationship = Relationship(node_parent, edge_word, node_child)
    graph.merge(relationship)


def make_fake_parent(node_parent, future_parent_pattern, node_children):
    # print("here?")
    parent = Node(label_word)
    parent["pattern"] = future_parent_pattern
    parent["real_enzyme"] = False

    relationship = Relationship(node_parent, edge_word, parent)
    graph.merge(relationship)

    old_children = get_children(node_parent)
    for child in node_children:
        if child in old_children:
            relationship = graph.match_one(start_node=node_parent, end_node=child, rel_type=edge_word)
            graph.separate(relationship)
        relationship = Relationship(parent, edge_word, child)
        graph.merge(relationship)


# case 1: no children and contained -> make child
# case 2: children and children not contained -> minimum common pattern
# case 3: children and child is contained -> make child root, recur

def insert_node_recur(node_root, node):
    # print("here3?")

    search_str = node["pattern"]
    if node_root is None:
        return False, None
    root_str = node_root["pattern"]

    children = list(get_children(node_root))
    # print(children)

    # case 1
    if len(children) == 0 and root_str in search_str:
        make_child(node_root, node)
        return True

    sub_len = []
    for child in children:
        if child["pattern"] == node_root["pattern"]:
            continue
        # case 3
        if child["pattern"] in search_str:
            found = insert_node_recur(child, node)
            if found:
                return True
        else:
            match_str = min_common_pattern(node_root, node, child)
            # if len(match_str)
            sub_len.append((len(match_str), match_str, child))

    # case 2
    # pick best match
    # print(sub_len)
    best_match = next(reversed(sorted(sub_len, key=lambda x: x[0])))

    make_fake_parent(node_parent=node_root, future_parent_pattern=best_match[1], node_children=[node, best_match[2]])

    return True

# print(list(reversed(sorted([(1, 2), (4, 2), (2, 2), (4, 2)], key=lambda x: x[0]))))


def insert_node(node):
    # graph.merge(node)
    pattern = node["pattern"]
    # print(pattern)
    cleave_pos = pattern.find("^")
    if cleave_pos == -1:
        return

    str_piece_mid = pattern[cleave_pos - 1: cleave_pos + 2]
    # print(str_piece_mid)
    node_root = graph.find_one(label=label_word, property_key="pattern", property_value=str_piece_mid)
    # print(node_root)
    insert_node_recur(node_root, node)


def get_enzyme_recur(dna_str_copy, node):
    if node["real_enzyme"]:
        print(node["name"])
        return True, node

    next_node = list(graph.match(start_node=node, rel_type=edge_word))
    # these are the children, exclude this node
    next_nodes = ([c.nodes()[1] for c in next_node if
                       c.nodes()[1]["pattern"] in dna_str_copy and c.nodes()[1]["pattern"] not in node["pattern"]])
    # print(next_nodes)
    found = False
    i = 0
    while not found and i < len(next_nodes):
        found, node = get_enzyme_recur(dna_str_copy, next_nodes[i])
        i += 1

    return False, None


def get_enzyme(dna_str, pos):
    start_time = datetime.now()
    left_pos = pos
    right_pos = pos + 1
    # print(pos, len(dna_str), dna_str)

    dna_str_copy = dna_str[:pos + 1] + "^" + dna_str[pos + 1:]
    str_piece_mid = dna_str[left_pos] + "^" + dna_str[right_pos]
    str_piece_left = str_piece_mid[:2]
    str_piece_right = str_piece_mid[1:]
    next_node = graph.find_one(label=label_word, property_key="pattern", property_value=str_piece_mid)

    # print(str_piece_mid, next_node)
    found, node = get_enzyme_recur(dna_str_copy, next_node)

    end_time = datetime.now()
    print("time:", end_time - start_time)
    if found:
        return node["pattern"], node["name"]
    else:
        return None, None

# get_enzyme(dna_str="GACTTCGAGC", pos=3)

# print(min_common_pattern({"pattern": "C^T"}, {"pattern": "GCC^TA"}, {"pattern": "ACC^TA"}))