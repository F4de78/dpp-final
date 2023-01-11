import copy

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
        print("  " * self.level, self.label,":",self.mole_num)
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
                    #print("child label: ", new_label, ", level ", self.level, " child Ms list ", new_Ms)
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
        #TODO: da stamapre con logging
        #print("score table: ")
        #print("label MM IL link")
        #for label,score in score_table.items():
        #    print(label, " ", score.MM, " " ,score.IL, " ", [i.label for i in score.node_link])
        return score_table

    # remove the subtree having 'self' as root, the root and his link in score table
    def remove_subtree(self, root, score_table):
        if self.label != root:
            score_table[self.label].node_link.remove(self) # remove from score table links
        for child in self.children:
            child.remove_subtree(root,score_table) #recursively remove subtree 
        self.children.clear() # remove all children from self
        if self.label == root:
            # we don't need to update the children of root, because at this point they don't exists anymore
            for ancestor in self.get_ancestors(): # update ancestors of root
                ancestor.mole_num -= self.mole_num
                score_table[ancestor.label].MM -= self.mole_num
                #we probably need to update IL 
            self.father.children.remove(self) # remove root
        score_table[self.label].MM -= self.mole_num
        del self # ?

    def suppress_moles(self,MM,IL):
        score_table = self.build_score_table(MM,IL)
        #TODO: da stamapre con logging
        #print("initial score table:")
        #for label,score in score_table.items():
        #    print(label, " ", score.MM, " " ,score.IL, " ", [i.label for i in score.node_link])
        supp_item = set()
        keys = list(score_table)
        while keys:  # while score table is not empty
            #print("keys",keys)
            score = []
            for _,e in score_table.items():
                score.append(e.MM/e.IL) # compute all MM/IL for all label
            #k = list(score_table.keys())
            e = keys[score.index(max(score))]
            #TODO: da stamapre con logging
            #print("To delete: ", e)
            supp_item.add(e) # select the label with the max value of MM/IL
            for link in score_table[e].node_link:
                link.remove_subtree(link.label,score_table)
            score_table[e].node_link.clear()
            #remove e from score table
            _ = score_table.pop(e)
            keys.remove(e)
            for k in list(score_table): # check if we have MM == 0 in score table
                if score_table[k].MM == 0:
                    _ = score_table.pop(k)
                    keys.remove(k)
            #TODO: da stamapre con logging
            print("-------------------")
            print("tree:")
            self.print_tree()
            print("score table:")
            for label,score in score_table.items():
                print(label, " ", score.MM, " ", score.IL, " ", [i.label for i in score.node_link])
        return supp_item
