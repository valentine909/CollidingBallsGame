import random
import tkinter

# CONSTANTS
WIDTH = 640
HEIGHT = 480
BG_COLOR = 'white'
COLORS = ['grey', 'green', 'yellow', 'pink']
BAD_COLOR = "red"
MAIN_COLOR = "blue"
BAD_BALLS_RATIO = 0.25
NUM_OF_BALLS = 20  # minimum 4


# balls class
class Ball:
    def __init__(self, x, y, r, color, dx=0, dy=0):
        if x - r < 0:
            self.x = r
        elif x + r > WIDTH:
            self.x = WIDTH - r
        else:
            self.x = x
        if y - r < 0:
            self.y = r
        elif y + r > HEIGHT:
            self.y = HEIGHT - r
        else:
            self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy

    def draw(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color,
                           outline=self.color)

    def hide(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=BG_COLOR,
                           outline=BG_COLOR)

    def is_colliding(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y + self.dy - ball.y)
        return (a * a + b * b) ** 0.5 <= self.r + ball.r

    def move(self):
        # colliding with walls
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= 0):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= 0):
            self.dy = -self.dy
        # colliding with balls
        for ball in balls:
            if self.is_colliding(ball):
                if ball.color == BAD_COLOR:
                    self.dx = 0
                    self.dy = 0
                else:
                    ball.hide()
                    balls.remove(ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


#  create ball
def create_random_ball():
    r_local = random.randint(15, 30)
    ball = Ball(random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                r_local,
                random.choice(COLORS))
    return ball


# create list of balls
def create_list_of_balls(number):
    lst = [create_random_ball()]
    while len(lst) < number:
        next_ball = create_random_ball()
        if not check_balls(next_ball, lst):
            next_ball.draw()
            lst.append(next_ball)
    for i in range(0, max(1, int(BAD_BALLS_RATIO * NUM_OF_BALLS))):
        lst[i].color = BAD_COLOR
        lst[i].draw()
    return lst


#  check balls overlapping
def is_overlapping(big_ball, small_ball):
    small_ball_vertices = [(small_ball.x - small_ball.r, small_ball.y - small_ball.r),
                           (small_ball.x - small_ball.r, small_ball.y + small_ball.r),
                           (small_ball.x + small_ball.r, small_ball.y - small_ball.r),
                           (small_ball.x + small_ball.r, small_ball.y + small_ball.r)]
    for i in small_ball_vertices:
        if (big_ball.x - big_ball.r <= i[0]) and (i[0] <= big_ball.x + big_ball.r) \
                and (big_ball.y - big_ball.r <= i[1]) and (i[1] <= big_ball.y + big_ball.r):
            return True
    return False


def check_balls(ball, lst_of_balls):
    flag = False
    for i in lst_of_balls:
        if ball.r > i.r:
            flag = is_overlapping(ball, i)
        else:
            flag = is_overlapping(i, ball)
        if flag:
            return flag
    return flag


# main circle game
def main():
    if "main_ball" in globals():
        main_ball.move()
        if len(balls) - int(BAD_BALLS_RATIO * NUM_OF_BALLS) == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="YOU WIN!", font="Arial, 20", fill=MAIN_COLOR)
            main_ball.dx = 0
            main_ball.dy = 0
            main_ball.color = BG_COLOR
        elif main_ball.dx == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="YOU LOSE!", font="Arial, 20", fill=BAD_COLOR)
    root.after(10, main)


# mouse events
def mouse_click(event):
    global main_ball
    if event.num == 1:
        if 'main_ball' not in globals():
            main_ball = Ball(event.x, event.y, 30, MAIN_COLOR, 1, 1)
            main_ball.draw()
        else:  # turn left
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 3:  # turn right
        if main_ball.dx * main_ball.dy > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy


root = tkinter.Tk()
root.title("Colliding Balls")
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-2>', mouse_click, "+")
canvas.bind('<Button-3>', mouse_click, "+")
balls = create_list_of_balls(max(4, NUM_OF_BALLS))
main()
root.mainloop()
