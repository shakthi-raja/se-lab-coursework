import random
import pygame
from game.text_box import TextBox


class GameEngine:
    MAX_HISTORY = 5
    MAX_ATTEMPTS = 7

    # Colors shared by feedback text and history chips
    COLOR_LOW = (80, 160, 240)
    COLOR_HIGH = (240, 100, 80)
    COLOR_CORRECT = (80, 220, 90)
    COLOR_GAME_OVER = (230, 60, 60)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.low_bound = 1
        self.high_bound = 100
        self.history = []  # list of (guess, status); status in {"LOW", "HIGH", "CORRECT"}
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.input_box = TextBox(width // 2 - 110, 150, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 150, 100, 48)
        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):
        if self.game_won or self.game_over:
            return

        text = self.input_box.text.strip()

        # Validate before converting: must be non-empty and all digits
        if not text or not text.isdigit():
            self.feedback_msg = "Please enter a valid number first!"
            self.feedback_color = (240, 200, 60)  # warning yellow
            self.input_box.clear()
            return  # attempts and history are NOT touched

        guess = int(text)

        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            status = "LOW"
            self.low_bound = max(self.low_bound, guess + 1)
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = self.COLOR_LOW
        elif guess > self.secret_number:
            status = "HIGH"
            self.high_bound = min(self.high_bound, guess - 1)
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = self.COLOR_HIGH
        else:
            status = "CORRECT"
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = self.COLOR_CORRECT
            self.game_won = True

        # Out of attempts without a correct guess: the game is lost
        if not self.game_won and self.attempts >= self.MAX_ATTEMPTS:
            self.game_over = True
            self.feedback_msg = f"GAME OVER! The number was {self.secret_number}."
            self.feedback_color = self.COLOR_GAME_OVER

        # Record the guess, keeping only the latest MAX_HISTORY entries
        self.history.append((guess, status))
        self.history = self.history[-self.MAX_HISTORY:]

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.low_bound = 1
        self.high_bound = 100
        self.history = []
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def _render_history(self, screen, y):
        """Draw 'History:' followed by one chip per recent guess, centered on one row.

        Indicators are drawn as shapes (not font glyphs) because the default
        pygame font has no guaranteed support for the triangle characters.
        """
        chip_h, pad, gap, icon_w = 28, 10, 8, 12
        label_color = (180, 185, 195)

        label_surf = self.font_small.render("History:", True, label_color)

        if not self.history:
            empty_surf = self.font_small.render("no guesses yet", True, (110, 115, 125))
            total_w = label_surf.get_width() + 10 + empty_surf.get_width()
            x = (self.width - total_w) // 2
            screen.blit(label_surf, (x, y + (chip_h - label_surf.get_height()) // 2))
            screen.blit(empty_surf, (x + label_surf.get_width() + 10, y + (chip_h - empty_surf.get_height()) // 2))
            return

        colors = {"LOW": self.COLOR_LOW, "HIGH": self.COLOR_HIGH, "CORRECT": self.COLOR_CORRECT}

        # Pre-render numbers so the whole row can be centered
        chips = []
        for guess, status in self.history:
            color = colors[status]
            num_surf = self.font_small.render(str(guess), True, color)
            chip_w = pad + num_surf.get_width() + 6 + icon_w + pad
            chips.append((num_surf, chip_w, status, color))

        total_w = label_surf.get_width() + 10 + sum(c[1] for c in chips) + gap * (len(chips) - 1)
        x = (self.width - total_w) // 2

        screen.blit(label_surf, (x, y + (chip_h - label_surf.get_height()) // 2))
        x += label_surf.get_width() + 10

        for num_surf, chip_w, status, color in chips:
            chip_rect = pygame.Rect(x, y, chip_w, chip_h)
            pygame.draw.rect(screen, (44, 50, 62), chip_rect, border_radius=8)
            pygame.draw.rect(screen, color, chip_rect, width=2, border_radius=8)

            screen.blit(num_surf, (x + pad, y + (chip_h - num_surf.get_height()) // 2))

            cx = x + chip_w - pad - icon_w // 2
            cy = y + chip_h // 2
            if status == "LOW":  # up arrow: guess too low, go higher
                pygame.draw.polygon(screen, color, [(cx, cy - 5), (cx - 6, cy + 5), (cx + 6, cy + 5)])
            elif status == "HIGH":  # down arrow: guess too high, go lower
                pygame.draw.polygon(screen, color, [(cx, cy + 5), (cx - 6, cy - 5), (cx + 6, cy - 5)])
            else:  # correct: check mark
                pygame.draw.lines(screen, color, False, [(cx - 6, cy), (cx - 2, cy + 5), (cx + 6, cy - 5)], 3)

            x += chip_w + gap

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 35))

        attempts_surf = self.font_medium.render(f"Attempts: {self.attempts} / {self.MAX_ATTEMPTS}", True, (180, 185, 195))
        screen.blit(attempts_surf, (self.width // 2 - attempts_surf.get_width() // 2, 95))

        self.input_box.render(screen)
        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 235))

        # Dynamic range hint
        range_surf = self.font_medium.render(
            f"Current Possible Range: {self.low_bound} - {self.high_bound}", True, (150, 200, 255)
        )
        screen.blit(range_surf, (self.width // 2 - range_surf.get_width() // 2, 268))

        # Guess history chips (y=302 to 330)
        self._render_history(screen, 302)

        if self.game_won:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, 345))
        elif self.game_over:
            retry_surf = self.font_medium.render("Press [R] to Try Again", True, (255, 220, 80))
            screen.blit(retry_surf, (self.width // 2 - retry_surf.get_width() // 2, 345))