# Object opens the game window that contains the number of labels with text
# 1,2,...,n where n is the number of labels defined in oma_projekti.py file.
# Window also shows instructions on how to play.
# After two seconds, when the start_button is pressed, the labels will
# change colors. Colors will disappear if the player presses any key on
# keyboard. Colors will then appear after two seconds. This repeats as many
# times as it is defined in oma_projekti.py file.
from tkinter import *
import random
import time


class GameWindow:
    def __init__(self, users_dict, label_count, round_count):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Reaction game")
        self.__mainwindow.geometry(f"{100 * label_count + 150}x300")
        self.__mainwindow.bind("<Key>", self.press_key)

        self.__users_dict = users_dict
        self.__label_count = label_count
        self.__round_count = round_count
        self.__press_now = False

        self.__wrong_colors = ["pink", "white", "light blue"]
        self.__color_list = []

        self.__start_timing = None
        self.__stop_timing = None
        self.__score = 0
        self.__current_round = 0
        self.__game_successful = False

        self.__labels = []
        for i in range(self.__label_count):
            label = Label(self.__mainwindow, text=i + 1, height=5, width=5,
                          bg="white")
            label.place(x=100 + 100 * i, y=100)
            self.__labels.append(label)

        info = "How to play:\n When the color in boxes changes, press the " \
               "number in keyboard that changes to green.\nThe sooner you " \
               "press it the better the score and if you press other than " \
               "green button, \nyou'll get plus points (smaller score is " \
               "better)."
        self.__info_label = Label(self.__mainwindow, text=info)
        self.__info_label.place(x=50, y=200)
        self.__start_button = Button(self.__mainwindow, text="Start game",
                                     command=self.start_round)
        self.__start_button.place(x=50, y=250)
        self.__score_label = Label(self.__mainwindow, text="Score: 0")
        self.__score_label.place(x=50, y=10)

    def update_window(self):
        """
        Method updates the window in order to update the GUI.
        :return: nothing
        """
        self.__mainwindow.update()

    def start_round(self):
        """
        Method destroys the how-to-play-text and the start_button and calls
        the self.play_round() in order to start the game.
        :return: nothing
        """
        self.__info_label.destroy()
        self.__start_button.destroy()
        self.update_window()

        self.play_round()

    def play_round(self):
        """
        Method compares if current round count is less or equal to defined
        round count. If it is, a list of wrong colors is randomized (for
        example ["white", "pink", "light blue", "white"] and after that
        one of the items is changed to light green, which is the correct
        color. After two seconds, the method self.color_labels() is called.
        :return: nothing
        """
        self.__current_round += 1
        if self.__current_round <= self.__round_count:
            self.__color_list = [self.__wrong_colors[random.randint(
                0, len(self.__wrong_colors) - 1)] for i in range(
                self.__label_count)]
            self.__color_list[
                random.randint(0, len(self.__color_list) - 1)] = \
                "light green"

            self.__mainwindow.after(2000, self.color_labels)
        else:
            self.end_screen()

    def color_labels(self):
        """
        Method changes the color of the labels to corresponding colors from
        the list self.__labels. self.__press_now is set to True making the
        keyboard keys active to pressing. Point system works by taking the
        time, that it takes to player to push the key. Time starts here.
        :return: nothing
        """
        for i in range(len(self.__labels)):
            self.__labels[i].configure(bg=self.__color_list[i])

        self.__press_now = True
        self.__start_timing = time.time()

    def press_key(self, event):
        """
        Method stops time and cheks if the key that the player pressed is the
        correct number and adds the time difference to score. If the wrong key
        is pressed, an extra second is added to score. After this, all labels
        are set to white and self.update_window() is called in order to update
        the window and self.play_round() is called in order to play the correct
        amount of rounds.
        :param event: KeyPress event
        :return: nothing
        """
        if self.__press_now:
            self.__stop_timing = time.time()

            if event.char in "123456789" and int(event.char) - 1 == \
                    self.__color_list.index("light green"):
                self.__score += self.__stop_timing - self.__start_timing
            elif event.char in "123456789":
                self.__score += self.__stop_timing - self.__start_timing + 1

            self.__score = round(self.__score, 2)
            self.__score_label.configure(text=f"Score: {self.__score}")

            # Change every label's background to white
            self.__press_now = False
            for label in self.__labels:
                label.configure(bg="white")  # Configuraa default väri

            self.update_window()
            self.play_round()

    def end_screen(self):
        """
        Method destroys game-window and changes self.__game_successful to True
        since a game is successfully played to the end.
        :return: nothing
        """
        self.__game_successful = True
        self.__mainwindow.destroy()

    def start_game(self):
        """
        Method calls mainloop and starts the game. After the method
        have run to end, this method returns score variable that are used in
        other functions outside this object.
        :return: float self.__score, score from the current game
        """
        self.__mainwindow.mainloop()
        return self.__score, self.__game_successful
