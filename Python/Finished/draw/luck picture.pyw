from turtle import *
from random import *

def main():
    turtle = Turtle()
    title('每日图像')
    
    turtle.speed(0)
    colors = ('red', 'orange', 'yellow', 'green', 'lightblue', 'blue', 'purple', 'black', 'white', 'pink', 'brown', 'gray')
    animations = ('turtle.color(colors[randint(0, len(colors)-2)])', 'bgcolor(colors[randint(0, len(colors)-2)])', 
                  'turtle.pensize(randint(1, 24))', 'turtle.forward(50)', 'turtle.backward(50)', 'turtle.circle(10, 180)', 
                  'turtle.left(30)', 'turtle.right(30)', 'Screen().setup(randint(50, 1200), randint(50, 1200), randint(0, 800), randint(0, 800))', 
                  'Screen().setup(randint(50, 1200), randint(50, 1200), randint(0, 800), randint(0, 800))')
    for i in range(2000):
        exec(animations[randint(0, len(animations)-1)])

    done()
main()