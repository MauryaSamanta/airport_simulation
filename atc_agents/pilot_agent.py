from .agent import Agent
from .memory.memory import Memory
from communication.message import Message

class PilotAgent(Agent):

    def __init__(self, aircraft, bus):
        super().__init__(aircraft.callsign, bus)
        self.aircraft = aircraft
        self.memory = Memory()
        self.pending_actions = []

    def observe(self, world):
        messages = self.bus.retrieve_for(self.name)
        return messages

    def plan(self, world):
        messages = self.observe(world)

        for msg in messages:
            if msg.type == "CLEARANCE_TAXI":
                route = msg.content["route"]
                self.pending_actions.append(("TAXI_ROUTE", route))

            if msg.type == "CLEARANCE_TAKEOFF":
                self.pending_actions.append(("TAKEOFF", None))

    def act(self):
        if not self.pending_actions:
            return

        action, data = self.pending_actions.pop(0)

        if action == "TAXI_ROUTE":
            self.aircraft.assign_route(data)

        if action == "TAKEOFF":
            self.aircraft.begin_takeoff()