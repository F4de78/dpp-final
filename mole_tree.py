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

class ScoreList:
    def __init__(self,MM_value,IL_value,link):
        self.MM = MM_value
        self.IL = IL_value
        self.node_link = link # replace linking all nodes in tree

class MoleTree:
    def __init__(self, level, Ms, label, mole_num: int, node_link):
        self.level = level # level of the node in tree
        self.Ms = Ms # list of visible moles for the node
        self.children = [] # (list of nodes)
        self.label = label
        self.mole_num = mole_num
        #self.node_link = node_link #replaced by a list of nodes in score table


    # add child to node
    def add_child(self, child):
        self.children.append(child)

    # build the subtree from the node (recursive)
    def build_tree(self, MM):
        for mole in self.Ms:
            # add children to the node based on level element
            if self.level != len(mole):  # exit recursion: we reached a leaf
                new_label = mole[self.level]
                if new_label in [node.label for node in self.children]:  # child node already exists
                    for child in self.children:
                        if new_label == child.label:
                            child.mole_num += 1
                else:  # add new child node
                    # create Ms for the child
                    #new_Ms = [mtuple for mtuple in self.Ms if mole[self.level] == new_label]
                    new_Ms = []
                    for mtuple in self.Ms:
                        if mtuple[self.level] == new_label:
                            new_Ms.append(mtuple)
                    print("child label: ", new_label, ", level ", self.level, " child Ms list ", new_Ms)
                    # create child node
                    new_child = MoleTree(self.level+1, new_Ms, new_label, 1, None)
                    self.children.append(new_child)
                    #new_child.build_tree(MM)  # recursion by rami
        # recursion by levels
        for child in self.children:
            child.build_tree(MM)  # recursion


    def build_link(self,label,ret:list):
        for child in self.children:
            if child.label == label:
                ret.append(child)
            else:
                child.build_link(label,ret)


    def build_score_table(self,MM:dict,IL:dict):
        score_table = {}
        labels = MM.keys()
        for label in labels:
            l = []
            self.build_link(label,l)
            score_table[label] = ScoreList(MM[label],IL[label],l)

        print("score table: ")
        print("label MM IL link")
        for label,score in score_table.items():
            print(label, " ", score.MM, " " ,score.IL, " ", [i.mole_num for i in score.node_link])



