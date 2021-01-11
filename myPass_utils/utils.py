from os import system, name

# ----------------------------------------------------
# define clear function


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
# ----------------------------------------------------

# ----------------------------------------------------
# define int convertible check function
def is_int(string: str):
        try:
            int(string)
            return True
        except ValueError:
            return False