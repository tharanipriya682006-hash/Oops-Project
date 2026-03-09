import tkinter as tk
import random

# INITIAL SETUP
window = tk.Tk()
window.title("Brick Breaker Game")
window.resizable(False, False)

canvas_width = 500
canvas_height = 450

canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# SCORE
score = 0
score_text = canvas.create_text(60, 20, text="Score: 0",
                                fill="white", font=("Arial", 14))

# GAME VARIABLES
ball = None
paddle = None
bricks = []
game_running = False


# -------------------------
# CREATE PADDLE
# -------------------------
def create_paddle():
    return canvas.create_rectangle(210, 400, 290, 415, fill="white")


# -------------------------
# CREATE BALL
# -------------------------
def create_ball():
    return canvas.create_oval(240, 360, 260, 380, fill="red")


ball_dx = 3
ball_dy = -3


# -------------------------
# KEYBOARD CONTROLS
# -------------------------
def move_left(event):
    if game_running:
        canvas.move(paddle, -20, 0)


def move_right(event):
    if game_running:
        canvas.move(paddle, 20, 0)


window.bind("<Left>", move_left)
window.bind("<Right>", move_right)


# -------------------------
# CREATE BRICKS
# -------------------------
def create_bricks():
    global bricks
    bricks.clear()

    colors = ["cyan", "orange", "green"]

    brick_width = 60
    brick_height = 20

    for row in range(3):
        for col in range(7):
            x1 = 20 + col * (brick_width + 10)
            y1 = 60 + row * (brick_height + 10)
            x2 = x1 + brick_width
            y2 = y1 + brick_height

            brick = canvas.create_rectangle(x1, y1, x2, y2,
                                            fill=colors[row % len(colors)])
            bricks.append(brick)


# -------------------------
# GAME LOOP
# -------------------------
def move_ball():
    global ball_dx, ball_dy, score, game_running

    if not game_running:
        return

    canvas.move(ball, ball_dx, ball_dy)
    x1, y1, x2, y2 = canvas.coords(ball)

    # WALL COLLISION
    if x1 <= 0 or x2 >= canvas_width:
        ball_dx = -ball_dx
    if y1 <= 0:
        ball_dy = -ball_dy

    # PADDLE COLLISION
    paddle_pos = canvas.coords(paddle)
    if y2 >= paddle_pos[1] and y1 <= paddle_pos[3]:
        if x2 >= paddle_pos[0] and x1 <= paddle_pos[2]:
            ball_dy = -ball_dy

    # BRICK COLLISION
    for brick in bricks:
        bx1, by1, bx2, by2 = canvas.coords(brick)
        if x2 >= bx1 and x1 <= bx2 and y2 >= by1 and y1 <= by2:
            canvas.delete(brick)
            bricks.remove(brick)
            ball_dy = -ball_dy
            score += 5
            canvas.itemconfig(score_text, text=f"Score: {score}")
            break

    # GAME WIN
    if len(bricks) == 0:
        canvas.create_text(canvas_width / 2, canvas_height / 2,
                           text="YOU WIN!",
                           fill="yellow", font=("Arial", 26, "bold"))
        game_running = False
        return

    # GAME OVER
    if y2 >= canvas_height:
        canvas.create_text(canvas_width / 2, canvas_height / 2,
                           text="GAME OVER",
                           fill="red", font=("Arial", 26, "bold"))
        game_running = False
        return

    window.after(10, move_ball)


# -------------------------
# START GAME
# -------------------------
def start_game():
    global paddle, ball, game_running, score

    canvas.delete("all")

    score = 0

    # recreate score display
    global score_text
    score_text = canvas.create_text(60, 20, text="Score: 0",
                                    fill="white", font=("Arial", 14))

    paddle = create_paddle()
    ball = create_ball()
    create_bricks()

    game_running = True
    move_ball()


# -------------------------
# BUTTONS
# -------------------------
start_button = tk.Button(window, text="START GAME",
                         font=("Arial", 14, "bold"),
                         bg="green", fg="white",
                         command=start_game)
start_button.pack(pady=10)


restart_button = tk.Button(window, text="RESTART",
                           font=("Arial", 14, "bold"),
                           bg="blue", fg="white",
                           command=start_game)
restart_button.pack(pady=5)

# -------------------------
window.mainloop()
