class Memory:
    def __init__(self):
        self.events = []

    def add(self, sim_time, text):
        self.events.append({
            "time": sim_time,
            "text": text
        })

    def get_recent(self, n=5):
        return self.events[-n:]