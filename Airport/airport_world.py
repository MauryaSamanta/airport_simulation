from .node import Node
from .edge import Edge
import math


class AirportWorld:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    # ---------------------------------
    def build_airport(self):
        self._create_nodes()
        self._create_edges()

    # ---------------------------------
    def _create_nodes(self):

        # Terminal block (visual only handled in visualizer)

        # Gates (vertical alignment like diagram)
        self.nodes["A1"] = Node("A1", "gate", 180, 300)
        self.nodes["A2"] = Node("A2", "gate", 180, 380)

        # Taxiway Echo vertical
        self.nodes["Echo_entry"] = Node("Echo_entry", "taxiway", 350, 300)

        # Slight angled turn toward runway
        self.nodes["Hold_short_17R"] = Node("Hold_short_17R", "holding_point", 350, 480)

        # Runway threshold (angled)
        self.nodes["Runway_17R_Threshold"] = Node(
            "Runway_17R_Threshold", "runway_threshold", 400, 480
        )

        # Airborne target (angled upward)
        self.nodes["Airborne"] = Node("Airborne", "air", 500, 170)

    # ---------------------------------
    def _create_edges(self):

        self._add_edge("A1", "Echo_entry", 15, "taxiway")
        self._add_edge("A2", "Echo_entry", 15, "taxiway")

        self._add_edge("Echo_entry", "Hold_short_17R", 20, "taxiway")

        self._add_edge("Hold_short_17R", "Runway_17R_Threshold", 10, "runway_entry")

        self._add_edge("Runway_17R_Threshold", "Airborne", 80, "runway")

    # ---------------------------------
    def _add_edge(self, start_name, end_name, max_speed, category):

        start = self.nodes[start_name]
        end = self.nodes[end_name]

        length = math.dist((start.x, start.y), (end.x, end.y))

        edge = Edge(start, end, length, max_speed, category)

        self.edges.append(edge)
        start.outgoing_edges.append(edge)

    # ---------------------------------
    def get_node(self, name):
        return self.nodes.get(name)