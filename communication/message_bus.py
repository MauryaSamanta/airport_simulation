class MessageBus:

    def __init__(self):
        self.queue = []
        self.listeners = []

    def register_listener(self, listener):
        self.listeners.append(listener)

    def send(self, message):
        self.queue.append(message)

        # Notify listeners (Visualizer)
        for listener in self.listeners:
            listener(message)

    def retrieve_for(self, receiver):
        messages = [m for m in self.queue if m.receiver == receiver]
        self.queue = [m for m in self.queue if m.receiver != receiver]
        return messages