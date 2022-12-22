
# data of a node
class nodeData:
    def __init__(self, label, mole_num: int, node_link):
        self.label = label
        self. mole_num = mole_num
        self.node_link = node_link


class MoleTree:
    def __init__(self, label, mole_num: int, node_link):
        self.children = []
        self.data = nodeData(label, mole_num, node_link)

    # add child to node
    def add_child(self, child):
        self.children.append(child)

    # build the MoleTree
    def build_tree(self, Ms):
        # sorting all e in Ms with respect to MM(e)


        mole_tree = MoleTree("null", 0, None)
