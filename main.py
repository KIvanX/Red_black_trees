import random
import tree_view


class Node:
    def __init__(self, key):
        self.key = key
        self.isRed = False
        self.left = None
        self.rigth = None


class RB_Tree:
    def __init__(self):
        self.root = None

    def balancing(self, new: Node):
        father, grandpa, great_grandpa = self.descendants(new)[:3]

        if father is not None and grandpa is not None and new.isRed and father.isRed:

            uncle = grandpa.left if father == grandpa.rigth else grandpa.rigth

            # print(f'X:{new.key} P:{father.key} G:{grandpa.key} U:{uncle.key} GG:{great_grandpa is not None}')
            self.show()

            if uncle.isRed:
                father.isRed = False
                uncle.isRed = False
                grandpa.isRed = True
                self.balancing(grandpa)
            elif grandpa.rigth.left == new or grandpa.left.rigth == new:
                if father.left == new:
                    grandpa.rigth = new
                    father.left = new.rigth
                    new.rigth = father
                else:
                    grandpa.left = new
                    father.rigth = new.left
                    new.left = father
                self.balancing(father)
            else:
                if father.left == new:
                    grandpa.left = father.rigth
                    father.rigth = grandpa
                else:
                    grandpa.rigth = father.left
                    father.left = grandpa

                if great_grandpa is not None:
                    if great_grandpa.left == grandpa:
                        great_grandpa.left = father
                    else:
                        great_grandpa.rigth = father

                grandpa.isRed = True
                father.isRed = False

                if grandpa == self.root:
                    self.root = father

            if self.root.isRed:
                self.root.isRed = False

    def descendants(self, child, by_key=False) -> list[Node]:
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
                if a[i][j] is not None and (by_key and a[i][j].key == child or not by_key and a[i][j] == child):
                    j1, desc = j, []
                    for i1 in range(i-1, -1, -1):
                        desc.append(a[i1][j1 // 2])
                        j1 //= 2
                    return desc + [Node(None)] * (3 - len(desc))

    def add(self, key, red=True):
        if self.root is None:
            self.root = Node(key)
            self.root.isRed = False
            self.root.left = Node(None)
            self.root.rigth = Node(None)
            return 0

        now = self.root
        while now.key is not None:
            now = now.left if key < now.key else now.rigth

        now.key = key
        now.isRed = red
        now.left = Node(None)
        now.rigth = Node(None)

        tree.balancing(now)

    def delete(self, key):
        father = self.descendants(key, by_key=True)[0]
        if father.key is None and self.root.key != key:
            return 0

        if self.root.key == key:
            node = self.root
        else:
            node = father.rigth if father.rigth.key == key else father.left

        if node.left.key is not None and node.rigth.key is not None:
            now = node.left
            while now.rigth.key is not None:
                now = now.rigth
            now.key, node.key = node.key, now.key
            self.delete(now.key)

        elif node.left.key is not None or node.rigth.key is not None:
            print('2')
            node.key = node.left.key if node.left.key is not None else node.rigth.key
            node.left = node.rigth = Node(None)

        elif node.isRed and node.left.key is None and node.rigth.key is None:
            print('3')
            if father.rigth == node:
                father.rigth = Node(None)
            else:
                father.left = Node(None)

        elif not node.isRed and node.left.key is None and node.rigth.key is None:
            print('4')
            if father.rigth == node:
                father.rigth = Node(None)
            else:
                father.left = Node(None)
            self.rebalansing(father)

    def rebalansing(self, father):
        brother = father.left if father.rigth.key is None else father.rigth
        if father.isRed:
            print('К')
            father.isRed, brother.isRed = brother.isRed, father.isRed
            if brother.left.isRed:
                self.balancing(brother.left)
                father.isRed = False
                brother.isRed = True
                brother.left.isRed = False
        else:
            if brother.isRed and brother.rigth.key is not None and \
                    (brother.rigth.left.isRed + brother.rigth.rigth.isRed) == 0:
                print('ЧКЛrЧlЧ')
                brother.rigth.isRed = True
                grandpa = self.descendants(father)[0]
                if grandpa.key is not None:
                    if grandpa.rigth == father:
                        grandpa.rigth = brother
                    else:
                        grandpa.left = brother

                father.left = brother.rigth
                brother.rigth = father

                if father == self.root:
                    self.root = brother
                    self.root.isRed = False
            elif brother.isRed and brother.rigth.key is not None and brother.rigth.left.isRed:
                print('ЧКrЛlК')
                brother.rigth.left.isRed = False
                brother.rigth.isRed = True
                self.balancing(brother.rigth)
                father.isRed = False
            elif not brother.isRed and (brother.rigth.isRed or brother.left.isRed):
                print('ЧЧК')
                brother.isRed = True
                self.balancing(brother.rigth if brother.rigth.isRed else brother.left)
                # father.isRed = False
                # brother.isRed = False
            elif not (brother.isRed or brother.left.isRed or brother.rigth.isRed):
                print('ЧЧЧЧ')
                brother.isRed = True

    def show(self):
        v = 0
        while v is not None:
            v = viewer.show_tree(self.root)
            if v is not None and v != 0:
                print('del:', v[0])
                self.delete(v[0])


tree = RB_Tree()
viewer = tree_view.Tree_view(600, 600)


# v = [(10, 0), (7, 1), (3, 0), (8, 0), (1, 1), (0, 0), (2, 0), (4, 1)]
# for key, red in v:
#     tree.add(key, red=bool(red))

while True:
    tree.add(random.randint(-99, 99))
    tree.show()
