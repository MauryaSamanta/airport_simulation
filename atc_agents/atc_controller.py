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

            # 1️⃣ Handle aircraft parked at gate
            if aircraft.current_state == "PARKED":
                self._handle_gate_departure(aircraft)

            # 2️⃣ Handle aircraft waiting at nodes
            elif aircraft.current_state == "WAITING_CLEARANCE":
                self._handle_waiting_aircraft(aircraft)

    # -------------------------------------------------
    # HANDLE GATE TAXI CLEARANCE
    # -------------------------------------------------
    def _handle_gate_departure(self, aircraft):

        node = aircraft.current_node

        if node.type == "gate":

            taxi_edge = self._get_taxi_edge_from_node(node)

            if taxi_edge and not taxi_edge.occupied_by:
                self._grant_taxi_clearance(aircraft, taxi_edge)

    # -------------------------------------------------
    # HANDLE AIRCRAFT WAITING AT HOLDING POINT
    # -------------------------------------------------
    def _handle_waiting_aircraft(self, aircraft):

        node = aircraft.current_node

        if node.type == "holding_point":

            runway_edge = self._get_runway_edge_from_node(node)

            if runway_edge and not runway_edge.occupied_by:
                self._grant_takeoff_clearance(aircraft, runway_edge)
        
        if node.type == "taxiway":
            taxi_edge = self._get_taxi_edge_from_node(node)

            if taxi_edge and not taxi_edge.occupied_by:
                self._grant_taxi_clearance(aircraft, taxi_edge)


    # -------------------------------------------------
    # FIND TAXI EDGE FROM NODE
    # -------------------------------------------------
    def _get_taxi_edge_from_node(self, node):

        for edge in node.outgoing_edges:
            if edge.category == "taxiway":
                return edge

        return None

    # -------------------------------------------------
    # FIND RUNWAY EDGE FROM HOLDING POINT
    # -------------------------------------------------
    def _get_runway_edge_from_node(self, node):

        for edge in node.outgoing_edges:
            if edge.category in ["runway_entry", "runway"]:
                return edge

        return None

    # -------------------------------------------------
    # GRANT TAXI CLEARANCE
    # -------------------------------------------------
    def _grant_taxi_clearance(self, aircraft, edge):

        edge.occupied_by = aircraft.callsign

        aircraft.current_edge = edge
        aircraft.current_node = None
        aircraft.distance_on_edge = 0

        aircraft.current_state = "TAXIING"

    # -------------------------------------------------
    # GRANT TAKEOFF CLEARANCE
    # -------------------------------------------------
    def _grant_takeoff_clearance(self, aircraft, edge):

        edge.occupied_by = aircraft.callsign

        aircraft.current_edge = edge
        aircraft.current_node = None
        aircraft.distance_on_edge = 0

        aircraft.current_state = "TAKEOFF_ROLL"
