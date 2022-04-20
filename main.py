import random
import tree_view


class Node:
    def __init__(self, key, node_id=-1):
        self.key = key
        self.isRed = False
        self.left = None
        self.rigth = None
        self.node_id = node_id


class RB_Tree:
    def __init__(self):
        self.root = None
        self.hist = []
        self.index_show = -1
        self.next_id = 0

    def turn(self, node):
        father, grandpa = self.progenitors(node.node_id)[:2]
        if father.left == node:
            father.left = node.rigth
            node.rigth = father
        else:
            father.rigth = node.left
            node.left = father

        if grandpa.key is not None:
            if grandpa.left == father:
                grandpa.left = node
            else:
                grandpa.rigth = node
        else:
            self.root = node
            self.root.isRed = False

    def balancing(self, new: Node):
        father, grandpa, great_grandpa = self.progenitors(new.node_id)[:3]

        if not (new.key is None or father is None or grandpa is None) and new.isRed and father.isRed:
            uncle = grandpa.left if father == grandpa.rigth else grandpa.rigth
            self.show()

            if uncle.isRed:
                father.isRed = False
                uncle.isRed = False
                grandpa.isRed = True
                self.root.isRed = False
                self.balancing(grandpa)
            elif grandpa.rigth.left == new or grandpa.left.rigth == new:
                self.turn(new)
                self.balancing(father)
            else:
                self.turn(father)
                grandpa.isRed = True
                father.isRed = False

    def progenitors(self, node_id) -> list[Node]:
        a, flag = [[self.root]], True
        while flag:
            flag = False
            row = []
            for e in a[-1]:
                if e is not None:
                    flag = True
                    row += [e.left, e.rigth]
                else:
                    row += [None, None]
            if flag:
                a.append(row)

        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j] is not None and a[i][j].node_id == node_id:
                    j1, desc = j, []
                    for i1 in range(i-1, -1, -1):
                        desc.append(a[i1][j1 // 2])
                        j1 //= 2
                    return desc + [Node(None)] * (3 - len(desc))

        return [Node(None)] * 3

    def add(self, key, red=True):
        if self.root is None:
            self.root = Node(key, node_id=self.next_id)
            self.next_id += 1
            self.root.isRed = False
            self.root.left = Node(None)
            self.root.rigth = Node(None)
            return 0

        now = self.root
        while now.key is not None:
            now = now.left if key <= now.key else now.rigth

        now.key = key
        now.isRed = red
        now.node_id = self.next_id
        self.next_id += 1
        now.left = Node(None)
        now.rigth = Node(None)

        tree.balancing(now)

    def delete(self, node_id):
        father = self.progenitors(node_id)[0]
        if father.key is None and self.root.node_id != node_id:
            return 0

        node = self.root if self.root.node_id == node_id else None
        if node is None:
            node = father.rigth if father.rigth.node_id == node_id else father.left

        if node.left.key is not None and node.rigth.key is not None:
            now = node.left
            while now.rigth.key is not None:
                now = now.rigth
            node.key, now.key = now.key, node.key
            print(now.key)
            self.delete(now.node_id)
        elif node.left.key is not None or node.rigth.key is not None:
            node.key = node.left.key if node.left.key is not None else node.rigth.key
            node.left = Node(None)
            node.rigth = Node(None)
        elif node.left.key is None and node.rigth.key is None:
            if father.rigth == node:
                father.rigth = Node(None)
            else:
                father.left = Node(None)
            if not node.isRed:
                self.show()
                brother = father.left if father.rigth.key is None else father.rigth
                self.rebalansing(father, brother)

    def rebalansing(self, father: Node, brother: Node):
        if father.rigth == brother:
            if not brother.isRed:
                if brother.rigth.isRed:
                    brother.rigth.isRed = False
                    brother.isRed = father.isRed
                    father.isRed = False
                    self.turn(brother)
                elif brother.left.isRed:
                    brother.left.isRed = brother.isRed
                    brother.isRed = True
                    self.turn(brother.left)
                    brother = father.rigth
                    brother.rigth.isRed = False
                    brother.isRed = father.isRed
                    father.isRed = False
                    self.turn(brother)
                else:
                    brother.isRed = True
                    if father.isRed:
                        father.isRed = False
                    else:
                        new_father = self.progenitors(father.node_id)[0]
                        new_brother = new_father.left if new_father.rigth == father else new_father.rigth
                        self.show()
                        if new_brother is not None:
                            self.rebalansing(new_father, new_brother)
            else:
                father.isRed = True
                brother.isRed = False
                self.turn(brother)
                self.show()
                self.rebalansing(father, father.rigth)
        else:
            if not brother.isRed:
                if brother.left.isRed:
                    brother.left.isRed = False
                    brother.isRed = father.isRed
                    father.isRed = False
                    self.turn(brother)
                elif brother.rigth.isRed:
                    brother.rigth.isRed = brother.isRed
                    brother.isRed = True
                    self.turn(brother.rigth)
                    brother = father.left
                    brother.left.isRed = False
                    brother.isRed = father.isRed
                    father.isRed = False
                    self.turn(brother)
                else:
                    brother.isRed = True
                    if father.isRed:
                        father.isRed = False
                    else:
                        new_father = self.progenitors(father.node_id)[0]
                        new_brother = new_father.left if new_father.rigth == father else new_father.rigth
                        self.show()
                        if new_brother is not None:
                            self.rebalansing(new_father, new_brother)
            else:
                father.isRed = True
                brother.isRed = False
                self.turn(brother)
                self.show()
                self.rebalansing(father, father.left)

    def show(self, rec=True):
        self.index_show = len(self.hist)
        self.hist.append([tree_view.get_matrix(self.root), rec])
        while True:
            res = viewer.show_tree(self.hist[self.index_show])
            if res == 'next' and self.index_show < len(self.hist)-1:
                self.index_show += 1
            elif res == 'prev' and self.index_show > 0:
                self.index_show -= 1
            elif res == 'add':
                self.index_show = len(self.hist) - 1
                return 0
            elif res == 'quit':
                exit()
            elif res[-1].isdigit() and self.index_show == len(self.hist) - 1 and not self.hist[-1][1]:
                self.delete(int(res))
                self.index_show = len(self.hist)
                self.hist.append([tree_view.get_matrix(self.root), False])


tree = RB_Tree()
viewer = tree_view.Tree_view(600, 600)


while True:
    tree.add(random.randint(-99, 99))
    tree.show(rec=False)
