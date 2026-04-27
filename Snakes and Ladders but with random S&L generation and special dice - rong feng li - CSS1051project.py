import pygame, random, time, math
pygame.init()

###########################
###derive from razormist###
###########################

#https://www.sourcecodester.com/python/18541/snakes-and-ladders-game-using-pygame-python-source-code.html

print("------------------------------")
print("this is derive from razormist so credit goes to razormist")
print("------------------------------")
print("https://www.sourcecodester.com/python/18541/snakes-and-ladders-game-using-pygame-python-source-code.html")
print("------------------------------")

GOAL = 100  

#Generate randomly placed snakes and ladders
def generate_random_snakes_and_ladders():
    snakes_and_ladders = {}
    available_positions = set(range(1, GOAL))  # pos from 1 to 99

    while len(snakes_and_ladders) < 20:  # generate a combine of snakes and ladder to total of 20
        start = random.choice(list(available_positions))  # Random start pos
        end = random.choice(list(available_positions))    # Random end pos
        
        if abs(start - end) <= 20 and start != end:                     # The distance between start and end is within 20 spaces
            if start < end and end not in snakes_and_ladders.values():  # Ladder
                snakes_and_ladders[start] = end
                available_positions.remove(start)
                available_positions.remove(end)
            elif start > end and end not in snakes_and_ladders.values():  # Snake
                snakes_and_ladders[start] = end
                available_positions.remove(start)
                available_positions.remove(end)

    return snakes_and_ladders

SNAKES_AND_LADDERS = generate_random_snakes_and_ladders()

def roll_die():
    global CURRENT_ROLL_MODE
    
    if CURRENT_ROLL_MODE == '0-1':
        return random.randint(0, 1)  # Rolls between 0-1
    elif CURRENT_ROLL_MODE == '1-3':
        return random.randint(1, 3)  # Rolls between 1-3
    elif CURRENT_ROLL_MODE == '4-6':
        return random.randint(4, 6)  # Rolls between 4-6
    elif CURRENT_ROLL_MODE == '1-9':
        return random.randint(1, 9)  # Rolls between 1-9
    else:
        return random.randint(1, 6)  # Rolls between 1-6

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LADDER_COLOR = (0, 150, 0) 
SNAKE_COLOR = (200, 50, 50) 
RED = (200, 0, 0) 
GREEN = (0, 200, 0)
L_BLUE = (144, 183, 255)
PINK = (242, 217, 239)      
YELLOW = (225, 225, 0)  
L_GREEN = (216, 238, 223)
GOLD = (255, 215, 0)
DICE_BG_COLOR = (200, 200, 200) 
BUTTON_CLICKABLE = (50, 200, 50)
BUTTON_NOT_CLICKABLE = (200, 50, 50)
BUTTON_RESET = (40, 40, 40)
BUTTON_RESET_FLASH = (180, 180, 180)
POPUP_BG_COLOR = (240, 240, 240, 200)

# Game States
MENU = 0
PLAYING = 1
ROLL_MODES = ['0-1', '1-3', '4-6', '1-9', '1-6']
CURRENT_ROLL_MODE = '1-6'  # Default mode is 1-6
LIMITED_BUTTON_RECT = None

# Screen Dimensions and Board Constants
GRID_SIZE = 10
SQUARE_SIZE = 60
TOP_MARGIN = 80 
SIDE_MARGIN = 50
WIDTH = (GRID_SIZE * SQUARE_SIZE) + (2 * SIDE_MARGIN)
HEIGHT = (GRID_SIZE * SQUARE_SIZE) + TOP_MARGIN + SIDE_MARGIN
SCREEN_SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snakes and Ladders but with random S&L generation and special dice")
clock = pygame.time.Clock()

# Define Fonts
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 64)
font_huge = pygame.font.Font(None, 90)

# Dice
class Dice:
    def __init__(self):
        self.size = 60
        self.x = WIDTH - SIDE_MARGIN - self.size - 20  # position on screen
        self.y = 10
        self.is_rolling = False
        self.roll_result = 1
        self.final_roll = 1  # Store final roll separately
        self.roll_start_time = 0
        self.roll_duration = 0.5
        self.animation_frames = 0

    def start_roll(self):
        self.is_rolling = True
        self.roll_start_time = time.time()
        self.animation_frames = 0
        self.final_roll = roll_die()  # final roll result

    def update(self):
        if self.is_rolling:
            elapsed_time = time.time() - self.roll_start_time
            if elapsed_time < self.roll_duration:
                self.animation_frames += 1
                if self.animation_frames % 5 == 0:
                    self.roll_result = roll_die()  # animation value
            else:
                self.roll_result = self.final_roll  # ensure final value shown
                self.is_rolling = False
                return True
        return False

    def draw_face(self, surface, number): #Dice face draw
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, DICE_BG_COLOR, rect, 0, 5) 
        pygame.draw.rect(surface, BLACK, rect, 2, 5) 
        dot_radius = 5
        center = (self.x + self.size // 2, self.y + self.size // 2)
        q = self.size // 4
        dots = { #Face for 0-9
            0: [],
            1: [(0, 0)],
            2: [(-q, -q), (q, q)],
            3: [(-q, -q), (0, 0), (q, q)],
            4: [(-q, -q), (q, -q), (-q, q), (q, q)],
            5: [(-q, -q), (q, -q), (0, 0), (-q, q), (q, q)],
            6: [(-q, -q), (q, -q), (-q, 0), (q, 0), (-q, q), (q, q)],
            7: [(-q, -q), (q, -q), (-q, 0), (q, 0), (-q, q), (q, q), (0, 0)],  
            8: [(-q, -q), (q, -q), (-q, 0), (q, 0), (-q, q), (q, q), (0, q), (0, -q)],  
            9: [(-q, -q), (q, -q), (-q, 0), (q, 0), (-q, q), (q, q), (0, q), (0, -q), (0, 0)],  
    }
        if number in dots:
            for dx, dy in dots[number]:
                dot_pos = (center[0] + dx, center[1] + dy)
                pygame.draw.circle(surface, BLACK, dot_pos, dot_radius)

    def draw(self, surface):
        self.draw_face(surface, self.roll_result)

# Initialize/reset game

PLAYER_COLORS = [RED, GREEN]
PLAYER_OFFSETS = [-15, -5, 5, 15]

def initialize_game(num_players):# Change to always 2
    players = {}
    for i in range(num_players):
        player_name = f"Player {i + 1}"
        players[player_name] = {
            "pos": 1,
            "color": PLAYER_COLORS[i],
            "offset": PLAYER_OFFSETS[i]
        }
    return players

def reset_global_game_vars(): #Reset global
    global players, player_names, current_player_name, game_over, move_pending, dice #Reset variable 
    players = {}
    player_names = []
    current_player_name = ""
    game_over = False
    move_pending = False
    dice = Dice() # Re-initialize dice

#Dice button
SPECIAL = random.randint(2, 5)
SPECIAL_ONES_DIGIT = random.randint(0, 9)
print("special is", SPECIAL)
print("ones is", SPECIAL_ONES_DIGIT)

def draw_limited_roll_button(mouse_pos): #limited roll button (next to the dice)
    button_width = 100
    button_height = 40
    x = WIDTH - SIDE_MARGIN - 205
    y = 15
    rect = pygame.Rect(x, y, button_width, button_height)

    player_pos = players[current_player_name]['pos']

    IS_MULTIPLE = (player_pos % SPECIAL == 0)
    IS_ONES_DIGIT = (player_pos % 10 == SPECIAL_ONES_DIGIT)

    if player_pos == 100: #Forcing the goal to be always be gold color
        square_color = YELLOW
    elif IS_MULTIPLE != IS_ONES_DIGIT: # Determine if the player's current square is L_BLUE
        square_color = L_BLUE
    elif (player_pos - 1) // 10 % 2 == 0: #Alternation row for pink & light green (for aesthetic reason)
        square_color = PINK
    else:
        square_color = L_GREEN
    
    # Set button color based on square color
    if square_color == L_BLUE:
        color = BUTTON_CLICKABLE
    else:
        color = BUTTON_NOT_CLICKABLE

    pygame.draw.rect(screen, color, rect, 0, 8)
    
    # Change text based on the current roll mode
    if CURRENT_ROLL_MODE == '0-1':
        text_label = "Roll 0-1"
    elif CURRENT_ROLL_MODE == '1-3':
        text_label = "Roll 1-3"
    elif CURRENT_ROLL_MODE == '4-6':
        text_label = "Roll 4-6"
    elif CURRENT_ROLL_MODE == '1-9':
        text_label = "Roll 1-9"
    else:
        text_label = "Roll 1-6"
    
    text = font_small.render(text_label, True, WHITE)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    
    return rect

def draw_reset_button(mouse_pos): #Reset button
    global reset_flash_start_time
    button_width = 50
    button_height = 40
    x = WIDTH - SIDE_MARGIN - 280  
    y = 15
    rect = pygame.Rect(x, y, button_width, button_height)
    
    # Flash logic
    if reset_flash_start_time:
        elapsed = time.time() - reset_flash_start_time
        if elapsed < RESET_FLASH_DURATION:
            color = BUTTON_RESET_FLASH
        else:
            reset_flash_start_time = None
            color = BUTTON_RESET
    else:
        color = BUTTON_RESET

    pygame.draw.rect(screen, color, rect, 0, 8)
    
    text = font_small.render("Reset", True, WHITE)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)
    
    return rect

def reset_game(): #lots of global reset
    global players, player_names, current_player_name, game_over, move_pending, dice, CURRENT_ROLL_MODE, SPECIAL, SPECIAL_ONES_DIGIT, SNAKES_AND_LADDERS

    players = initialize_game(num_players)
    player_names = list(players.keys())
    current_player_name = player_names[0]
    game_over = False
    move_pending = False
    dice = Dice()
    CURRENT_ROLL_MODE = '1-6'
    SPECIAL = random.randint(2, 5)
    SPECIAL_ONES_DIGIT = random.randint(0, 9)
    SNAKES_AND_LADDERS = generate_random_snakes_and_ladders()
    print("------------------------------")
    print("Game reset")
    print("special is", SPECIAL)
    print("ones is", SPECIAL_ONES_DIGIT)

def get_square_coords(square_number): #For drawing board stuff
    if square_number < 1 or square_number > GOAL: return (0, 0)
    row = (square_number - 1) // GRID_SIZE
    col = (square_number - 1) % GRID_SIZE
    if row % 2 != 0: col = GRID_SIZE - 1 - col
    x = SIDE_MARGIN + (col * SQUARE_SIZE)
    y_start_board = TOP_MARGIN 
    y = y_start_board + ((GRID_SIZE - 1 - row) * SQUARE_SIZE)
    return (x, y)

def get_center_coords(square_number):
    x, y = get_square_coords(square_number)
    return (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)

def draw_board(): #Drawing the board
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            square_num_base = row * GRID_SIZE
            square_number = square_num_base + col + 1 if row % 2 == 0 else square_num_base + GRID_SIZE - col
            x, y = get_square_coords(square_number)
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
    
            if square_number == 100:
                fill_color = GOLD  # Force last square to be yellow
            else:
                IS_MULTIPLE = (square_number % SPECIAL == 0)
                IS_ONES_DIGIT = (square_number % 10 == SPECIAL_ONES_DIGIT)
                # Color based on odd/even, with multi 2-5 XOR ones digit (0-9) being light blue
                if IS_MULTIPLE != IS_ONES_DIGIT:  
                    fill_color = L_BLUE
                elif (square_number - 1) // 10 % 2 == 0:
                    fill_color = PINK   # 0-10, 21-30...
                else:
                    fill_color = L_GREEN # 11-20, 31-40...
                    
            pygame.draw.rect(screen, fill_color, rect)
            text = font_small.render(str(square_number), True, BLACK)
            screen.blit(text, (x + 5, y + 5))

def draw_arrow(surface, start_pos, end_pos, color, arrow_size=10, offset=0): #Draw line with an arrow
    start = (start_pos[0], start_pos[1] + offset)
    end = (end_pos[0], end_pos[1] + offset)
    pygame.draw.line(surface, color, start_pos, end_pos, 5)

    dx = end_pos[0] - start_pos[0]     # Calculate where to place the arrowhead
    dy = end_pos[1] - start_pos[1]
    angle = math.atan2(dy, dx)

    arrow_point1 = (end_pos[0] - arrow_size * math.cos(angle - math.pi / 6), end_pos[1] - arrow_size * math.sin(angle - math.pi / 6))
    arrow_point2 = (end_pos[0] - arrow_size * math.cos(angle + math.pi / 6), end_pos[1] - arrow_size * math.sin(angle + math.pi / 6))

    pygame.draw.line(surface, color, end_pos, arrow_point1, 5)
    pygame.draw.line(surface, color, end_pos, arrow_point2, 5)

    dot_radius = 6  # Dot radius size
    pygame.draw.circle(surface, BLACK, start, dot_radius)

def draw_jumps():
    for start_pos, end_pos in SNAKES_AND_LADDERS.items():
        if start_pos == 1:
            continue  # Not spawning on the first space
        start_center = get_center_coords(start_pos)
        end_center = get_center_coords(end_pos)
        color = LADDER_COLOR if end_pos > start_pos else SNAKE_COLOR
        draw_arrow(screen, start_center, end_center, color)

def draw_player(player_position, color, offset=0): # "player" itself 
    center_x, center_y = get_center_coords(player_position)
    center_x += offset
    pygame.draw.circle(screen, color, (center_x, center_y), 15)
 
def draw_game_over_popup(current_player_name): # Draws a centered pop-up panel for the game over screen

    # Height/width number
    POPUP_W = 400
    POPUP_H = 250
    popup_x = (WIDTH - POPUP_W) // 2
    popup_y = (HEIGHT - POPUP_H) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, POPUP_W, POPUP_H)

    # Transparent overlay
    overlay = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))

    # Main popup panel
    pygame.draw.rect(screen, POPUP_BG_COLOR, popup_rect, 0, 10)
    pygame.draw.rect(screen, BLACK, popup_rect, 3, 10)

    # Winner text
    winner_surface = font_huge.render("GAME OVER", True, RED)
    winner_rect = winner_surface.get_rect(center=(popup_x + POPUP_W // 2, popup_y + 50))
    screen.blit(winner_surface, winner_rect)

    player_surface = font_large.render(f"{current_player_name} WINS!", True, BLACK)
    player_rect = player_surface.get_rect(center=(popup_x + POPUP_W // 2, popup_y + 120))
    screen.blit(player_surface, player_rect)

    # Reset button
    button_width = 120
    button_height = 50
    button_x = popup_x + (POPUP_W - button_width) // 2
    button_y = popup_y + POPUP_H - button_height - 30
    reset_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    pygame.draw.rect(screen, BUTTON_RESET, reset_rect, 0, 8)
    text = font_medium.render("Reset", True, WHITE)
    text_rect = text.get_rect(center=reset_rect.center)
    screen.blit(text, text_rect)

    return reset_rect

def draw_hud(current_player_name, players, game_over=False, move_pending=False):
    # This logic only draws the standard HUD when the game is ACTIVE
    if not game_over:
        # Instructions / Game Status
        if move_pending:
            status_text = f"{current_player_name} Rolled {dice.roll_result}! Moving..."
            color = BLACK
        else:
            status_text = f"Press SPACE to Roll."
            color = BLACK
        
        text_surface = font_medium.render(status_text, True, color)
        screen.blit(text_surface, (SIDE_MARGIN, 10))
        
        # Player Turns and Positions
        x_pos = SIDE_MARGIN
        for name, data in players.items():
            pos_text = f"{name}: {data['pos']}"
            
            is_active_turn = (name == current_player_name and not dice.is_rolling and not move_pending and not game_over)
            
            if is_active_turn:
                pos_color = YELLOW
                text_rect = pygame.Rect(x_pos, 45, font_medium.size(pos_text)[0], font_medium.size(pos_text)[1])
                pygame.draw.rect(screen, BLACK, text_rect, 0)
            else:
                pos_color = BLACK

            pos_surface = font_medium.render(pos_text, True, pos_color)
            screen.blit(pos_surface, (x_pos, 45))
            x_pos += 150
            
    return None # Return None if not game over

# more variable
game_state = PLAYING
num_players = 2
players = initialize_game(num_players)
player_names = list(players.keys())
current_player_name = player_names[0]
game_over = False
dice = Dice()
move_pending = False
back_button_rect = None 
mouse_pos = (0, 0)
reset_button_rect = None
reset_flash_start_time = None  
RESET_FLASH_DURATION = 0.15     # in seconds

# Main loop
running = True
mouse_pos = (0, 0)

while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()  # Update mouse position every frame

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check Reset Button Click
            if reset_button_rect and reset_button_rect.collidepoint(event.pos):
                reset_flash_start_time = time.time()
                reset_game()

            if game_over and back_button_rect and back_button_rect.collidepoint(event.pos):
                reset_game()

            # Check Limited Roll Button Click
            if LIMITED_BUTTON_RECT and LIMITED_BUTTON_RECT.collidepoint(event.pos):
                player_pos = players[current_player_name]['pos']

                IS_MULTIPLE = (player_pos % SPECIAL == 0)
                IS_ONES_DIGIT = (player_pos % 10 == SPECIAL_ONES_DIGIT)

                if player_pos == 100:
                    square_color = YELLOW
                elif IS_MULTIPLE != IS_ONES_DIGIT:
                    square_color = L_BLUE
                elif (player_pos - 1) // 10 % 2 == 0:
                    square_color = PINK
                else:
                    square_color = L_GREEN
                
                if square_color == L_BLUE:
                    current_index = ROLL_MODES.index(CURRENT_ROLL_MODE)
                    CURRENT_ROLL_MODE = ROLL_MODES[(current_index + 1) % len(ROLL_MODES)]
                    print(f"Roll mode toggled to: {CURRENT_ROLL_MODE}")
                else:
                    print(f"Cannot toggle roll mode, not on a blue space.")

        if event.type == pygame.KEYDOWN and game_state == PLAYING and not game_over:
            if event.key == pygame.K_SPACE and not dice.is_rolling and not move_pending:
                dice.start_roll()
                move_pending = True

    # Game logic
    if game_state == PLAYING and not game_over:
        roll_complete = dice.update()
        if roll_complete and move_pending:
            # Move player
            roll_result = dice.final_roll  # Use final roll, not current animation
            player_data = players[current_player_name]
            new_pos = player_data["pos"] + roll_result
            if new_pos > GOAL: # Calculate bounce back
                excess = new_pos - GOAL
                new_pos = GOAL - excess  # Move backward the excess
            player_data["pos"] = SNAKES_AND_LADDERS.get(new_pos, new_pos) # Check win
            
            if player_data["pos"] == GOAL:
                game_over = True

            # Force roll mode back to '1-6' if not divisible by SPECIAL
            if player_data["pos"] % SPECIAL != 0:
                CURRENT_ROLL_MODE = '1-6'

            move_pending = False

            # Switch to next player
            if not game_over:
                current_index = player_names.index(current_player_name)
                current_player_name = player_names[(current_index + 1) % num_players]
                CURRENT_ROLL_MODE = '1-6'

    # Drawing
    screen.fill(WHITE)
    draw_board()
    draw_jumps()

    for name, data in players.items():
        draw_player(data["pos"], data["color"], data["offset"])

    # Draw HUD and Dice
    draw_hud(current_player_name, players, game_over, move_pending)
    dice.draw(screen)

    # Draw buttons and get their rects
    LIMITED_BUTTON_RECT = draw_limited_roll_button(mouse_pos)
    reset_button_rect = draw_reset_button(mouse_pos)

    # Game Over Popup
    if game_over:
        back_button_rect = draw_game_over_popup(current_player_name)
    else:
        back_button_rect = None

    pygame.display.flip()

pygame.quit()
