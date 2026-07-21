from typing import *


class doc_node:
    content: str
    desc: str
    children: list["doc_node"]
    parent_node: Optional["doc_node"]
    depth: int

    # Nodes are represented using horizontal strips of space, with proportion being the horizontal
    # proportion of treePanel allocated to a node, and start being the starting position of a strip
    # as a fraction of treePanel's width. Nodes are rendered in the centre of their allocated strip
    proportion: float
    start: float

    def __init__(
        self,
        init_content: str,
        init_desc: str,
        parent_node: Optional["doc_node"]
    ):

        self.content = init_content
        self.desc = init_desc
        self.children = []
        self.parent = parent_node
        if parent_node is not None:
            self.depth = parent_node.depth + 1
        else:
            self.depth = 0
        self.nodes_across = 1
        self.proportion = 1.0
        self.start = 0

    # Update content/description if provided
    def update_content(
        self,
        new_content: Optional[str],
        new_desc: Optional[str]
    ):

        if new_content is not None:
            self.content = new_content
        if new_desc is not None:
            self.desc = new_desc

    # Create a new version as a child of the current node
    def add_new_ver(self, new_content: str, new_desc: str) -> "doc_node":
        new_node = doc_node(new_content, new_desc, self)
        self.children.append(new_node)
        return new_node

    # Updates depth of each descendant and returns the highest descendant's depth
    def get_max_depth(self) -> int:
        curr_max = self.depth
        for node in self.children:
            node.depth = self.depth + 1
            node_max_depth = node.get_max_depth()
            if node_max_depth > curr_max:
                curr_max = node_max_depth

        return curr_max

    # Return a list containing all descendants of this node
    def traverse(self) -> list:
        node_list = [self]
        for node in self.children:
            node_list.extend(node.traverse())

        return node_list

    # Calculate and assign the horizontal proportion of visual space allocated to each node
    def distribute_proportion(self):
        for node in self.children:
            # Each child node gets an equal proportion of its parent's space
            node.proportion = self.proportion / len(self.children)
            node.distribute_proportion()

    # Create a dictionary representing this node's subtree
    def create_tree_dict(self) -> dict:
        child_dicts = []
        for node in self.children:
            child_dicts.append(node.create_tree_dict())

        tree_dict = {
            "content": self.content,
            "description": self.desc,
            "children": child_dicts
        }

        return tree_dict

    # Load content of dictionary as a tree
    def load_tree_dict(self, tree_dict: dict) -> int:
        for attr in ("content", "description", "children"):
            if attr not in tree_dict.keys():
                return 1  # Error

        self.content = tree_dict["content"]
        self.desc = tree_dict["description"]

        for child in tree_dict["children"]:
            new_node = doc_node("", "", self)
            if new_node.load_tree_dict(child) == 1:
                return 1
            self.children.append(new_node)

        return 0
