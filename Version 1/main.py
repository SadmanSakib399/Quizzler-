# IMPORTS
import requests, json, html
from tkinter import *
from tkinter import ttk


# VARIABLES
score = 0
question_till = 0

# colors
c_black = "#212121"
c_white = "#EFECE3"
c_green = "#63A361"
c_red = "#CD5656"


# FUNCTOINS
def get_quezz_from_the_api():
    response = requests.get(f"https://opentdb.com/api.php?amount=10&category={category_code()}&difficulty={a_difficulty.get().lower()}&type=boolean")
    response.raise_for_status()
    data = response.json()

    with open("100 Days Of Learning Python/DAY 34 - Quizzler/Version 1/guess_data", "w") as quess_data:
        json.dump(data, quess_data, indent=4, ensure_ascii=False)


def get_quezzes():
    with open("100 Days Of Learning Python/DAY 34 - Quizzler/Version 1/guess_data", "r") as file:
        data = json.load(file)
    return data["results"]


def save_high_Score():
    global high_score

    if score > high_score:
        with open("100 Days Of Learning Python/DAY 34 - Quizzler/Version 1/high score", "w") as file:
            file.write(str(score))
        high_score_label.config(text=f"High Score: {score}")


def start():
    global question_till

    enable_button()
    quezz = get_quezzes()
    canvas.config(bg=c_white)

    if question_till < len(quezz):
        quezz_label.config(text=html.unescape(quezz[question_till]["question"]), bg=c_white)
    else:
        question_till = 0
        get_quezz_from_the_api()
        start()


def check(ans):
    global quezz, question_till, score

    correct_answer = quezz[question_till]["correct_answer"]
    disable_button()

    if ans == correct_answer:
        score += 1
        save_high_Score()
        canvas.config(bg=c_green)
        quezz_label.config(bg=c_green)
        score_label.config(text=f"Score: {score}")
    else:
        score = 0
        canvas.config(bg=c_red)
        quezz_label.config(bg=c_red)
        score_label.config(text=f"Score: {score}")

    question_till += 1
    screen.after(1000, start)


def category_code():
    if a_category.get() == "General Knowledge":
        return "9"


def disable_button():
    yes_button.config(state="disabled") 
    no_button.config(state="disabled") 


def enable_button():
    yes_button.config(state="normal")
    no_button.config(state="normal")


def Select_button():
    global quezz
    get_quezz_from_the_api()
    quezz = get_quezzes()


# SCREEN SETUPS
screen = Tk()
screen.title("Quizzler")
screen.config(padx= 200, pady= 100, background=c_black)

canvas = Canvas( width=350, height=350, bg= c_white, highlightthickness=0)

score_label = Label(text= f"Score: {score}", bg=c_black, fg="white", font="Arial 20 bold", pady= 30)
high_score_label = Label(text= f"High Score: 0", bg=c_black, fg="white", font="Arial 20 bold", pady= 30)
quezz_label = Label(text="", bg=c_white, fg=c_black, font="Arial 16 bold", wraplength=320,)

yes_button = Button(text="✔", font="arial 32", bg= c_green, command=lambda: check(ans= "True"))
no_button = Button(text="✖", font="arial 32", bg= c_red, command=lambda: check(ans= "False"))
start_button = Button(text="SELECT", font="arial 12 italic", command=Select_button)

a_category = StringVar()
category = ttk.Combobox( width = 24, textvariable = a_category)
category['values'] = ("General Knowledge",)
category.current(0)

a_difficulty = StringVar()
difficulty = ttk.Combobox( width = 24, textvariable = a_difficulty)
difficulty['values'] = ("Easy", "Medium")
difficulty.current(0)

canvas.grid(row=1, column=0, columnspan=2)
quezz_label.grid(row=1, column=0, columnspan=2)
score_label.grid(row=0, column=0, sticky="w")
high_score_label.grid(row=0, column=1, sticky="e")
yes_button.grid(row=2, column=0, ipadx=40, padx=15, pady=30)
no_button.grid(row=2, column=1, ipadx=40, padx=15, pady=30)
start_button.grid(row=4, column=0, columnspan=2, pady= 20, ipadx= 100)
category.grid(column = 0, row = 3)
difficulty.grid(column = 1, row = 3)


# MAIN LOOP
try:
    with open("100 Days Of Learning Python/DAY 34 - Quizzler/version 1/high score", "r") as file:
        high_score = int(file.read())
        high_score_label.config(text= f"High Score: {high_score}")
except: 
    pass

get_quezz_from_the_api()
quezz = get_quezzes()
start()


screen.mainloop()