import turtle
import time
import random
import playsound as p
import math

def snake_game():
    delay = 0.1
    score = 0
    high_score = 0
    wn = turtle.Screen()
    wn.title("Snake Game")
    wn.bgcolor("black")
    wn.setup(width=800, height=750)
    wn.tracer(1)
    s = turtle.Turtle()
    s.speed(0)
    s.color('yellow')
    s.pensize(3)
    s.penup()
    s.goto(-310,310)
    s.pendown()
    for i in range(4):
        s.fd(620)
        s.rt(90)
    s.hideturtle()
    head = turtle.Turtle()
    head.shape("square")
    head.color("white")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.shapesize(0.5,0.5)
    food.color("red")
    food.penup()
    food.goto(0, 100)
    segments = []
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 320)
    pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

    def go_up():

        if head.direction != "down":
            head.direction = "up"

    def go_down():

        if head.direction != "up":
            head.direction = "down"

    def go_left():

        if head.direction != "right":
            head.direction = "left"

    def go_right():

        if head.direction != "left":
            head.direction = "right"

    def move():

        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)

        if head.direction == "down":
            y = head.ycor()
            head.sety(y - 20)

        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)

        if head.direction == "right":
            x = head.xcor()
            head.setx(x + 20)
    wn.listen()
    wn.onkey(go_up, "Up")
    wn.onkey(go_down, "Down")
    wn.onkey(go_left, "Left")
    wn.onkey(go_right, "Right")

    try:
        while True:
            wn.update()

            if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                score = 0
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
                delay = 0.1

            if head.distance(food) < 20:
                x = random.randint(-290, 290)
                y = random.randint(-290, 290)
                food.goto(x, y)
                colors = ['red','green','pink','purple','cyan','magenta','blue']
                new_segment = turtle.Turtle()
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color(random.choice(colors))
                new_segment.penup()
                segments.append(new_segment)
                delay -= 0.001
                score += 10

                if score > high_score:
                    high_score = score
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
            for index in range(len(segments) - 1, 0, -1):
                x = segments[index - 1].xcor()
                y = segments[index - 1].ycor()
                segments[index].goto(x, y)

            if len(segments) > 0:
                x = head.xcor()
                y = head.ycor()
                segments[0].goto(x, y)
            move()
            for segment in segments:

                if segment.distance(head) < 20:
                    time.sleep(1)
                    head.goto(0, 0)
                    head.direction = "stop"
                    for segment in segments:
                        segment.goto(1000, 1000)
                    segments.clear()
                    score = 0
                    pen.clear()
                    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
                    delay = 0.1
            current_time = time.time()
            pulse_speed = 6
            scale_factor = 0.5 + 0.2 * math.sin(current_time * pulse_speed)
            food.shapesize(scale_factor, scale_factor)
            time.sleep(delay)

    except turtle.Terminator:
        print("Game closed.")

    except Exception as e:
        print(f"Error: {e}")

    finally:

        try:
            wn.bye()

        except:
            pass
        turtle.TurtleScreen._RUNNING = False
