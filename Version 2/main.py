from tkinter import *
from classes import *

c_black = "#212121"
c_white = "#EFECE3"
c_green = "#63A361"
c_red = "#CD5656"


ui = Main_UI(c_black, c_white, c_green, c_red)
quezz_brain = Quezz_Brain("Easy", "General Knowledge", ui)
ui.set_brain_button(quezz_brain)
quezz_brain.get_quezz_from_the_api()
quezz_brain.start()
ui.run_loop()