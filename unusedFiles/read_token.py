# Read the bot token contained in the file located at the given path.
def read_bot_token(filePath):
    with open(filePath, "r") as f:
        lines = f.readlines()
        return lines[0].strip()
