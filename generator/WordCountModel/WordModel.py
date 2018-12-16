class WordModel:
    def __init__(self):
        self.words = dict()

    def add_words(self, words):
        for word in words:
            if word not in self.words:
                self.words[word] = 0
            self.words[word] += 1
