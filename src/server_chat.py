from src.color_printer import ColorPrinter

class ServerChat:

    @staticmethod
    def notify_server_start(host: str, port: int ) -> None:
        print(f'Server start on {ColorPrinter.colored(str(host),"warning")} port {ColorPrinter.colored(str(port),"warning")}')
        
    @staticmethod
    def notify_new_client(nickname: str, address: tuple) -> str:
        message = ColorPrinter.colored(f"{nickname} joined to the chat")
        print(message)
        return message
    
    def notify_client_left(nickname: str) -> str:
        message = ColorPrinter.colored(f"{nickname} left the chat", type="error")
        print(message)
        return message
