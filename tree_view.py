import pygame as pg
import os


def get_matrix(root):
    a, flag = [[root]], True
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
            a[i][j] = [a[i][j].key, a[i][j].isRed] if a[i][j] is not None else None

    return a


class Tree_view:

    def __init__(self, w, h):
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{1300}, {200}'
        pg.init()
        self.w, self.h = w, h
        self.window = pg.display.set_mode((w, h), pg.RESIZABLE)
        pg.display.set_caption('Визуальное представление красно-черного дерева')
        self.font = pg.font.SysFont('arial', 15)

    def calc_coors(self, a):
        w1, h1 = max(10, (self.w - 100)//len(a[-1])+1)//1.5, (self.h-100)//len(a)
        x0, y0 = w1+30 if w1 < self.w//2 else self.w//2, (self.h + 30) - h1 if h1 < self.h//2 else self.h//2
        coor = [[(x0 + w1*i, y0) for i in range(len(a[-1]))]]
        for i in range(len(a)-1):
            row = []
            for j in range(0, len(coor[i])-1, 2):
                row.append(((coor[i][j][0]+coor[i][j+1][0])/2, coor[i][j][1]-h1))
            coor.append(row)

        return coor

    def show_tree(self, matrix):
        a = matrix[0]
        coor = self.calc_coors(a)

        while True:
            self.window.fill((200, 200, 200))

            m = set()
            for i in range(len(coor)):
                for j in range(len(coor[i])):
                    if a[len(a) - 1 - i][j] is not None:
                        if a[len(a) - 1 - i][j][0] is not None:
                            m.add(a[len(a)-1-i][j][0])
                        if i != len(coor) - 1:
                            pg.draw.line(self.window, (0, 0, 0), coor[i][j], coor[i + 1][j // 2], 2)
                        if a[len(a) - 1 - i][j][0] is not None:
                            pg.draw.circle(self.window, (0, 0, 0), coor[i][j], 15, 2)
                            pg.draw.circle(self.window, (250, 0, 0) if a[len(a)-1-i][j][1] else (0, 0, 0),
                                           coor[i][j], 13)
                            text = self.font.render(str(a[len(a)-1-i][j][0]), True, (250, 250, 250))
                            self.window.blit(text, (coor[i][j][0]-7, coor[i][j][1]-10))
                        else:
                            pg.draw.circle(self.window, (0, 0, 0), coor[i][j], 5)

            text = self.font.render(' '.join(map(str, sorted(list(m)))), True, (0, 0, 0))
            self.window.blit(text, (10, 10))

            if matrix[1]:
                text = self.font.render('балансировка...', True, (0, 0, 0))
                self.window.blit(text, (10, 30))
            pg.display.flip()

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return 'quit'

                if e.type == pg.KEYUP:
                    if e.key == pg.K_LEFT:
                        return 'prev'
                    if e.key == pg.K_RIGHT:
                        return 'next'
                    if e.key == pg.K_RETURN:
                        return 'add'

                if e.type == pg.MOUSEBUTTONUP:
                    x, y = pg.mouse.get_pos()
                    res = 0
                    for i in range(len(coor)):
                        for j in range(len(coor[i])):
                            if (x - coor[i][j][0]) ** 2 + (y - coor[i][j][1]) ** 2 < 300:
                                res = (len(a)-1-i, j)

                    if res != 0:
                        return str(a[res[0]][res[1]][0])


