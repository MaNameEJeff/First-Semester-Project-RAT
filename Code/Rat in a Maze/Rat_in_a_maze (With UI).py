'''
#Project Name: Rat in a maze
#Last Updated: 23/02/2022 20:54 
#Last Updated by: Sarthak S Kumar

#Changelog:
    23/02/2022 23:12 Sarthak S Kumar
        # Functionality to change the color of squares visited previously
        # Canvas size updation in maze_ui
        # Code Refinement and Comments

    23/02/2022 20:54 Sarthak S Kumar
        # Added Functionality to check whether the user solution is correct or not
        # UI updation when user solves the maze, or gives up
        # Added Timer functionality
        # Code Refinement and Comments

    22/02/2022 21:47 Sarthak S Kumar
        # Added Functionality to let the user solve the maze manually
        # Comments and Decluttering

    21/02/2022 11:40 Sarthak S Kumar
        # Added the new try, prompt window (Exit Screen)
        # Fixed Username not displaying while using main()

    08/02/2022 20:40 Sarthak S Kumar
        # Added Welcome Screen, User Entry Screen, and Maze UI Screen
        # Show the randomly generated maze
        # Show the solution for the randomly generated maze
    
    08/02/2022 9:10 Vishal M Godi
        # Algorithm to solve Rat in a Maze using Backtracking
#Pending:
        # Resolve scaling issues
        # Bugs in the user_entry screen and maze_ui screens
'''
# MODULES
import numpy as np
import random
import time
import copy
import datetime
from tkinter import *
from tkinter import ttk
from ctypes import windll
from PIL import Image
from PIL import ImageTk
windll.shcore.SetProcessDpiAwareness(1)


def main():  # Program execution begins from here.
    """Tkinter Window Initialisation"""
    master = Tk()
    master.title("Rat in a Maze")
    master.geometry("1920x1080")
    master.configure(bg="#ffffff")

    """ Welcome Screen """
    intro = Frame(master)
    intro.place(anchor="nw")

    bg = PhotoImage(file=r"Code\Rat in a Maze\Assets\intro.png")
    canvas1 = Canvas(intro, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    intro.after(3000, intro.destroy)
    intro.wait_window(intro)

    """User Entry Screen"""
    user_entry = Frame(master, background="#ffffff")
    user_entry.pack()

    bg = PhotoImage(file=r"Code\Rat in a Maze\Assets\user_entry.png")
    canvas1 = Canvas(user_entry, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    Label(user_entry, text="Welcome", font=(r"HK Grotesk", 50), fg="#000000", bg="#ffffff").place(anchor='c', x=960, y=275)

    Label(user_entry, text="Your Name: ", font=(r"HK Grotesk", 25), fg="#000000", bg="#ffffff").place(anchor='e', x=800, y=450)

    sizebox = Entry(user_entry, font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff")
    sizebox.place(anchor='w', x=960, y=450)

    Label(user_entry, text="Maze Size: ", font=(r"HK Grotesk", 25), fg="#000000", bg="#ffffff").place(anchor='e', x=800, y=540)

    clicked = StringVar()
    clicked.set("Select one")

    gridsizes = ["5 x 5", "8 x 8", "10 x 10", "15 x 15", "20 x 20", "25 x 25"]
    drop = OptionMenu(user_entry, clicked, *gridsizes)
    drop.place(anchor='w', x=960, y=540)
    drop.config(font=(r'HK Grotesk', (20)), bg='#ffffff', fg="#000000")

    def movenext():
        global N, username, x
        username = sizebox.get()  # Maze Size Variable
        x = clicked.get().split()
        N = int(x[0])
        user_entry.after(1000, user_entry.destroy)

    submit = Button(user_entry, text="Submit", command=movenext, bg="#4d1354", font=(r'HK Grotesk', (25)), fg="white").place(anchor='c', x=960, y=800)

    user_entry.wait_window(user_entry)

    """ Maze Initialisation and Solution Generation (Backtracking)"""
    sol_maze = []
    while True:
        global maze
        maze = np.random.randint(2, size=(N, N))

        def MAZE(maze):
            global sol
            sol = copy.deepcopy(maze)

            if BACKTRACKING_ALGORITHM(maze, 0, 0, sol) == False:
                return False

            return True

        def BACKTRACKING_ALGORITHM(maze, x, y, sol):

            if x == N - 1 and y == N - 1:
                sol[x][y] = 5
                return True

            if check(maze, x, y) == True:
                sol[x][y] = 5

                if BACKTRACKING_ALGORITHM(maze, x + 1, y, sol) == True:
                    return True

                if BACKTRACKING_ALGORITHM(maze, x, y + 1, sol) == True:
                    return True

                sol[x][y] = 0
                return False

        def check(maze, x, y):
            if x >= 0 and x < N and y >= 0 and y < N and maze[x][y] == 1:
                return True

        if MAZE(maze) == False or maze[N - 1][N - 1] == 0 or maze[0][0] == 0:
            continue
        break

    """Maze UI"""
    squaresize = int(60 / N + 30)  # Dynamically changes with the maze size
    tile_color = " "
    rectbox_coordinates = [0, 0, squaresize, squaresize]
    forbidden = []  # To store co-ordinates of obstacle boxes in maze grid

    maze_UI = Frame(master, background="#fffceb")
    maze_UI.pack()

    bg2 = PhotoImage(file=r"Code\Rat in a Maze\Assets\maze_ui.png")
    canvas2 = Canvas(maze_UI, height=1080, width=2000)
    canvas2.pack()
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    headline = Label(maze_UI, text=f"Hello {username}\n Your {tile_color.join(x)} maze is here. Solve it", font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
    headline.place(anchor='center', x=1390, y=375)

    # Canvas to display Maze to be solved
    question_canvas = Canvas(maze_UI, height=(N * squaresize + (N)), width=(N * squaresize + (N)), bg='#ffffff')
    question_canvas.place(anchor='center', x=500, y=512)

    # Drawing the maze to be solved in the question canvas
    for i in maze:
        for j in i:
            if j == 1:
                color = "white"
            else:
                color = "black"
                forbidden.append((rectbox_coordinates[0], rectbox_coordinates[1], rectbox_coordinates[2], rectbox_coordinates[3]))

            square = question_canvas.create_rectangle(rectbox_coordinates[0], rectbox_coordinates[1], rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=0)
            rectbox_coordinates[0] += squaresize
            rectbox_coordinates[2] += squaresize

        rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
        rectbox_coordinates[1] += squaresize
        rectbox_coordinates[3] += squaresize

    # Rat Object to Traverse through the maze
    rat = question_canvas.create_oval(0, 0, squaresize, squaresize, fill="green", width=0)

    endpoint = question_canvas.create_rectangle(squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N, fill="#660033")

    use = Label(maze_UI, text="Use", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff")
    use.place(anchor='e', x=1235, y=540)

    img = Image.open(r"Code\Rat in a Maze\Assets\arrowkeys.png")
    img = img.resize((100, 100), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(img)
    arrow = Canvas(maze_UI, width=100, height=100, bg="white", bd=0, highlightthickness=0, relief='ridge')
    arrow.place(x=1360, y=540, anchor='e')
    arrow.create_image(0, 0, image=photoImg, anchor='nw')

    labe = Label(maze_UI, text="to move the rat", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff")
    labe.place(anchor='w', x=1385, y=540)

    visited_squares = []  # List to stores the squares in which the rat has been before

    def pathsquare(coord):  # To change color of the path traversed accordingly
        if [coord[0], coord[1], coord[2], coord[3]] not in ls:
            ls.append([coord[0], coord[1], coord[2], coord[3]])
            question_canvas.create_rectangle(coord[0], coord[1], coord[2], coord[3], fill="purple", width=0)
            question_canvas.tag_raise(rat)
        else:
            question_canvas.create_rectangle(coord[0], coord[1], coord[2], coord[3], fill="orange", width=0)
            question_canvas.tag_raise(rat)

    def nextstep():  # When Next button is clicked
        Next = Tk()
        Next.geometry("1500x300")
        Next.title("Solving the Maze")
        Next.configure(bg="#ffffff", border=1)
        message = Label(Next, text=f"Wanna solve another maze?", font=(
            r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
        message.place(anchor='center', x=750, y=100)

        def restart():  # Restart the program
            Next.destroy()
            master.destroy()
            main()

        yes = Button(Next, text="Yeah", command=restart, bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        yes.place(anchor='e', x=750, y=200)
        no = Button(Next, text="Nah", command=exit, bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        no.place(anchor='w', x=850, y=200)

    def user_solved():  # When user manages to solve the maze

        use.destroy()
        arrow.destroy()
        labe.destroy()
        headline.destroy()
        comp_solve.destroy()

        # To check the number of seconds elapsed after game started
        endtime = datetime.datetime.now()
        td = endtime - starttime
        elapsed = td.total_seconds()
        successmessages = ["Yay! You made it!"]
        Label(maze_UI, text="🎉 Congratulations 🎉", font=(r"HK Grotesk", 40), fg="#000000", bg="#ffffff").place(anchor='e', x=1720, y=375)
        Label(maze_UI, text=random.choice(successmessages), font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff").place(anchor='center', x=1390, y=455)
        Label(maze_UI, text=f"You solved the maze in {round(elapsed, 2)} seconds", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff").place(anchor='center', x=1390, y=520)

        # Displays Confirmation Window on clicking next
        nextb = Button(maze_UI, text="Next", command=nextstep,
                       bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        nextb.place(anchor='center', x=1390, y=600)

    # Keybind Events
    def left(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[0] > 0:
            x = -squaresize
            y = 0
            if (rat_xy[0] + x, rat_xy[1], rat_xy[2] + x, rat_xy[3]) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    def right(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[2] <= N * squaresize - 1:
            x = squaresize
            y = 0
            if (rat_xy[0] + x, rat_xy[1], rat_xy[2] + x, rat_xy[3]) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    def up(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[1] > 0:
            x = 0
            y = -squaresize
            if (rat_xy[0], rat_xy[1] + y, rat_xy[2], rat_xy[3] + y) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    def down(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[3] <= N * squaresize - 1:
            x = 0
            y = squaresize
            if (rat_xy[0], rat_xy[1] + y, rat_xy[2], rat_xy[3] + y) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    master.bind("<Left>", left)
    master.bind("<Right>", right)
    master.bind("<Up>", up)
    master.bind("<Down>", down)

    global starttime, endtime
    starttime = datetime.datetime.now()

    # When user gives up on solving the maze
    def solve():
        question_canvas.destroy()

        # To display the maze solution
        solution_canvas = Canvas(maze_UI, height=(N * squaresize + (N)), width=(N * squaresize + (N)), bg='#ffffff')
        solution_canvas.place(anchor='center', x=500, y=512)

        rectbox_coordinates = [0, 0, squaresize, squaresize]
        for i in sol:
            for j in i:
                if j == 5:
                    color = "green"
                elif j == 1:
                    color = "white"
                else:
                    color = "black"
                square = solution_canvas.create_rectangle(
                    rectbox_coordinates[0], rectbox_coordinates[1], rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=0)
                rectbox_coordinates[0] += squaresize
                rectbox_coordinates[2] += squaresize

            rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
            rectbox_coordinates[1] += squaresize
            rectbox_coordinates[3] += squaresize

        use.destroy()
        arrow.destroy()
        labe.destroy()
        headline.destroy()
        comp_solve.destroy()

        failmessages = ["You gave up so quick!"]
        Label(maze_UI, text=random.choice(failmessages), font=(r"HK Grotesk", 40), fg="#000000", bg="#ffffff").place(anchor='center', x=1390, y=375)
        Label(maze_UI, text=f"Better luck next time!", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff").place(anchor='center', x=1390, y=475)

        # Displays Confirmation Window on clicking next
        nextb = Button(maze_UI, text="Next", command=nextstep,
                       bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        nextb.place(anchor='center', x=1390, y=600)

    # Button to let computer display the solution
    comp_solve = Button(maze_UI, text="Give Up!", command=solve,
                        bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
    comp_solve.place(anchor='center', x=1390, y=800)

    mainloop()


if __name__ == "__main__":
    main()
