class Aircraft:

    def __init__(self, callsign, current_node=None, current_edge=None,
                 distance_on_edge=0.0, speed=0.0, current_state="PARKED"):

        self.callsign = callsign

        # Position
        self.current_node = current_node      # Node object (if stationary)
        self.current_edge = current_edge      # Edge object (if moving)
        self.distance_on_edge = distance_on_edge  # meters along edge

        # Motion
        self.speed = speed                    # meters per second

        # Operational state
        self.current_state = current_state
