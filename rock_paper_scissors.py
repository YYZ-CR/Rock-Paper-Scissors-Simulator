import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Simulator")

# Colors
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Load custom images for rock, paper, and scissors
rock_img = pygame.image.load("rock.png").convert_alpha()  # Custom rock image
paper_img = pygame.image.load("paper.png").convert_alpha()  # Custom paper image
scissors_img = pygame.image.load("scissors.png").convert_alpha()  # Custom scissors image

# Object classes
class Object:
    def __init__(self, object_type, x, y):
        self.type = object_type
        self.x = x
        self.y = y
        self.size = 50  # Size of object
        self.dx = random.choice([-1, 1]) * random.uniform(0.5, 2)  # Random x-direction movement
        self.dy = random.choice([-1, 1]) * random.uniform(0.5, 2)  # Random y-direction movement
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
            self.dx *= -1
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.size:
            self.dy *= -1

    def draw(self):
        if self.type == 'rock':
            screen.blit(rock_img, (int(self.x), int(self.y)))
        elif self.type == 'paper':
            screen.blit(paper_img, (int(self.x), int(self.y)))
        elif self.type == 'scissors':
            screen.blit(scissors_img, (int(self.x), int(self.y)))

# Function to spawn objects
def spawn_object(object_type):
    x = random.randint(50, SCREEN_WIDTH - 50)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    return Object(object_type, x, y)

# Function to clear all objects
def clear_objects():
    return []

# Button class
class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 20)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Slider class for total object count
class Slider:
    def __init__(self, x, y, min_value, max_value, value):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 10
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.slider_rect = pygame.Rect(self.x + int(self.value * (self.width / self.max_value)), self.y - 5, 10, 20)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.slider_rect)

    def get_value(self, pos):
        if self.rect.collidepoint(pos):
            relative_x = pos[0] - self.x
            self.value = (relative_x / self.width) * (self.max_value - self.min_value)
            self.slider_rect.x = self.x + int(self.value * (self.width / self.max_value))
        return self.value

# Function to handle collisions and apply the rules
def handle_collisions(objects):
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):  # Check every pair of objects
            obj1 = objects[i]
            obj2 = objects[j]
            
            # Calculate the distance between two objects
            distance = ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5
            
            if distance < obj1.size:  # Collision happens if they are close enough
                # Apply Rock-Paper-Scissors rules
                if obj1.type == 'rock' and obj2.type == 'scissors':
                    obj2.type = 'rock'  # Rock beats Scissors
                elif obj1.type == 'scissors' and obj2.type == 'paper':
                    obj2.type = 'scissors'  # Scissors beats Paper
                elif obj1.type == 'paper' and obj2.type == 'rock':
                    obj2.type = 'paper'  # Paper beats Rock
                elif obj2.type == 'rock' and obj1.type == 'scissors':
                    obj1.type = 'rock'  # Rock beats Scissors
                elif obj2.type == 'scissors' and obj1.type == 'paper':
                    obj1.type = 'scissors'  # Scissors beats Paper
                elif obj2.type == 'paper' and obj1.type == 'rock':
                    obj1.type = 'paper'  # Paper beats Rock

# Main loop
def main():
    clock = pygame.time.Clock()
    objects = []
    paused = False
    show_ui = True
    running = True
    speed = 1  # Default speed value
    max_objects = 20  # Max objects controlled by slider

    # Buttons for spawning objects, reset, and pause/play
    rock_button = Button(700, 20, 80, 40, WHITE, "Rock", BLACK)
    paper_button = Button(700, 80, 80, 40, WHITE, "Paper", BLACK)
    scissors_button = Button(700, 140, 80, 40, WHITE, "Scissors", BLACK)
    clear_button = Button(700, 200, 80, 40, WHITE, "Clear", BLACK)

    # Buttons for speed control and pause/play
    slower_button = Button(360, 20, 40, 40, WHITE, "-", BLACK)
    pause_button = Button(410, 20, 40, 40, WHITE, "||", BLACK)  # Pause/Play toggle
    faster_button = Button(460, 20, 40, 40, WHITE, "+", BLACK)

    # Slider for total object count
    object_slider = Slider(20, 550, 1, 100, max_objects)

    while running:
        screen.fill(GRAY)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if show_ui:
                    if rock_button.is_clicked(mouse_pos):
                        if len(objects) < max_objects:
                            objects.append(spawn_object('rock'))
                    elif paper_button.is_clicked(mouse_pos):
                        if len(objects) < max_objects:
                            objects.append(spawn_object('paper'))
                    elif scissors_button.is_clicked(mouse_pos):
                        if len(objects) < max_objects:
                            objects.append(spawn_object('scissors'))
                    elif clear_button.is_clicked(mouse_pos):
                        objects = clear_objects()  # Clear all objects
                    elif pause_button.is_clicked(mouse_pos):
                        paused = not paused  # Toggle pause
                        pause_button.text = "▶" if paused else "||"
                    elif slower_button.is_clicked(mouse_pos):
                        speed = max(1, speed - 1)  # Decrease speed
                    elif faster_button.is_clicked(mouse_pos):
                        speed = min(10, speed + 1)  # Increase speed
                    max_objects = int(object_slider.get_value(mouse_pos))  # Adjust max objects with slider

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space bar to toggle UI
                    show_ui = not show_ui
                else:
                    show_ui = True

        # Adjust the number of objects to match the
        # Adjust the number of objects to match the slider value for total objects
        while len(objects) > max_objects:
            objects.pop()

        # Move and draw objects if not paused
        for obj in objects:
            if not paused:
                obj.move()
            obj.draw()  # Always draw objects, even when paused

        # Handle collisions
        handle_collisions(objects)

        # Draw UI elements if they are visible
        if show_ui:
            # Display count of objects
            counts = {'rock': 0, 'paper': 0, 'scissors': 0}
            for obj in objects:
                counts[obj.type] += 1
            count_text = small_font.render(f"Rocks: {counts['rock']}  Papers: {counts['paper']}  Scissors: {counts['scissors']}", True, WHITE)
            screen.blit(count_text, (20, 20))

            # Draw buttons and speed controls
            rock_button.draw()
            paper_button.draw()
            scissors_button.draw()
            clear_button.draw()
            slower_button.draw()
            pause_button.draw()
            faster_button.draw()

            # Draw slider for total object count
            object_slider.draw()

            # Display total object count
            total_object_text = small_font.render(f"Total Objects: {len(objects)}", True, WHITE)
            screen.blit(total_object_text, (20, 520))

            # Display the speed value
            speed_text = small_font.render(f"Speed: {int(speed)}", True, WHITE)
            screen.blit(speed_text, (510, 30))

        # Update display
        pygame.display.update()
        clock.tick(30*speed)

if __name__ == '__main__':
    main()