def all_none(*args):
    for x in args:
        if x is not None:
            return False
    return True
