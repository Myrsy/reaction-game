# Object opens the scoreboard window that contains every users' best score and
# shows them in order from best to worst. At the bottom of the window is a play
# again - button that starts the game-window again.
from tkinter import *


class ScoreWindow:
    def __init__(self, users_dict, user_name, score):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Scoreboard")

        self.__score = score
        self.__users_dict = users_dict
        self.__user_name = user_name
        self.__play_again = False

        self.__score_label = Label(self.__mainwindow,
                                   text=f"Your score is: {self.__score}\n")
        self.__score_label.pack()
        self.__highscore_label = Label(self.__mainwindow, text="HIGH SCORES")
        self.__highscore_label.pack()

        # Only the best score is saved in the users_dict-dicionary
        if self.__score < float(self.__users_dict[self.__user_name][1]):
            self.__users_dict[self.__user_name][1] = str(self.__score)

        for player in sorted(self.__users_dict, key=lambda user: float(
                self.__users_dict[user][1])):
            # If user closes the game after logging in, the default score 1000
            # will show in score board unless it's not removed
            if float(self.__users_dict[player][1]) < 1000:
                label = Label(self.__mainwindow,
                              text=f"{player}: {self.__users_dict[player][1]}")
                label.pack()

        self.__play_again_button = Button(self.__mainwindow, text="Play again",
                                          command=self.play_again)
        self.__play_again_button.pack()

    def play_again(self):
        """
        Method destroys scoreboard-window and sets play_again to True in order
        to continue playing. If window if pressed before this, the play_again
        is left False and playing is not continued.
        :return: nothing
        """
        self.__play_again = True
        self.__mainwindow.destroy()

    def start(self):
        """
        Method calls mainloop and starts the scoreboard-window. After the
        method have run to end, this method returns play_again variable that
        are used in other functions outside this object.
        :return: boolean self.__play_again, True if play_again-button is
                                            pressed, else False
        """
        self.__mainwindow.mainloop()
        return self.__play_again
