class InferenceEngine:

    def __init__(self, board, kb):
        self.board = board
        self.kb = kb
        self.logs = []

    def run(self, max_iterations=50):
        changed = True
        iteration = 0
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            self.logs.append(f"Iteration {iteration}")
            for rule in self.kb.rules:
                result = rule(self.board)
                self.logs.append(f"  {rule.__name__}: {result}")
                if result:
                    changed = True
        return self.logs
