import pygame
import sys


class GameUI:
    COLORS = {
        "bg": (128, 128, 128),
        "grid": (0, 0, 0),
        "x": (200, 0, 0),
        "o": (0, 0, 200),
        "button": (100, 100, 100),
        "button_hover": (150, 150, 150),
        "button_text": (255, 255, 255)
    }

    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 400, 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.font = pygame.font.SysFont(None, 32)
        self.clock = pygame.time.Clock()

        self.cell_size = self.WIDTH // 3
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.bot = False
        self.winner = None

        # Buttons
        self.restart_btn = pygame.Rect(10, self.HEIGHT - 60, 180, 40)
        self.bot_btn = pygame.Rect(210, self.HEIGHT - 60, 180, 40)

    def draw_board(self):
        self.screen.fill(self.COLORS["bg"])
        # Grid
        for i in range(1, 3):
            pygame.draw.line(self.screen, self.COLORS["grid"], (0, i*self.cell_size), (self.WIDTH, i*self.cell_size), 3)
            pygame.draw.line(self.screen, self.COLORS["grid"], (i*self.cell_size, 0), (i*self.cell_size, self.WIDTH), 3)
        # X und O
        for y in range(3):
            for x in range(3):
                center = (x*self.cell_size + self.cell_size//2, y*self.cell_size + self.cell_size//2)
                if self.board[y][x] == "X":
                    pygame.draw.line(self.screen, self.COLORS["x"], (center[0]-40, center[1]-40), (center[0]+40, center[1]+40), 5)
                    pygame.draw.line(self.screen, self.COLORS["x"], (center[0]+40, center[1]-40), (center[0]-40, center[1]+40), 5)
                elif self.board[y][x] == "O":
                    pygame.draw.circle(self.screen, self.COLORS["o"], center, 40, 5)

    def draw_ui(self):
        # Restart Button
        pygame.draw.rect(self.screen, self.COLORS["button"], self.restart_btn)
        txt2 = self.font.render("Neustart", True, self.COLORS["button_text"])
        self.screen.blit(txt2, (self.restart_btn.x + 35, self.restart_btn.y + 5))

        # Bot Button
        pygame.draw.rect(self.screen, self.COLORS["button_hover"] if self.bot else self.COLORS["button"], self.bot_btn)
        txt = self.font.render(f"Auto Solver: {'AN' if self.bot else 'AUS'}", True, self.COLORS["button_text"])
        self.screen.blit(txt, (self.bot_btn.x + 10, self.bot_btn.y + 5))

    def handle_click(self, pos):
        if self.restart_btn.collidepoint(pos):
            self.reset_game()
            return
        elif self.bot_btn.collidepoint(pos):
            self.bot = not self.bot
            return

        if self.winner:
            return

        x = pos[0] // self.cell_size
        y = pos[1] // self.cell_size
        if x < 3 and y < 3 and self.board[y][x] == "":
            self.board[y][x] = self.current_player
            self.check_winner()
            self.switch_player()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        lines = self.board + [list(col) for col in zip(*self.board)] + [[self.board[i][i] for i in range(3)], [self.board[i][2-i] for i in range(3)]]
        for line in lines:
            if line[0] != "" and all(cell == line[0] for cell in line):
                self.winner = line[0]
                return
        if all(self.board[y][x] != "" for y in range(3) for x in range(3)):
            self.winner = "Unentschieden"

    def bot_move(self):
        if self.winner or self.current_player != "O":
            return
        best_score = -float('inf')
        best_move = None
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == "":
                    self.board[y][x] = "O"
                    score = self.minimax(False)
                    self.board[y][x] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (y, x)
        if best_move:
            y, x = best_move
            self.board[y][x] = "O"
            self.check_winner()
            self.switch_player()

    def minimax(self, is_maximizing):
        if self.check_winner_state("O"):
            return 1
        if self.check_winner_state("X"):
            return -1
        if all(self.board[y][x] != "" for y in range(3) for x in range(3)):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == "":
                        self.board[y][x] = "O"
                        score = self.minimax(False)
                        self.board[y][x] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == "":
                        self.board[y][x] = "X"
                        score = self.minimax(True)
                        self.board[y][x] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner_state(self, player):
        lines = self.board + [list(col) for col in zip(*self.board)] + [[self.board[i][i] for i in range(3)], [self.board[i][2-i] for i in range(3)]]
        return any(line[0] == player and all(cell == player for cell in line) for line in lines)

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.winner = None

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.bot and self.current_player == "O" and not self.winner:
                self.bot_move()

            self.draw_board()
            self.draw_ui()

            if self.winner:
                txt = self.font.render(f"Gewinner: {self.winner}", True, (0, 255, 0))
                self.screen.blit(txt, (100, self.HEIGHT - 110))

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    GameUI().main()
