class Solver:
    def __init__(self, answers):
        self.answers = answers
        self.outcomes = self.get_outcomes()

    def solve(self, game):
        outcome = game.move('tarse')
        self.get_new_answers('tarse', outcome)

        moves_played = [('tarse', outcome, len(self.answers))] 
        while len(self.answers) > 1:
            best, _ = self.find_guess(self.answers)
            outcome = game.move(best[0])
            self.answers = self.get_new_answers(best[0], outcome)
            moves_played.append((best[0], outcome, len(self.answers)))
        
        outcome = game.move(self.answers[0])
        moves_played.append((self.answers[0], outcome, len(self.answers)))
        return moves_played

    def get_new_answers(self, input, output):
        new_list = []
        for answer in self.answers:
            if self.evaluate(answer, input) == output:
                new_list.append(answer)
        self.answers = new_list

    def find_guess(self):
        if len(self.answers) == 1:
            return (self.answers[0], float('inf')), ('queer', float('-inf'))

        best_word = ('', float('-inf'))
        worst_word = ('', float('inf'))

        for guess in words:
            out = {outcome: 0 for outcome in self.outcomes}
            for answer in self.answers:
                outcome = self.evaluate(answer, guess)
                out[outcome] = out.get(outcome, 0) + 1
            
            info = self.entropy(out)
            if info > best_word[1]:
                best_word = (guess, info)
            if info < worst_word[1]:
                worst_word = (guess, info)

        return best_word, worst_word

    def entropy(self, out):
        total = len(self.answers)
        entropy = 0
        for val in out.values():
            if val > 0:
                entropy -= val / total * np.log2(val / total)
        return entropy

    @staticmethod
    def get_outcomes():
        res = []
        stack = [[]]
        while stack:
            curr = stack.pop()
            if len(curr) == 5:
                res.append(''.join(curr))
                continue
            stack.extend([curr + ['y'], curr + ['a'], curr + ['n']])
        return res

    @staticmethod
    def evaluate(word, guess):
        results = ['n' for _ in range(5)]
        counts = {}
        for idx, letter in enumerate(word):
            if letter == guess[idx]:
                results[idx] = 'y'
            else:
                counts[letter] = 1 + counts.get(letter, 0)

        for idx, letter in enumerate(guess):
            if results[idx] == 'n' and counts.get(letter, 0) > 0:
                results[idx] = 'a'
                counts[letter] -= 1

        return ''.join(results)

