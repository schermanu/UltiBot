# read the constants.py file and return all constants in a dictionary

def read_constants_from_file():
    constants = {}
    for line in open("../constants.py"):
        if '=' not in line:
            continue
        if line.startswith('#'):
            continue
        name, value = line.strip().split('=', 1)
        # exec("%s = '%s'" % (name, value))

        try:  # try to convert in int if possible
            value = int(value)
        except ValueError:
            pass
        constants[name] = value
    return constants


