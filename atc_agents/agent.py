class Agent:
    def __init__(self, name, bus):
        self.name = name
        self.bus = bus
        self.memory = None

    def observe(self, world):
        pass

    def update_memory(self, sim_time, event):
        if self.memory:
            self.memory.add(sim_time, event)

    def plan(self, world):
        pass

    def act(self):
        pass