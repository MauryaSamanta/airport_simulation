class MessageBus:
    def __init__(self):
        self.queue = []

    def send(self, message):
        self.queue.append(message)

    def retrieve_for(self, receiver):
        messages = [m for m in self.queue if m.receiver == receiver]
        self.queue = [m for m in self.queue if m.receiver != receiver]
        return messages