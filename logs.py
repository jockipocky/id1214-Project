# logs.py

class Logger:
    """
    Simple central logger for the solver.
    Stores structured log entries and can print them in readable form.
    """

    def __init__(self):
        self.entries = []

    def add_iteration(self, iteration):
        self.entries.append({
            "type": "iteration",
            "iteration": iteration
        })

    def add_rule_change(self, rule_name, row, col, old_value, new_value, reason=None, extra=None):
        entry = {
            "type": "rule",
            "rule": rule_name,
            "row": row,
            "col": col,
            "old": old_value,
            "new": new_value,
            "reason": reason,
        }
        if extra is not None:
            entry["extra"] = extra
        self.entries.append(entry)

    def add_guess(self, row, col, old_value, new_value, depth, candidates=None, reason=None):
        self.entries.append({
            "type": "guess",
            "row": row,
            "col": col,
            "old": old_value,
            "new": new_value,
            "depth": depth,
            "candidates": list(candidates) if candidates else [],
            "reason": reason
        })

    def add_undo(self, row, col, old_value, new_value, depth, reason=None):
        self.entries.append({
            "type": "undo",
            "row": row,
            "col": col,
            "old": old_value,
            "new": new_value,
            "depth": depth,
            "reason": reason
        })

    def add_message(self, message):
        self.entries.append({
            "type": "message",
            "message": message
        })

    # -------------------------------------------------------
    # Pretty-printing
    # -------------------------------------------------------

    def format_entry(self, entry):
        t = entry["type"]

        if t == "iteration":
            return f"\n--- Iteration {entry['iteration']} ---"

        if t == "rule":
            rule = entry["rule"]
            r, c = entry["row"], entry["col"]
            new = entry["new"]
            reason = entry.get("reason", "")
            return f"[Rule] {rule} -> Placed {new} at ({r},{c}). {reason}"

        if t == "guess":
            r, c = entry["row"], entry["col"]
            new = entry["new"]
            depth = entry["depth"]
            cand = entry.get("candidates", [])
            return f"[Guess depth={depth}] Trying {new} at ({r},{c}). Candidates: {cand}"

        if t == "undo":
            r, c = entry["row"], entry["col"]
            old = entry["old"]
            depth = entry["depth"]
            reason = entry.get("reason", "")
            return f"[Undo depth={depth}] Rejected {old} at ({r},{c}). {reason}"

        if t == "message":
            return f"[Info] {entry['message']}"
        
        if t == "elim":
            rule = entry["rule"]
            r, c = entry["row"], entry["col"]
            removed = entry["removed"]
            reason = entry.get("reason", "")
            return f"[Elim] {rule}: removed {removed} from ({r},{c}). {reason}"


        return f"[Unknown] {entry}"


    def print_logs(self):
        """Print all log entries in human-readable form."""
        for entry in self.entries:
            print(self.format_entry(entry))

    def __iter__(self):
        return iter(self.entries)
    
    def add_elimination(self, rule_name, row, col, removed, reason=None):
        self.entries.append({
            "type": "elim",
            "rule": rule_name,
            "row": row,
            "col": col,
            "removed": sorted(list(removed)),
            "reason": reason,
        })
