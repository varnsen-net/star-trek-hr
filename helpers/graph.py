import networkx as nx


# alternate methods. save for posterity.
# G = nx.gnp_random_graph(20, 0.1)
# tree = nx.bfs_tree(G, 0)
# tree = nx.minimum_spanning_tree(G)
# beam = nx.bfs_beam_edges(G, source=0, width=3, value=lambda x: 1)
# G = nx.Graph(beam)



def generate_story_graph(n):
    """Generate a random directed tree graph with n nodes.

    :param int n: number of nodes in the graph
    :return: a list of edges and a list of nodes in breadth-first order
    :rtype: tuple
    """
    tree = nx.random_tree(n, create_using=nx.DiGraph)
    edge_list = list(nx.edge_bfs(tree, source=0))
    layers = list(nx.bfs_layers(tree, sources=[0]))
    node_list = [node for layer in layers for node in layer] # flatten layers

    # sanity check
    forest = nx.forest_str(tree, sources=[0])
    print(forest)

    return node_list, edge_list


def get_parent(node, edge_list):
    """Get the parent node of a given node.

    :param int node: the node to find the parent of
    :param list[tuple] edge_list: a list of edge tuples (parent, child)
    :return: the parent node
    :rtype: int
    """
    for edge in edge_list:
        if edge[1] == node:
            return edge[0]


def get_children(node, edge_list):
    """Get the children nodes of a given node.

    :param int node: the node to find the children of
    :param list[tuple] edge_list: a list of edge tuples (parent, child)
    :return: a list of children nodes
    :rtype: list[int]
    """
    children = []
    for edge in edge_list:
        if edge[0] == node:
            children.append(edge[1])
    return children


def node_is_leaf(node, edge_list):
    """Determine if a node is a leaf node.

    :param int node: the node to check
    :param list[tuple] edge_list: a list of edge tuples (parent, child)
    :return: True if the node is a leaf, False otherwise
    :rtype: bool
    """
    return len(get_children(node, edge_list)) == 0


def generate_storyboard_json(node_list, edge_list):
    """Generate a JSON object for the storyboard.

    Iterates over a node list and constructs a json object with parent and
    children node information. Nodes are assumed to be in breadth-first order.

    :param list[int] node_list: a list of nodes in breadth-first order
    :param list[tuple] edge_list: a list of edge tuples (parent, child)
    :return: a storyboard json object
    :rtype: dict
    """
    node_json = {}
    for node in node_list:
        parent = get_parent(node, edge_list)
        children = get_children(node, edge_list)
        node_json[node] = {'parent': parent,
                           'is_leaf': node_is_leaf(node, edge_list),
                           'previous_paragraph': '',
                           'previous_dialogue_option': '',
                           'paragraph_text': '',
                           'dialogue_options': {}}
        for child in children:
            node_json[node]['dialogue_options'][child] = ''
    return node_json


