import pygame
import sys

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.width, self.height = 300, 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики")
        self.clock = pygame.time.Clock()
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def draw_board(self):
        self.screen.fill((0,0,0))

        for i in range(1, 3):
            pygame.draw.line(self.screen, (255, 255, 255), (0, i * self.height // 3), (self.width, i * self.height // 3), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (i * self.width // 3, 0), (i * self.width // 3, self.height), 2)

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    pygame.draw.line(self.screen, (255, 255, 255), (col * self.width // 3, row * self.height // 3),
                                     ((col + 1) * self.width // 3, (row + 1) * self.height // 3), 2)
                    pygame.draw.line(self.screen, (255, 255, 255), ((col + 1) * self.width // 3, row * self.height // 3),
                                     (col * self.width // 3, (row + 1) * self.height // 3), 2)
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       (col * self.width // 3 + self.width // 6, row * self.height // 3 + self.height // 6),
                                       self.width // 6, 2)

    def make_move(self, row, col):
        if not self.game_over and self.board[row][col] == '':
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
                self.game_over = True
            elif self.is_board_full():
                self.winner = 'Ничья'
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True

    def show_winner_screen(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Игрок {self.winner} выиграл!', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def show_draw_screen(self):
        font = pygame.font.Font(None, 36)
        text = font.render('Ничья!', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    x, y = pygame.mouse.get_pos()
                    col = x // (self.width // 3)
                    row = y // (self.height // 3)
                    self.make_move(row, col)

            self.draw_board()
            pygame.display.flip()

            if self.game_over:
                self.screen.fill((255, 255, 255))
                if self.winner != 'Ничья':
                    self.show_winner_screen()
                else:
                    self.show_draw_screen()
                pygame.time.delay(2000) 
                pygame.quit()
                sys.exit()

            self.clock.tick(30)

if __name__ == "__main__":
    game = TicTacToe()
    game.run_game()
