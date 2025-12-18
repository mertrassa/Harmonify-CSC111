"""
The visual part of the program
"""
import tkinter as tk
from tkinter import messagebox
from graph_functions import _Vertex
from graph_visualization import *
from graph_functions import *
import platform


def button1_clicked() -> None:
    """
    After pressing the song list button, this function opens a pdf file including song list with their ids
    """
    if platform.system() == "Darwin":  # macOS
        import subprocess
        subprocess.run(["open", "mypdf.pdf"])

    elif platform.system() == "Windows":  # Windows
        import os
        os.startfile("mypdf.pdf")

    elif platform.system() == "Linux":  # Linux
        import subprocess
        subprocess.call(["xdg-open", "mypdf.pdf"])


def button2_clicked() -> None:
    """
    After pressing the visualize graph button, this function visualizes the graph using networkx
    """
    visualize_graph(load_review_graph('all_user_data_200_songs.csv', 'songs_by_popularity.csv'))


def move_entries(k=0) -> None:
    """
    After pressing the launch button, this function moves all entries and the button to the left
    """
    if mybool[0]:
        if k < 10:
            for element in entries + labels + buttons:
                element_x = int(element.place_info()['x'])
                element.place_configure(x=element_x - 20)
            gui.after(10, move_entries, k + 1)
        elif k == 10:
            mybool[0] = False
            place_elements()


def match_values() -> None:
    """
    Inserts relative values from entries to values list
    """
    for j in range(7):
        given_entries[j] = entries[j].get()


def compute_algorithm() -> None:
    """
    Computes all background work and places all values of matched person
    """
    g = load_review_graph('all_user_data_200_songs.csv', 'songs_by_popularity.csv')
    new_user = _Vertex(given_entries[0], [given_entries[0]], 'user')
    g.add_vertex(new_user.key, new_user.item, new_user.kind)

    for n in given_entries[1:6]:
        g.add_edge(new_user.key, str(n))

    output = g.compatible_user_rec_songs(new_user.key, given_entries[6], duration[0])

    new_labels[0].config(text=output[0][0])  # Username
    new_labels[1].config(text=output[0][1])  # Name
    new_labels[2].config(text=output[0][2])  # Age
    new_labels[3].config(text=output[0][3])  # Province
    new_labels[4].config(text=',\n'.join(output[1][0]))  # Songs in common
    new_labels[5].config(text=',\n'.join(output[1][1]))  # Recommended songs
    new_labels[6].config(text=str(round((output[2][0] * 100) / 30)) + " %")  # Highest Macht Score

    new_labels[0].place(x=450, y=100)
    new_labels[1].place(x=450, y=80)
    new_labels[2].place(x=450, y=120)
    new_labels[3].place(x=450, y=140)
    new_labels[4].place(x=420, y=220)
    new_labels[5].place(x=420, y=380)
    new_labels[6].place(x=450, y=160)


def button3_clicked() -> None:
    """
    Combines two functions to work when button gets clicked
    """
    match_values()
    if any(h == "" for h in given_entries):
        messagebox.showerror("Empty Entry", "Do not leave any empty entry!")
    elif not (all(k.isdigit() for k in given_entries[1:6]) and given_entries[0].isalnum()):
        messagebox.showerror("Invalid Input", "Given invalid input in some entry!")
    elif given_entries[6] not in ['soul', 'chill', 'alt-rock', 'folk', 'reggae', 'club', 'edm', 'sleep', 'german',
                                  'rock', 'hip-hop', 'latino', 'piano', 'j-pop', 'emo', 'indie-pop', 'country', 'k-pop',
                                  'dance', 'electro', 'garage', 'indie', 'latin', 'synth-pop', 'funk', 'ambient',
                                  'hard-rock', 'british', 'pop', 'alternative', 'indian', 'singer-songwriter', 'anime']:
        messagebox.showerror("Invalid Genre", "Choose one of the genres in Info->Genre")
    elif len(set(given_entries[1:6])) != len(given_entries[1:6]):
        messagebox.showerror("Same Type", "Do not input same songs more than once!")
    elif not (all((int(g) < 201) and (int(g) > 0) for g in given_entries[1:6])):
        messagebox.showerror("Invalid Song ID", "Song ID must be between 1 and 200, inclusive!")
    elif duration[0] == "":
        messagebox.showerror("Empty Duration", "Select a duration!")
    else:
        move_entries(0)
        compute_algorithm()


def create_menu() -> None:
    """Creates a menu bar with Reset and Exit options."""
    my_menu = tk.Menu(gui)
    gui.config(menu=my_menu)

    my_options = tk.Menu(my_menu, tearoff=0)
    my_options.add_command(label="Quit", command=gui.quit)
    my_options.add_command(label="Switch Color", command=lambda: reverse_color(reverse_counter))

    my_menu.add_cascade(label="Options", menu=my_options)

    my_infos = tk.Menu(my_menu, tearoff=0)
    my_infos.add_command(label="Genre", command=genre_info)

    my_menu.add_cascade(label="Info", menu=my_infos)


def genre_info() -> None:
    """
    Infobox of genres
    """
    messagebox.showinfo(title="Genre",
                        message="Available Genres: 'soul', 'chill', 'alt-rock', 'folk', 'reggae', 'club', 'edm', " +
                                "'sleep', 'german', 'rock', 'hip-hop', 'latino', 'piano', 'j-pop', 'emo', 'indie-pop'" +
                                ", 'country', 'k-pop', 'dance', 'electro', 'garage', 'indie', 'latin', 'synth-pop', " +
                                "'funk', 'ambient', 'hard-rock', 'british', 'pop', 'alternative', " +
                                "'indian', 'singer-songwriter', 'anime'.")


def reverse_color(counter: list) -> None:
    """
    Reverses color for night mode
    """
    if counter[0] % 2 == 0:
        gui.configure(background='gray15')
        counter[0] += 1
    else:
        gui.configure(background='gray85')
        counter[0] -= 1


def place_elements() -> None:
    """
    Initialize the Mathing Menu after necessary information is correctly given as input
    """
    my_x = 360
    my_y = 60
    labels.append(tk.Label(text="Your match:", font='Helvetica 14 underline'))
    labels[-1].place(x=my_x, y=my_y - 10)

    labels.append(tk.Label(text="Name:"))
    labels[-1].place(x=my_x, y=my_y + 20)

    labels.append(tk.Label(text="Username:"))
    labels[-1].place(x=my_x, y=my_y + 40)

    labels.append(tk.Label(text="Age:"))
    labels[-1].place(x=my_x, y=my_y + 60)

    labels.append(tk.Label(text="Province:"))
    labels[-1].place(x=my_x, y=my_y + 80)

    labels.append(tk.Label(text="Match score:"))
    labels[-1].place(x=my_x, y=my_y + 100)

    labels.append(tk.Label(text="Matched Songs:"))
    labels[-1].place(x=my_x, y=my_y + 135)

    labels.append(tk.Label(text="This user also listens these songs:"))
    labels[-1].place(x=my_x, y=my_y + 275)


def check_dur() -> None:
    """
    Checks duration
    """
    myint = var.get()
    if myint == 1:
        duration[0] = "Short"
    elif myint == 2:
        duration[0] = "Medium"
    elif myint == 3:
        duration[0] = "Long"


gui = tk.Tk()
gui.title("Harmonify")
gui.geometry("800x600")
gui.resizable(False, False)
gui.configure(background='gray85')

reverse_counter = [0]
mybool = [True]
entries = []
given_entries = ["" for _ in range(7)]  # 0 username 1-5 şarkılar id, 6 genre
labels = []
new_labels = [tk.Label(gui, text="") for _ in range(7)]
buttons = []
duration = [""]  # duration[0] = short | medium | long
var = tk.IntVar()

create_menu()

copyright_label = tk.Label(text="©Copyrighted in 2025 by CSC111 Survivors™")
copyright_label.place(x=260, y=570)

labels.append(tk.Label(text="Input your favourite songs' id:"))
labels[-1].place(x=305, y=40)

labels.append(tk.Label(text="Username:"))
labels[-1].place(x=260, y=80)

entries.append(tk.Entry(gui))
entries[-1].place(x=390, y=80)

for i in range(3, 8):
    entries.append(tk.Entry(gui))
    entries[-1].place(x=390, y=(i * 40))
    labels.append(tk.Label(gui, text=f"Liked Song {i - 2}:"))
    labels[-1].place(x=260, y=(i * 40))

entries.append(tk.Entry(gui))
entries[-1].place(x=390, y=320)

labels.append(tk.Label(text="Favourite Genre:"))
labels[-1].place(x=260, y=320)

buttons.append(tk.Button(gui, text="Song List", command=button1_clicked))
buttons[-1].place(x=352, y=440)

buttons.append(tk.Button(gui, text="Visualize Program", command=button2_clicked))
buttons[-1].place(x=330, y=400)

buttons.append(tk.Button(gui, text="Launch", command=button3_clicked))
buttons[-1].place(x=356, y=480)

xvalue, yvalue = 280, 360

buttons.append(tk.Radiobutton(gui, text="Short", variable=var, value=1, command=check_dur))
buttons[-1].place(x=xvalue, y=yvalue)
buttons.append(tk.Radiobutton(gui, text="Medium", variable=var, value=2, command=check_dur))
buttons[-1].place(x=xvalue + 65, y=yvalue)
buttons.append(tk.Radiobutton(gui, text="Long", variable=var, value=3, command=check_dur))
buttons[-1].place(x=xvalue + 145, y=yvalue)

gui.mainloop()
