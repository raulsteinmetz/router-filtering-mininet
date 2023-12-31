def bad_words_filter(file_path, input_string):
    contains_bad_words = False

    with open(file_path, 'r') as file:
        bad_words = [line.strip() for line in file.readlines()]

    for word in bad_words:
        if word in input_string:
            contains_bad_words = True
            input_string = input_string.replace(word, '*' * len(word))

    return contains_bad_words, input_string



class BadWordsFilter:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.bad_words = [line.strip() for line in file.readlines()]

    def filter(self, input_string):
        contains_bad_words = False
        for word in self.bad_words:
            if word in input_string:
                contains_bad_words = True
                input_string = input_string.replace(word, '*' * len(word))

        return contains_bad_words, input_string

