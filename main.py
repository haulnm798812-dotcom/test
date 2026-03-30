try:
    if float(habit.strip()):
        return False, "habit mustnot be a number"
except ValueError:
    pass
if habit.strip() != "":
    return True, None