from .node import Node
from .edge import Edge


class AirportWorld:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    # ---------------------------
    # PUBLIC METHOD
    # ---------------------------
    def build_airport(self):
        self._create_nodes()
        self._create_edges()

    # ---------------------------
    # NODE CREATION
    # ---------------------------
    def _create_nodes(self):

        self.nodes["A1"] = Node("A1", "gate")
        self.nodes["A2"] = Node("A2", "gate")

        self.nodes["Echo_entry"] = Node("Echo_entry", "taxiway")
        self.nodes["Hold_short_17R"] = Node("Hold_short_17R", "holding_point")

        self.nodes["Runway_17R_Threshold"] = Node("Runway_17R_Threshold", "runway_threshold")
        self.nodes["Runway_29L_Threshold"] = Node("Runway_29L_Threshold", "runway_threshold")

        self.nodes["Airborne"] = Node("Airborne", "air")

    # ---------------------------
    # EDGE CREATION
    # ---------------------------
    def _create_edges(self):

        self._add_edge("A1", "Echo_entry", 200, 15, "taxiway")
        self._add_edge("A2", "Echo_entry", 220, 15, "taxiway")

        self._add_edge("Echo_entry", "Hold_short_17R", 300, 20, "taxiway")

        self._add_edge("Hold_short_17R", "Runway_17R_Threshold", 100, 10, "runway_entry")

        self._add_edge("Runway_17R_Threshold", "Airborne", 2500, 80, "runway")

    # ---------------------------
    # INTERNAL HELPER
    # ---------------------------
    def _add_edge(self, start_name, end_name, length, max_speed, category):

        start_node = self.nodes[start_name]
        end_node = self.nodes[end_name]

        edge = Edge(start_node, end_node, length, max_speed, category)

        self.edges.append(edge)

        start_node.outgoing_edges.append(edge)

    # ---------------------------
    # OPTIONAL HELPER
    # ---------------------------
    def get_node(self, name):
        return self.nodes.get(name)
