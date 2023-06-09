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


class Minimax:
    def __init__(self, size, inicio):
        """ Inicializa o tamanho do quebra-cabeça com o tamanho especificado """
        self.inicio = inicio
        self.n = size
        self.movimentos = 0

    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or len(node.generate_child()) == 0:
            # Implemente sua função de avaliação heurística aqui
            return 0

        if maximizing_player:
            max_eval = float('-inf')
            for child in node.generate_child():
                eval = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for child in node.generate_child():
                eval = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def solve_puzzle(self, node, depth):
        goal = [['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '_']]

        if node.data == goal:
            return True

        if depth == 0:
            return False

        for child in node.generate_child():
            if self.solve_puzzle(child, depth - 1):
                return True

        return False

    def process(self, depth):
        print("Digite a matriz do estado inicial \n")
        start = self.inicio

        start = Node(start, 0, 0)

        if self.solve_puzzle(start, depth):
            print("O quebra-cabeça foi resolvido!")
        else:
            print("Não foi possível resolver o quebra-cabeça.")

