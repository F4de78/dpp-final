# sort all tuples (moles) in Ms considering values of MM(e)
def sort_tuple(Ms, MM):
    Ms_sorted = []
    for mole in Ms:
        mole_dict = {}  # subdictionary of MM that contains only values of MM for elements in mole tuple
        mole = sorted(mole, reverse=True)  # it grants ordering if MM values are equal: simple numeric order
        for item in mole:
            mole_dict[item] = MM[item]
        # sort mole_dict by value
        mole_dict = dict(sorted(mole_dict.items(), key=lambda item: item[1], reverse=True))
        Ms_sorted.append(tuple(mole_dict.keys()))
    return Ms_sorted



class MoleTree:
    def __init__(self, label, mole_num: int, node_link):
        self.children = []
        self.label = label
        self.mole_num = mole_num
        self.node_link = node_link


    # add child to node
    def add_child(self, child):
        self.children.append(child)

    # build the MoleTree
    def build_tree(self, Ms, MM):
        # sorting all e in Ms with respect to MM(e)
        Ms = sort_tuple(Ms, MM)

        # building tree
        max_level = max(len(mole) for mole in Ms) # is equivalent to the max len for tuples in Ms
        for level in range(0, max_level-1):
            for mole in Ms:
                # build the node for the element



