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

logger = DebugLogger()
logger.log("Debug logger initialized", "DEBUG")