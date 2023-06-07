import pygame
import random
import time
from sprite import *
from settings import *
from resolver import *
import threading
from buscaGulosa import *
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.start_A = False
        self.start_Gulosa = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        self.movements =0

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        # Cria uma nova matriz representando o jogo
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    # Verifica as direções possíveis para mover o espaço vazio
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        # Escolhe uma direção aleatória e realiza o movimento
        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        # Inicializa as variáveis do jogo
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "A*", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "Busca Gulosa", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "Reset", WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                # Verifica se o jogo foi concluído
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            # Embaralha o jogo e inicia a resolução em uma nova thread
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 5:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True
                if self.start_A:
                    thread = threading.Thread(target=self.BuscaA)
                    thread.start()
                    self.start_A = False
                elif self.start_Gulosa:
                    thread = threading.Thread(target=self.BuscaGulosa)
                    thread.start()
                    self.start_Gulosa = False                

        self.all_sprites.update()

    def BuscaA(self):
        self.movements = 0
        # Método para resolver o jogo
        time.sleep(1)
        strings = [[str(num) if num != 0 else '_' for num in sublist] for sublist in self.tiles_grid]
        puz = A(3, strings)
        puz.process()
        self.movements = puz.movimentos
        
        for resultado in puz.closed:
            strings = [[int(num) if num != '_' else 0 for num in sublist] for sublist in resultado.data]
            self.tiles_grid = strings
            self.draw_tiles()
            time.sleep(0.1)

    def BuscaGulosa(self):
        # Método para resolver o jogo
        time.sleep(1)
        strings = [[str(num) if num != 0 else '_' for num in sublist] for sublist in self.tiles_grid]
        puz = BuscaGulosa(3, strings)
        puz.process()
        self.movements = puz.movimentos
        UIElement(100, 400, "Movimentos: %d" % 10).draw(self.screen)  # Exibe a quantidade de movimentos
        

        for resultado in puz.closed:
            strings = [[int(num) if num != '_' else 0 for num in sublist] for sublist in resultado.data]
            self.tiles_grid = strings
            self.draw_tiles()
            time.sleep(0.1)            

    def draw_grid(self):
        # Desenha a grade do jogo na tela
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        # Desenha os elementos na tela
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 400, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        UIElement(100, 400, "Movimentos: %d" % self.movements).draw(self.screen)  # Exibe a quantidade de movimentos
        pygame.display.flip()

    def events(self):
        # Lida com eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            # Verifica se um tile foi clicado e realiza o movimento
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        # Verifica se um botão foi clicado
                        if button.text == "A*":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            self.start_A = True

                        if button.text == "Busca Gulosa":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            self.start_Gulosa = True

                        if button.text == "Reset":
                            self.new()

game = Game()
while True:
    game.new()
    game.run()
