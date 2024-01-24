# The project is a reaction game with login screen and scoreboard window.
# The game consists of a certain amount of labels that changes colours to
# either red, blue, green or stays white. The player has to press the number in
# keyboard that corresponds the green label in the game screen as soon as
# possible. The faster the player presses it, the smaller the score (which is
# better than bigger score). If player presses the wrong coloured number,
# player gets +1 extra points.

# Because used objects are in other files, they are imported
import csv
from loginwindow_class import LogInWindow
from gamewindow_class import GameWindow
from scorewindow_class import ScoreWindow

# These variables are better left untouched. Because different numbers in
# both of these variables corresponds to a difference in duration and
# hardness in games, the scores in scoreboard won't be comparable.
LABEL_COUNT = 5
ROUND_COUNT = 5


def read_file():
    """
    Function reads the "users.csv" file where the names, passwords and best
    scores of all users are stored. Because the file is handled through the
    code, there won't be human errors, and thus checking for exceptions are
    not needed
    :return: dict, contains users from file in format {"user1": ["password1",
    "score1"], "user2": ["password2", "score2"],...}
    """
    file_name = "users.csv"
    users_dict = {}

    with open(file_name, "r") as file_to_read:
        reader = csv.reader(file_to_read)
        for user in reader:
            users_dict[user[0]] = user[1:]

    return users_dict


def call_login(users_dict):
    """
    Function calls for object's LogInWindow method start_log_in()
    which starts the sign_in-window
    :param users_dict: dict, contains users from file
    :return: str user_name, name of current user
             str password, password of current user
             boolean sign_in, if user closes sign_in-window before starting
                              the game (ie. before signing in),
                              sign_in will be False and else True
    """
    sign_in_window = LogInWindow(users_dict)
    user_name, password, sign_in = sign_in_window.start_sign_in()
    return user_name, password, sign_in


def call_game(users_dict):
    """
    Function calls for object's GameWindow method start_game(), which starts
    the game window
    :param users_dict: dict, contains users from file
    :return: float, score that current user got
    """
    game_window = GameWindow(users_dict, LABEL_COUNT, ROUND_COUNT)
    score = game_window.start_game()
    return score


def call_scoreboard(users_dict, user_name, score):
    """
    Function calss for object's ScoreWindow method start(), which starts the
    scoreboard window
    :param users_dict: dict, contains users from file
    :param user_name: str, name of current user
    :param score: float, score that current user got
    :return: boolean play_again, True if user has pressed the play again button
                                 and False if the user doesn't
    """
    scoreboard_window = ScoreWindow(users_dict, user_name, score)
    play_again = scoreboard_window.start()
    return play_again


def write_file(users_dict):
    """
    Function writes the dict of users to the file "users.csv".
    :param users_dict: dict, contains users from file
    :return: returns nothing
    """
    file_name = "users.csv"

    with open(file_name, "w", newline="") as file_to_write:
        writer = csv.writer(file_to_write)

        for user in users_dict:
            password = users_dict[user][0]
            score = users_dict[user][1]
            writer.writerow([user, password, score])
        

def main():
    users_dict = read_file()
    user_name, password, sign_in = call_login(users_dict)

    play_again = True
    if sign_in:
        while play_again:
            score, game_successful = call_game(users_dict)
            # If player quits the game window without playing game to the end
            # scoreboard won't show
            if game_successful:
                play_again = call_scoreboard(users_dict, user_name, score)
            else:
                play_again = False

    write_file(users_dict)


main()
