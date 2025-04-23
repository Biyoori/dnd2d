import gc

class DebugLogger:
    def __init__(self) -> None:
        self.debug_mode = True
        self.logs = []

    def log(self, message: str, category: str = "INFO") -> None:
        if self.debug_mode:
            formatted_message = f"[{category}] {message}"
            self.logs.append(formatted_message)
            print(formatted_message)

    def toggle(self) -> None:
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            print("Debug mode is ON")
        else:
            print("Debug mode is OFF")
    
    def clear_logs(self) -> None:
        self.logs.clear()
        print("[DEBUG] Logs cleared")

    def log_references(self, obj: object) -> None:
        if not self.debug_mode:
            return
        references = gc.get_referrers(obj)
        self.log(f"Found {len(references)} references to {obj}: {references}", "DEBUG")
        for ref in references:
            self.log(f"Reference: {ref}", "DEBUG")

logger = DebugLogger()
logger.log("Debug logger initialized", "DEBUG")