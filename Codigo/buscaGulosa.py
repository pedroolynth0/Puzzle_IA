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


class BuscaGulosa:
    def __init__(self, size, inicio):
        self.inicio = inicio
        self.n = size
        self.open = []
        self.closed = []
        self.movimentos = 0

    def h(self, start, goal):
        temp = 0
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    x, y = divmod(int(start[i][j]) - 1, self.n)
                    temp += abs(i - x) + abs(j - y)
        return temp

    def process(self):
        start = self.inicio

        grid = [[x + y * self.n for x in range(1, self.n + 1)] for y in range(self.n)]
        grid[-1][-1] = 0

        goal = [[str(num) if num != 0 else '_' for num in sublist] for sublist in grid]

        start = Node(start, 0, 0)
        self.open.append(start)

        while True:
            if not self.open:
                break
            if self.movimentos == 400:
                print("Não foi possível resolver")
                self.closed = []
                break

            cur = self.open.pop(0)

            if self.h(cur.data, goal) == 0:
                self.closed.append(cur)
                self.movimentos += 1
                break

            for i in cur.generate_child():
                self.open.append(i)

            self.closed.append(cur)
            self.movimentos += 1

            self.open.sort(key=lambda x: self.h(x.data, goal), reverse=False)
