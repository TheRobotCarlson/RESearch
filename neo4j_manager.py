from py2neo import Node, Relationship, Graph

graph = Graph(password="pass")

temp_node = Node("test", id="AAATG")
temp_node["stuff"] = "things"

graph.merge(temp_node)

for res in graph.run("MATCH (n) RETURN n"):
    print(res)

temp_node_2 = Node("test", id="AAATG")
graph.merge(temp_node_2)

for res in graph.run("MATCH (n) RETURN n"):
    print(res)


