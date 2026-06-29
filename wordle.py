import numpy as np

with open('all_words.txt', 'r') as f:
    words_str = f.read()
words = words_str.split('\n')

with open('answer_list.txt', 'r') as f:
    answers_str = f.read()
answers = answers_str.split('\n')

words = words + answers

class Wordle:
    def __init__(self, answer=None):
        self.attempts = 6 
        self.answer = answers[np.random.randint(1, len(answers))] if not answer else answer
        self.answer_counts = {}
        for letter in self.answer:
            self.answer_counts[letter] = 1 + self.answer_counts.get(letter, 0)

    def evaluate(self, guess):

        results = ['n' for _ in range(5)]
        counts = {}
        for idx, letter in enumerate(self.answer):
            if letter == guess[idx]:
                results[idx] = 'y'
            else:
                counts[letter] = 1 + counts.get(letter, 0)

        for idx, letter in enumerate(guess):
            if results[idx] == 'n' and counts.get(letter, 0) > 0:
                results[idx] = 'a'
                counts[letter] -= 1

        return ''.join(results)


    def move(self, guess):
        if guess not in words or len(guess) != 5:
            return "You Failed"
        
        self.attempts -= 1
        
        if guess == self.answer:
            return "Correct"

        if self.attempts == 0:
            return "Game Over"

        results = self.evaluate(guess) 
        return results
