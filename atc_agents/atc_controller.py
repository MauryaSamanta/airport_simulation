class ATCController:

    def __init__(self, world):
        self.world = world

    # -------------------------------------------------
    # MAIN EVALUATION LOOP
    # -------------------------------------------------
    def evaluate(self, aircraft_list):
        """
        Called every simulation tick.
        Decides whether to issue clearances.
        """

        for aircraft in aircraft_list:
            if aircraft.current_state == "WAITING_CLEARANCE":
                self._handle_waiting_aircraft(aircraft)

    # -------------------------------------------------
    # HANDLE AIRCRAFT WAITING AT NODE
    # -------------------------------------------------
    def _handle_waiting_aircraft(self, aircraft):

        node = aircraft.current_node

        # Example logic:
        # If at holding point → check runway availability
        if node.type == "holding_point":

            runway_edge = self._get_runway_edge_from_node(node)

            if runway_edge and not runway_edge.occupied_by:
                self._grant_takeoff_clearance(aircraft, runway_edge)

    # -------------------------------------------------
    # FIND RUNWAY EDGE CONNECTED TO HOLDING POINT
    # -------------------------------------------------
    def _get_runway_edge_from_node(self, node):

        for edge in node.outgoing_edges:
            if edge.category in ["runway_entry", "runway"]:
                return edge

        return None

    # -------------------------------------------------
    # ISSUE CLEARANCE
    # -------------------------------------------------
    def _grant_takeoff_clearance(self, aircraft, edge):

        # Mark runway occupied
        edge.occupied_by = aircraft.callsign

        # Tell aircraft to enter edge
        aircraft.current_edge = edge
        aircraft.current_node = None
        aircraft.distance_on_edge = 0

        # Change aircraft state
        aircraft.current_state = "TAKEOFF_ROLL"
