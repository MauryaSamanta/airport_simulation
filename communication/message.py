class Message:
    def __init__(self, sender, receiver, msg_type, content):
        self.sender = sender
        self.receiver = receiver
        self.type = msg_type
        self.content = content