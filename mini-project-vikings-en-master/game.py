import pygame
import wargame
import random
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("⚔️🔥Vikings VS Saxons⚔️🔥")
clock = pygame.time.Clock()

# Game state flags
running = True
game_started = False
battle_started = False
winner_screen = None

# Custom class to send output to both the Python terminal and the in-game terminal
class DualOutput:
    def write(self, text):
        if text.strip():  # Ignore empty lines
            add_terminal_message(text.strip())  # Send to the in-game terminal
            sys.__stdout__.write(text)  # Send to the real Python terminal

    def flush(self):
        sys.__stdout__.flush()  # Ensure proper terminal flushing

# Redirect sys.stdout to send print statements to both outputs
sys.stdout = DualOutput()


# Terminal message storage
terminal_messages = ["Welcome to the game!", "Press the fight button to start."]
textbox_rect = pygame.Rect(50, 560, 500, 120)

def add_terminal_message(msg):
    """Adds a message to the in-game terminal and keeps only the last 6 messages."""
    terminal_messages.append(msg)
    if len(terminal_messages) > 6:  # Keep only the latest 6 messages
        terminal_messages.pop(0)


def draw_terminal_textbox(surface, rect, messages, font, text_color=(255, 255, 255),
                          bg_color=(0, 0, 0), border_color=(255, 255, 255)):
    """Draws a scrolling terminal textbox with stored messages."""
    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, border_color, rect, 2)
    line_height = font.get_linesize()
    for i, message in enumerate(terminal_messages[-4:]):  # Only show last 4 messages
        text_surf = font.render(message, True, text_color)
        surface.blit(text_surf, (rect.x + 5, rect.y + 5 + i * line_height))

# Load and scale images
def load_and_scale(image_path, size, convert_alpha=False):
    img = pygame.image.load(image_path)
    img = img.convert_alpha() if convert_alpha else img.convert()
    return pygame.transform.scale(img, size)

# Load assets
loading_screen = load_and_scale("loading_screen.png", (1280, 720))
winner_viking = load_and_scale("winner_viking.png", (1280, 720))
winner_saxon = load_and_scale("winner_saxon.png", (1280, 720))
fight_button_img = load_and_scale("fight_button.png", (250, 130), convert_alpha=True)
button_rect = fight_button_img.get_rect(center=(screen.get_width() // 2 + 300, screen.get_height() // 2 + 265))
battle_background = load_and_scale("battle_background1.png", (1280, 720))

# Fonts
font = pygame.font.Font("SourceCodePro-Bold.ttf", 20)

# Army status windows
viking_status_box = pygame.Rect(50, 50, 200, 100)
saxon_status_box = pygame.Rect(1030, 50, 200, 100)

# Get number of soldiers from the terminal before the game starts
try:
    num_soldiers = int(input("Enter the number of soldiers (1-50): "))
except ValueError:
    num_soldiers = 10  # default value if input is invalid
num_soldiers = max(1, min(num_soldiers, 50))
add_terminal_message(f"Selected {num_soldiers} soldiers.")

# To control battle round timing
last_round_time = 0

# Main Game Loop
while running:
    dt = clock.tick(30)  # Limit frame rate to 30 FPS
    screen.fill((0, 0, 0))  # Clear screen

    if winner_screen:  # Display winner screen when battle is over
        screen.blit(winner_screen, (0, 0))
    elif not game_started:
        # Show initial screen
        screen.blit(loading_screen, (0, 0))
        draw_terminal_textbox(screen, textbox_rect, terminal_messages, font)
        screen.blit(fight_button_img, button_rect.topleft)
    elif battle_started:
        screen.blit(battle_background, (0, 0))
        current_time = pygame.time.get_ticks()
        if current_time - last_round_time >= 1000:  # Process one round per second
            last_round_time = current_time
            result = wargame.process_battle_round()  # Process one battle round

            # print battle results
            print(result.get('viking', ''))
            print(result.get('saxon', ''))

        # Check for a winner
        battle_status = wargame.great_war.showStatus()
        if battle_status == "Vikings have won the war of the century!":
            winner_screen = winner_viking
            print("🏆 Vikings have won!")
        elif battle_status == "Saxons have fought for their lives and survive another day...":
            winner_screen = winner_saxon
            print("🛡️ Saxons have won!")


    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not game_started:
                game_started = True
                battle_started = True
                wargame.init_war(num_soldiers)  # initialize war without blocking
                last_round_time = pygame.time.get_ticks()

    draw_terminal_textbox(screen, textbox_rect, terminal_messages, font)  # redraw messages each frame
    pygame.display.flip()

pygame.quit()
