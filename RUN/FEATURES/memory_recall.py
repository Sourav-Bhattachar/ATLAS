def recall():
    try:
        with open(r"RUN\FEATURES\Remember.txt", "r") as memory_file:
            memories = memory_file.read()
            if memories:
                return f'You told me to remember that: {memories}'
            else:
                return("Atlas has no memories yet.")
    except FileNotFoundError:
        return ("No memory file found.")
