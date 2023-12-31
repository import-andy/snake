# Import the Turtle Graphics, random modules
import turtle
import random
import pygame

# Define program constants
WIDTH = 800
HEIGHT = 500
FOOD_SIZE = 20  # Pixels
EATING_DIST = 20
SCORE = 0
scores = []

offsets = {"up": (0, 20), "down": (0, -20), "right": (20, 0), "left": (-20, 0)}

# Play main theme sound
pygame.mixer.init()
pygame.mixer.music.load(f"sounds/master_of_puppets_8_bit.mp3")
pygame.mixer.music.set_volume(0.7)  # 0.7 of full track's volume
pygame.mixer.music.play(-1)  # repeats indefinitely


def display_score(self):
    global SCORE
    font = pygame.font.SysFont("Impact", bold=False, size=30)
    render = font.render(f"SCORE: {SCORE}", True, (255, 255, 255))
    self.surface.blit(render, (0, 0))

def play_sound(sound):
    sound = pygame.mixer.Sound(f"sounds/{sound}")
    pygame.mixer.Sound.play(sound)


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("right"), "Right")
    screen.onkey(lambda: set_snake_direction("left"), "Left")


def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # preventing going backwards to itself
            snake_direction = "up"
    elif direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = "right"
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = "left"


def game_loop():
    stamp.clearstamps()  # Removes existing snake
    stamp_head.clearstamps()  # Removes existing snake head

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check snake-snake & snake-wall collisions
    if new_head in snake or new_head[1] > HEIGHT / 2 or new_head[1] < -HEIGHT / 2 \
            or new_head[0] > WIDTH / 2 or new_head[0] < -WIDTH / 2:
        play_sound("explosion.wav")
        pygame.mixer.music.pause()
        reset()
    else:
        # Add new head to the snake body
        snake.append(new_head)

        # Check snake-food collision
        if not food_collision():
            snake.pop(0)  # Removing last segment as the snake moves
        else:
            play_sound("collect.wav")

        # Drawing the snake
        for segment in snake:
            stamp.goto(segment[0], segment[1])  # x & y coordinates
            stamp.stamp()

        # Drawing snake's head
        stamp_head.goto(snake[-1][0], snake[-1][1])  # x & y coordinates
        stamp_head.stamp()

        # Making record
        scores.append(SCORE)
        record = max(scores)

        # Refreshing the screen - to render updates
        screen.title(f"Snake. Score: {SCORE}. Record: {record}")
        screen.update()

        # Rinse and repeat
        turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_position, SCORE, DELAY
    if get_distance(snake[-1], food_position) < EATING_DIST:
        SCORE += 1

        # Levelups - increasing speed as score rises
        if SCORE == 5:
            DELAY -= 50
            play_sound('levelup.wav')
        elif SCORE == 15:
            DELAY -= 50
            play_sound('levelup.wav')
        elif SCORE > 15:
            DELAY -= 1

        # Creating new food position if previous was eaten
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False


def get_random_food_position():  # except snake position

    # Appending snake's x & y coordinates to respective lists
    snake_x = []
    snake_y = []
    for segment in snake:
        snake_x.append(segment[0])
    for segment in snake:
        snake_y.append(segment[1])

    # Appending screen's x & y coordinates to respective lists
    screen_x = []
    screen_y = []
    for coord in range(int(-WIDTH / 2 + FOOD_SIZE), int(WIDTH / 2 - FOOD_SIZE)):
        screen_x.append(coord)
    for coord in range(int(-HEIGHT / 2 + FOOD_SIZE), int(HEIGHT / 2 - FOOD_SIZE)):
        screen_y.append(coord)

    # Removing snake's coordinate's from screen's coordinates to get free spaces
    for coord in snake_x:
        for i in range(coord - 10, coord + 10):  # Removing +-10 pixels within snake
            if i in screen_x:
                screen_x.remove(i)
    for coord in snake_y:
        for i in range(coord - 10, coord + 10):  # Removing +-10 pixels within snake
            if i in screen_y:
                screen_y.remove(i)
    x = random.choice(screen_x)
    y = random.choice(screen_y)
    return x, y


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagoras' theorem
    return distance


def reset():
    global SCORE, DELAY, snake, snake_direction, food_position
    DELAY = 200  # Milliseconds
    SCORE = 0
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]  # x & y coordinates
    snake_direction = "up"
    food_position = get_random_food_position()
    food.goto(food_position)
    pygame.mixer.music.unpause()
    game_loop()


# Game window
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics window.
screen.bgcolor("black")
screen.tracer(0)  # Disables automatic animation

# Event handler (arrow key commands)
screen.listen()
bind_direction_keys()

# Snake
stamp = turtle.Turtle()
stamp.shape("circle")
stamp.penup()
stamp.color("green")  # Color of our future snake

# Snake head (other color)
stamp_head = turtle.Turtle()
stamp_head.shape("circle")
stamp_head.penup()
stamp_head.color("orange")  # Color of snake head

# Food
food = turtle.Turtle()
food.shape("circle")
food.color("orange")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# Set all in motion
reset()

# Finish
turtle.done()
