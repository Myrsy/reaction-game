# Object opens the sign_in-window that contains entries for user name and
# password and buttons for signing in and creating account. If the user
# wants to sign in, there need to be the wanted account already in the
# "users.csv" file. Otherwise player needs to create the account by pressing
# the sign_up-button. After pressing the sign_in-button, the player needs to
# create the account by entering desired user name, which is not already
# used, and password two times. If one of these fails, the error message
# appears. If player wants to sign in after they have pressed the
# sign_up-button, they need to close the window and run the code again.
from tkinter import *


class LogInWindow:
    def __init__(self, users_dict):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Sign in")

        self.__user_name = None
        self.__password = None
        self.__users_dict = users_dict
        self.__login_successful = False

        self.__user_name_label = Label(self.__mainwindow, text="User name:")
        self.__user_name_label.grid(row=0, column=0)
        self.__user_name_entry = Entry(self.__mainwindow)
        self.__user_name_entry.grid(row=0, column=1)
        self.__password_label = Label(self.__mainwindow, text="Password:")
        self.__password_label.grid(row=1, column=0)
        self.__password_entry = Entry(self.__mainwindow, show="*")
        self.__password_entry.grid(row=1, column=1)
        self.__sign_in = Button(self.__mainwindow, text="Sign in",
                                command=self.sign_in)
        self.__sign_in.grid(row=2, column=0)
        self.__sign_up_button = Button(self.__mainwindow,
                                       text="Don't have an account?",
                                       command=self.change_sign_in)
        self.__sign_up_button.grid(row=2, column=2)

        # The following widgets are defined here but are placed in the window
        # later since they belong to signing up
        self.__error_text_label = Label(self.__mainwindow)
        self.__password_again_label = Label(self.__mainwindow,
                                            text="Enter password again:")
        self.__password_again_entry = Entry(self.__mainwindow, show="*")

    def get_entries(self, state):
        """
        Method gets the entries of user name and password and saves them to
        variables self.__user_name and self.__password. If player is signing
        up, the passwords are saved in list and are compared later.
        :param state: str, "sign in" if player is signing in and "sign up" if
                            player is signing up
        :return: nothing
        """
        self.__user_name = self.__user_name_entry.get()

        if state == "sign in":
            self.__password = self.__password_entry.get()
        elif state == "sign up":
            self.change_sign_in()

            self.__password = [self.__password_entry.get(),
                               self.__password_again_entry.get()]
            self.__password_again_entry.delete(0, "end")

        self.__password_entry.delete(0, "end")

    def sign_in(self):
        """
        Method checks if entered user name is in the file (ie. in the dict of
        users) and if the entered password matches the user's password in the
        file. If entries doesn't match, self.error(index) is called.
        :return: nothing
        """
        self.get_entries(state="sign in")

        if self.__user_name in self.__users_dict and self.__password in \
                self.__users_dict[self.__user_name]:
            self.start_game()
        elif self.__user_name not in self.__users_dict:
            self.error(0)
        else:
            self.error(1)

    def sign_up(self):
        """
        Method checks if passwords in list matches and are not empty and that
        entered user name is not already in use nor empty. If one of these
        conditions fail, self.error(index) is called. If passwords match,
        self.__password-list is converted to string. User is added to
        dictionary with a score of 1000. Since smaller score is better and
        1000 is almost impossible to get, it's safe to set it as a default
        score in case that the player closes the game before getting any
        points.
        :return: nothing
        """
        self.get_entries(state="sign up")

        if self.__password[0] == self.__password[1] and self.__password[0] not\
                in " " and self.__user_name not in self.__users_dict and \
                self.__user_name not in " ":
            self.__password = self.__password[0]
            self.__users_dict[self.__user_name] = [self.__password, "1000"]
            self.start_game()
        elif self.__user_name in " ":
            self.error(2)
        elif self.__user_name in self.__users_dict:
            self.error(3)
        elif self.__password[0] in " ":
            self.error(5)
        else:
            self.error(4)

    def change_sign_in(self):
        """
        Method changes widgets to match the sign up - window.
        :return:
        """
        self.__mainwindow.title("Sign up")
        self.__user_name_label.configure(text="Enter user name:")
        self.__password_label.configure(text="Enter password:")
        self.__sign_up_button.configure(text="Sign up", command=self.sign_up)
        self.__sign_in.destroy()

        # Place widgets to mainwindow that are defined earlier
        self.__password_again_label.grid(row=2, column=0)
        self.__password_again_entry.grid(row=2, column=1)

    def error(self, message_index):
        """
        Method adds label that shows the correct error message from the list.
        :param message_index: int, index of the error message
        :return: nothing
        """
        error_messages = ["User not found", "Incorrect password",
                          "Invalid user name", "User already exists",
                          "Passwords doesn't match", "Invalid password"]

        self.__error_text_label.configure(text=error_messages[message_index])
        self.__error_text_label.grid(row=3, column=0, columnspan=3)

    def start_game(self):
        """
        Method destroys sign_in-window and changes the self.__login_successful
        to True since signing in is now completed successfully.
        :return: nothing
        """
        self.__login_successful = True
        self.__mainwindow.destroy()

    def start_sign_in(self):
        """
        Method calls the mainloop and starts the signing in. After the method
        have run to end, this method returns variables that are used in other
        functions outside this object.
        :return: str self.__user_name, name of the current user
                 str self.__password, password of the current user
                 boolean self.__login_successful, True if sign_in-button is
                 pressed with valid entries, else returns False
        """
        self.__mainwindow.mainloop()
        return self.__user_name, self.__password, self.__login_successful
