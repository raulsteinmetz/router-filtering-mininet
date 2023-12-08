from better_profanity import profanity

def filter_profanity(string:str):
    return profanity.censor(string)

def spot_profanity(string:str):
    return profanity.contains_profanity(string)

