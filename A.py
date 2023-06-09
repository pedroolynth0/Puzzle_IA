class Node:
    def __init__(self, data, level, fval):
        """ Inicializa o nó com os dados, nível do nó e o valor f calculado """
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        """ Gera nós filhos a partir do nó atual, movendo o espaço em branco
            em uma das quatro direções {cima, baixo, esquerda, direita} """
        x, y = self.find(self.data, '_')
        """ val_list contém os valores de posição para mover o espaço em branco em
            uma das 4 direções [cima, baixo, esquerda, direita], respectivamente. """
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move o espaço em branco na direção especificada e, se a posição estiver fora
            dos limites, retorna None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def copy(self, root):
        """ Função de cópia para criar uma matriz similar ao nó fornecido """
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find(self, puz, x):
        """ Usado especificamente para encontrar a posição do espaço em branco """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j


class A:
    def __init__(self, size, inicio):
        """ Inicializa o tamanho do quebra-cabeça com o tamanho especificado, listas aberta e fechada vazias """
        self.inicio = inicio
        self.n = size
        self.open = []
        self.closed = []
        self.movimentos =0

    def accept(self):
        """ Aceita o quebra-cabeça do usuário """
        puz = []
        for i in range(0, self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self, start, goal):
        """ Função heurística para calcular o valor heurístico f(x) = h(x) + g(x) """
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        """ Calcula a diferença entre os quebra-cabeças dados """
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def process(self):
        """ Aceita o estado inicial e objetivo do quebra-cabeça """
        print("Digite a matriz do estado inicial \n")
        start = self.inicio

        grid = [[x + y * 3 for x in range(1, 3 + 1)] for y in range(3)]
        grid[-1][-1] = 0

        goal = [[str(num) if num != 0 else '_' for num in sublist] for sublist in grid]
        print("Digite a matriz do estado objetivo \n")

        start = Node(start, 0, 0)
        start.fval = self.f(start, goal)
        """ Coloca o nó inicial na lista aberta """
        self.open.append(start)
        print("\n\n")
        
        while True:
            if self.movimentos ==400:
                print("Nao foi possivel resolver")
                self.closed =[]
                break
            cur = self.open[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \'/ \n")
            for i in cur.data:
                for j in i:
                    print(j, end=" ")
                print("")
            """ Se a diferença entre o nó atual e o objetivo for 0, chegamos ao nó objetivo """
            if self.h(cur.data, goal) == 0:
                self.closed.append(cur)
                self.movimentos = self.movimentos +1
                break
            for i in cur.generate_child():
                i.fval = self.f(i, goal)
                self.open.append(i)
            self.closed.append(cur)
            self.movimentos = self.movimentos +1
            del self.open[0]

            """ Classifica a lista aberta com base no valor f """
            self.open.sort(key=lambda x: x.fval, reverse=False)
