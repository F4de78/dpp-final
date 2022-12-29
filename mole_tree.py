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
    def __init__(self, level, Ms, label, mole_num: int, father):
        self.level = level # level of the node in tree
        self.Ms = Ms # list of visible moles for the node
        self.children = [] # (list of nodes)
        self.father = father
        self.label = label
        self.mole_num = mole_num
        #self.node_link = node_link #replaced by a list of nodes in score table
        
    def print_tree(self):
        print("  " * self.level, self.label)
        for child in self.children:
            child.print_tree()

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
                    new_child = MoleTree(self.level+1, new_Ms, new_label, 1, self)
                    self.children.append(new_child)
                    #new_child.build_tree(MM)  # recursion by rami
        # recursion by levels
        for child in self.children:
            child.build_tree(MM)  # recursion

    def get_ancestors(self):
        ancestors = []
        node = self
        while node.father.label != "null":
            ancestors.append(node.father)
            node = node.father
        return ancestors

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
        #for label,score in score_table.items():
        #    print(label, " ", score.MM, " " ,score.IL, " ", [i.label for i in score.node_link])
        return score_table

    # remove the subtree having 'self' as root
    def remove_subtree(self):
        print(self)
        self.father.children.remove(self)
        for child in self.children:
           child.remove_subtree()
        del self
           
         

    def suppress_moles(self,MM,IL):
        score_table = self.build_score_table(MM,IL)
        supp_item = set()
        tab_len = len(score_table)
        while tab_len != 0: # while is not empty
            score = []
            for _,e in score_table.items():
                score.append(e.MM/e.IL) # compute all MM/IL for all label
            k = list(score_table.keys())
            e = k[score.index(max(score))]
            supp_item.add(e) # select the label with the max value of MM/IL

            # update ancetors mole_number and eliminate e
            for link in score_table[e].node_link:
                print(link.get_ancestors())
                for ancestor in link.get_ancestors(): # update the value of mole_num of the ancestors of link ...
                    ancestor.mole_num -= link.mole_num # ... by removing the value of link from it
                    score_table[ancestor.label].MM -= link.mole_num 
                    if ancestor.mole_num == 0:
                        ancestor.remove_subtree()
                #link.remove_subtree()
            for k in score_table: # check if we have MM == 0 in score table
                if score_table[k].MM == 0:
                    #_ = score_table.pop(k)
                    tab_len -= 1
            print(tab_len)
        return supp_item

           



