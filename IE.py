class InferenceEngine:


    def __init__(self, board, kb):
        self.board = board
        self.kb = kb
        self.logs = []


    def run(self):
        changed = True
        while changed:
            changed = False
            for rule in self.kb.rules: # rules is list of function rules in kb
                if rule(self.board, logs=self.logs):
                    changed = True
        return self.logs
     

        



    
