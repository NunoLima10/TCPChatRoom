from src.color_printer import ColorPrinter

class ClientChat:
    @staticmethod
    def client_message(nickname: str, message: str)-> str:
        return f"{ColorPrinter.colored(nickname)}: {message}"
    
    @staticmethod
    def notify_new_message(message: str) -> None:
        print(message)
    
    @staticmethod
    def notify_connection_lost() -> None:
        ColorPrinter.show("Connection lost", type="error")

