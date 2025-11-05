import requests, json, html
from tkinter import *
from tkinter import ttk


class Main_UI:
    
    def __init__(self, background_color, middle_color, right_question_color, wrong_question_color):

        self.screen = Tk()
        self.screen.title("Quizzler")
        self.screen.resizable(False, False)
        self.screen.config(padx= 200, pady= 100, background=background_color)

        self.canvas = Canvas( width=350, height=350, bg=middle_color, highlightthickness=0)

        self.score_label = Label(text= f"Score: 0", bg=background_color, fg=middle_color, font="Arial 20 bold", pady= 30)
        self.high_score_label = Label(text= f"High Score: 0", bg=background_color, fg=middle_color, font="Arial 20 bold", pady= 30)
        self.quezz_label = Label(text="", bg=middle_color, fg=background_color, font="Arial 16 italic", wraplength=320,)

        self.yes_button = Button(text="✔", font="arial 32", bg= right_question_color)
        self.no_button = Button(text="✖", font="arial 32", bg= wrong_question_color)
        self.start_button = Button(text="SELECT", font="arial 12 bold", bg=background_color, fg=middle_color)

        self.a_category = StringVar()
        self.category = ttk.Combobox( width = 24, textvariable = self.a_category)
        self.category['values'] = ("General Knowledge",)
        self.category.current(0)

        self.a_difficulty = StringVar()
        self.difficulty = ttk.Combobox( width = 24, textvariable = self.a_difficulty, background=background_color)
        self.difficulty['values'] = ("Easy", "Medium")
        self.difficulty.current(0)

        self.canvas.grid(row=1, column=0, columnspan=2)
        self.quezz_label.grid(row=1, column=0, columnspan=2)
        self.score_label.grid(row=0, column=0, sticky="w")
        self.high_score_label.grid(row=0, column=1, sticky="e")
        self.yes_button.grid(row=2, column=0, ipadx=40, padx=15, pady=30)
        self.no_button.grid(row=2, column=1, ipadx=40, padx=15, pady=30)
        self.start_button.grid(row=4, column=0, columnspan=2, pady= 20, ipadx= 140)
        self.category.grid(column = 0, row = 3)
        self.difficulty.grid(column = 1, row = 3)
        

    def disable_button(self):
        self.yes_button.config(state="disabled") 
        self.no_button.config(state="disabled") 


    def enable_button(self):
        self.yes_button.config(state="normal")
        self.no_button.config(state="normal")


    def run_loop(self):
        self.screen.mainloop()


    def set_brain_button(self, brain):
        self.yes_button.config(command=lambda: brain.check("True"))
        self.no_button.config(command=lambda: brain.check("False"))
        self.start_button.config(command=lambda:brain.Select_button())





class Quezz_Brain:

    def __init__(self, difficulty, category, main_ui:Main_UI):

        self.ui = main_ui

        self.score = 0
        self.high_score = 0
        self.question_till = 0

        self.quezz = None
        self.category = category
        self.difficulty = difficulty.lower()

        self.update_score()


    def category_code(self):
        if self.category == "General Knowledge":
            return "9"


    def get_quezz_from_the_api(self):
        try:
            self.response = requests.get(f"https://opentdb.com/api.php?amount=10&category={self.category_code()}&difficulty={self.difficulty}&type=boolean")
            self.response.raise_for_status()
            self.data = self.response.json()
        except:
            print("Unable to reach the API.")
        else:
            with open("guess_data.json", "w") as quess_data:
                json.dump(self.data, quess_data, indent=4, ensure_ascii=False)


    def load_quezzes(self):
        try:
            with open("guess_data.json", "r") as file:
                self.data = json.load(file)
            self.quezz = self.data["results"]
        except:
            print("No quezz data file found.")
    

    def start(self, middle_color="#EFECE3"):
        self.ui.enable_button()
        self.ui.canvas.config(bg=middle_color)
        self.load_quezzes()

        if self.question_till < len(self.quezz):
            self.ui.quezz_label.config(text=html.unescape(self.quezz[self.question_till]["question"]), bg=middle_color)
        else:
            self.question_till = 0
            self.get_quezz_from_the_api()
            self.start()


    def check(self, ans, right_color="#63A361", wrong_color="#CD5656"):
        correct_answer = self.quezz[self.question_till]["correct_answer"]
        self.ui.disable_button()

        if ans == correct_answer:
            self.score += 1
            self.ui.canvas.config(bg=right_color)
            self.ui.quezz_label.config(bg=right_color)
            self.save_high_Score()
            self.update_score()
        else:
            self.score = 0
            self.ui.canvas.config(bg=wrong_color)
            self.ui.quezz_label.config(bg=wrong_color)
            self.update_score()

        self.question_till += 1
        self.ui.screen.after(1000, self.start)


    def Select_button(self):
        self.get_quezz_from_the_api()
        self.load_quezzes()


    def update_score(self):
        self.load_high_score()
        self.ui.score_label.config(text=f"Score: {self.score}")
        self.ui.high_score_label.config(text=f"High Score: {self.high_score}")


    def save_high_Score(self):
        if self.score > self.high_score:
            with open("high_score.txt", "w") as file:
                file.write(str(self.score))


    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except: 
            print("No high score file found.")
            self.save_high_Score()