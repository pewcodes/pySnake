# "ARROWKEYS": Navigate | "SpaceBar": Pause/Resume | "Esc": Exit
import curses
import random
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                                    # Initialize values
score = 0

snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
food = []                                                          # Random first food co-ordinates
while food == []:
    food = [randint(1, 15), randint(1, 58)]
    if food in snake: 
        food = []
win.addch(food[0], food[1], "*")                                   # Displays food

while key != 27:                                                   # While not ESC Key
    win.border(0)
    win.addstr(0, 46, " Score : " + str(score) + " ")              # Displays "Score"
    win.addstr(0, 24, " S N A K E ")                               # Displays "S N A K E"
    win.timeout(150 - (len(snake)//10)%120)                        # Adjusts Snake's speed with increased length
    
    prevKey = key                                                  
    event = win.getch()
    key = key if event == -1 else event 

    if key == ord(" "):                                            # If SPACEBAR, game is Paused, SPACEBAR again to Resume
        key = -1                                   
        while key != ord(" "):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If invalid key pressed, reverts back to previous key
        key = prevKey

    # Determine new coordinates of Snake's head
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake crosses boundaries, enter from opposite
    if snake[0][0] == 0: snake[0][0] = 15
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 16: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

    # If snake crosses boundaries, End Game
    # if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: 
    #     break
   
    if snake[0] in snake[1:]:                                       # If snake eats itself
        break

    elif snake[0] == food:                                          # If snake eats food
        food = []
        score += 1
        while food == []:
            food = [randint(1, 15), randint(1, 58)]                 # Randomize next food's coordinates
            if food in snake: 
                food = []
        win.addch(food[0], food[1], "*")
    else:    
        tail = snake.pop()                                          # If food not eaten, Snake's length decrease
        win.addch(tail[0], tail[1], " ")
    
    win.addch(snake[0][0], snake[0][1], "O")
    
curses.endwin()
print("\nScore: " + str(score))