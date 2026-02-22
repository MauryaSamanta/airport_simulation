from .agent import Agent
from .memory.memory import Memory
from communication.message import Message

class ATCAgent(Agent):

    def __init__(self, bus):
        super().__init__("ATC", bus)
        self.memory = Memory()

    def observe(self, world):
        # Observe aircraft states
        return world

    def plan(self, world, aircraft_list):

        for aircraft in aircraft_list:

            # At gate → issue taxi clearance
            if aircraft.current_node and aircraft.current_node.name.startswith("A"):
                msg = Message(
                    sender="ATC",
                    receiver=aircraft.callsign,
                    msg_type="CLEARANCE_TAXI",
                    content={"route": ["Echo_entry", "Hold_short_17R"]}
                )
                self.bus.send(msg)

            # At holding point → check runway
            if aircraft.current_node and aircraft.current_node.name == "Hold_short_17R":
                if self.runway_free(world, aircraft_list):

                    msg = Message(
                        sender="ATC",
                        receiver=aircraft.callsign,
                        msg_type="CLEARANCE_TAKEOFF",
                        content={"runway": "17R"}
                    )
                    self.bus.send(msg)

    def runway_free(self, world, aircraft_list):

        for aircraft in aircraft_list:

            if aircraft.current_edge:
                if aircraft.current_edge.category == "runway":
                    return False

            if aircraft.current_node:
                if aircraft.current_node.type == "runway_threshold":
                    return False

        return True

    def act(self):
        pass