class Aircraft:

    def __init__(self,
                 callsign,
                 current_node=None,
                 current_edge=None,
                 distance_on_edge=0.0,
                 speed=0.0,
                 current_state="PARKED"):

        self.callsign = callsign

        # Position
        self.current_node = current_node
        self.current_edge = current_edge
        self.distance_on_edge = distance_on_edge

        # Motion
        self.speed = speed

        # Operational state
        self.current_state = current_state

        # Route management
        self.route_queue = []   # List of Edge objects

    # -------------------------------------------------
    # ROUTE ASSIGNMENT
    # -------------------------------------------------

    def assign_route(self, route_node_names):
        """
        route_node_names = ["Echo_entry", "Hold_short_17R"]
        """

        if not self.current_node:
            return

        self.route_queue = []

        current_node = self.current_node

        for node_name in route_node_names:

            found_edge = None

            for edge in current_node.outgoing_edges:
                if edge.end_node.name == node_name:
                    found_edge = edge
                    break

            if found_edge:
                self.route_queue.append(found_edge)
                current_node = found_edge.end_node
            else:
                print(f"[{self.callsign}] Route error: No edge to {node_name}")
                return

        # Start taxiing
        self._proceed_to_next_edge()

    # -------------------------------------------------

    def _proceed_to_next_edge(self):

        if not self.route_queue:
            return

        next_edge = self.route_queue[0]

        if not next_edge.is_free():
            # Wait until edge is free
            self.current_state = "WAITING_EDGE"
            return

        # Edge is free → occupy
        next_edge.occupy(self)

        self.route_queue.pop(0)

        self.current_edge = next_edge
        self.current_node = None
        self.distance_on_edge = 0

        self.current_state = "TAXIING"

    # -------------------------------------------------
    # TAKEOFF
    # -------------------------------------------------

    def begin_takeoff(self):

        if not self.current_node:
            return

        if self.current_node.type != "holding_point":
            return

        if not self.current_node.outgoing_edges:
            return

        runway_entry_edge = self.current_node.outgoing_edges[0]

        if not runway_entry_edge.is_free():
            self.current_state = "WAITING_RUNWAY"
            return

        runway_entry_edge.occupy(self)

        self.current_edge = runway_entry_edge
        self.current_node = None
        self.distance_on_edge = 0

        self.current_state = "TAKEOFF_ROLL"