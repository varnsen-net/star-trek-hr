"""Helper class to generate a story graph and storyboard JSON object."""

import networkx as nx


class StoryGraph:
    """A class to represent a story graph.
    
    This class generates a random tree graph with a given number of nodes and
    provides methods to access information about the graph.

    :attr int n: the total number of nodes in the graph
    :attr nx.DiGraph tree: the tree graph object
    """

    def __init__(self, n):
        """Initialize a StoryGraph object.

        :param int n: number of nodes in the graph
        """
        self.n = n
        self.tree = nx.random_labeled_tree(n)

    @property
    def edge_list(self):
        """Return a list of edges in the graph.
        
        :return: a list of edge tuples (parent, child)
        :rtype: list[tuple]
        """
        return list(nx.edge_bfs(self.tree, source=0))

    @property
    def layers(self):
        """Return a list of nodes in each layer of the graph.
        
        :return: a list of lists of nodes
        :rtype: list[list[int]]
        """
        return list(nx.bfs_layers(self.tree, sources=[0]))

    @property
    def node_list(self):
        """Return a list of nodes in breadth-first order.

        :return: a list of nodes
        :rtype: list[int]
        """
        return [node for layer in self.layers for node in layer]

    def print_graph(self):
        """Print the graph as a string."""
        print(nx.write_network_text(self.tree, sources=[0]))

    def get_path_to_node(self, node):
        """Get the path from the root node to a given node.

        :param int node: the node to find the path to
        :return: a list of node indices ordered from root to node
        :rtype: list[int]
        """
        return nx.shortest_path(self.tree, source=0, target=node)

    def get_node_children(self, node):
        """Get the children nodes of a given node.

        :param int node: the node to find the children of
        :return: a list of children nodes
        :rtype: list[int]
        """
        children = []
        for edge in self.edge_list:
            if edge[0] == node:
                children.append(edge[1])
        return children

    def is_leaf(self, node):
        """Determine if a node is a leaf node.

        :param int node: the node to check
        :return: True if the node is a leaf, False otherwise
        :rtype: bool
        """
        return len(self.get_node_children(node)) == 0

    def generate_storyboard_json(self):
        """Generate a JSON object for the storyboard.

        Iterates over a node list and constructs a json object with parent and
        children node information. Nodes are assumed to be in breadth-first order.

        :return: a storyboard json object
        :rtype: dict
        """
        node_json = {}
        for node in self.node_list:
            path_to_node = self.get_path_to_node(node)
            children = self.get_node_children(node)
            node_json[node] = {'path_to_node': path_to_node,
                               'is_leaf': self.is_leaf(node),
                               'paragraph_text': "",
                               'dialogue_options': {}}
            for child in children:
                node_json[node]['dialogue_options'][child] = None
        return node_json


if __name__ == '__main__':
    graph = StoryGraph(20)
    graph.print_graph()
    print(graph.edge_list)
    print(graph.layers)
    print(graph.node_list)
    storyboard = graph.generate_storyboard_json()
    for node, data in storyboard.items():
        print(node)
        print(data)
