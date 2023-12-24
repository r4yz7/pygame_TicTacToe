import pygame
import sys

pygame.font.init() 

class TextInputBox:
    def __init__(self, x, y, width, height, font, color_inactive, color_active, symbol, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = color_inactive
        self.font = font
        self.symbol = symbol
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        font_symbol = pygame.font.Font(None, 36)
        text_symbol = font_symbol.render(self.symbol, True, (255, 255, 255)) 
        text_symbol_rect = text_symbol.get_rect(center=(self.rect.x - 40, self.rect.centery)) 
        screen.blit(text_symbol, text_symbol_rect)


class StartScreen:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Start Screen")
        self.clock = pygame.time.Clock()
        self.player_names = ['', '']
        self.previous_winner = self.read_previous_winner()
        self.text_input_boxes = [
            TextInputBox(self.width // 4, self.height // 3, 200, 32, pygame.font.Font(None, 32), (255, 255, 255), (200, 200, 200), 'X'),
            TextInputBox(self.width // 4, self.height // 3 + 50, 200, 32, pygame.font.Font(None, 32), (255, 255, 255), (200, 200, 200), 'O')
        ]
        self.start_button_rect = pygame.Rect(self.width // 4, self.height // 3 + 100, 200, 50)
        self.start_button_color = (0, 100, 0)
        self.start_button_active_color = (0, 80, 0) 
        self.start_button_color_current = self.start_button_color

    def read_previous_winner(self):
        try:
            with open("previous_winner.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return ''

    def write_previous_winner(self, winner):
        with open("previous_winner.txt", "w") as file:
            file.write(winner)

    
        pygame.display.flip()

    

    def draw_start_screen(self):
        self.screen.fill((0, 0, 0))

        if self.previous_winner:
            font = pygame.font.Font(None, 24)
            text_previous_winner = font.render(f'Прошлый победитель: {self.previous_winner}', True, (255, 255, 255))
            text_previous_winner_rect = text_previous_winner.get_rect(center=(self.width // 2, 20))
            self.screen.blit(text_previous_winner, text_previous_winner_rect)

        for i, box in enumerate(self.text_input_boxes):
            font_label = pygame.font.Font(None, 36)
            text_label = font_label.render(box.symbol, True, (255, 255, 255))
            text_label_rect = text_label.get_rect(center=(box.rect.x - 40, box.rect.centery))
            self.screen.blit(text_label, text_label_rect)

            box.draw(self.screen)

        pygame.draw.rect(self.screen, self.start_button_color_current, self.start_button_rect)
        font = pygame.font.Font(None, 36)
        text_start = font.render('Start', True, (255, 255, 255)) 
        text_start_rect = text_start.get_rect(center=(self.width // 2, self.start_button_rect.centery))
        self.screen.blit(text_start, text_start_rect)

        pygame.display.flip()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for box in self.text_input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.start_button_color_current = self.start_button_active_color
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.start_button_rect.collidepoint(event.pos):
                    self.start_button_color_current = self.start_button_color
                    self.player_names = [box.text for box in self.text_input_boxes]
                    return True

        return False

    def run_start_screen(self):
        while True:
            if self.handle_events():
                break

            for box in self.text_input_boxes:
                box.update()

            self.draw_start_screen()

            self.clock.tick(30)


class TicTacToe:
    def __init__(self, player_names, start_screen):
        pygame.init()
        self.width, self.height = 300, 300
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Крестики-нолики")
        self.clock = pygame.time.Clock()
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.player_names = player_names
        self.start_screen = start_screen

    def draw_board(self):
        self.screen.fill((0, 0, 0))

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
        text = font.render(f'{self.start_screen.player_names[0] if self.winner == "X" else self.start_screen.player_names[1]} выиграл!', True,
                           (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        self.start_screen.write_previous_winner(self.start_screen.player_names[0] if self.winner == "X" else self.start_screen.player_names[1])

    def show_draw_screen(self):
        font = pygame.font.Font(None, 36)
        text = font.render('Ничья!', True, (255, 255, 255))
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
                self.screen.fill((0, 0, 0))
                if self.winner != 'Ничья':
                    self.show_winner_screen()
                else:
                    self.show_draw_screen()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            self.clock.tick(30)

def main():
    start_screen = StartScreen(400, 300) 
    start_screen.run_start_screen()

    game = TicTacToe(start_screen.player_names, start_screen)
    game.run_game()

if __name__ == "__main__":
    main()