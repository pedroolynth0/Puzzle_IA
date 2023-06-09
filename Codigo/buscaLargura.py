from collections import deque

class Node:
    def __init__(self, data, level, fval):
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        x, y = self.find(self.data, '_')
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp_puz[x1][y1], temp_puz[x2][y2] = temp_puz[x2][y2], temp_puz[x1][y1]
            return temp_puz
        else:
            return None

    def copy(self, root):
        temp = []
        for i in root:
            t = i[:]
            temp.append(t)
        return temp

    def find(self, puz, x):
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if puz[i][j] == x:
                    return i, j


class BuscaEmLargura:
    def __init__(self, size, inicio):
        self.inicio = inicio
        self.n = size
        self.open = deque()
        self.closed = []
        self.movimentos = 0

    def process(self):
        start = self.inicio

        goal = [[str(x + y * self.n) for x in range(1, self.n + 1)] for y in range(self.n)]
        goal[-1][-1] = '_'

        start = Node(start, 0, 0)
        self.open.append(start)

        while self.open:
            if self.movimentos == 10000000:
                print("Não foi possível resolver")
                self.closed = []
                break

            cur = self.open.popleft()
            self.closed.append(cur)

            if cur.data == goal:
                break

            for child in cur.generate_child():
                self.open.append(child)

            self.movimentos += 1