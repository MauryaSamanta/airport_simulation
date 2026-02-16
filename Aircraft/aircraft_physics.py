class AircraftPhysics:

    @staticmethod
    def update(aircraft, dt):
        """
        Main physics update entry point.
        Called every simulation tick.
        """

        # 1️⃣ Handle state transitions if needed
        AircraftPhysics._handle_state_logic(aircraft)

        # 2️⃣ Apply motion if aircraft is on an edge
        if aircraft.current_state in ["TAXIING", "TAKEOFF_ROLL"]:
            AircraftPhysics._move_along_edge(aircraft, dt)

    # -------------------------------------------------

    @staticmethod
    def _handle_state_logic(aircraft):
        """
        Decide acceleration profile based on aircraft.current_state.
        No ATC logic here.
        Only motion behavior.
        """

        state = aircraft.current_state

        if state == "PARKED":
            aircraft.speed = 0

        elif state == "TAXIING":
            AircraftPhysics._apply_acceleration(
                aircraft,
                max_speed=aircraft.current_edge.max_speed,
                acceleration=1.5  # taxi acceleration
            )

        elif state == "TAKEOFF_ROLL":
            AircraftPhysics._apply_acceleration(
                aircraft,
                max_speed=aircraft.current_edge.max_speed,
                acceleration=3.5  # stronger accel
            )

        elif state == "HOLDING_SHORT":
            aircraft.speed = 0

        elif state == "AIRBORNE":
    # Airborne aircraft does not depend on edge
            aircraft.speed += 2.5

    # -------------------------------------------------

    @staticmethod
    def _apply_acceleration(aircraft, max_speed, acceleration):
        """
        Simple capped acceleration model.
        """
        aircraft.speed += acceleration

        if aircraft.speed > max_speed:
            aircraft.speed = max_speed

    # -------------------------------------------------

    @staticmethod
    def _move_along_edge(aircraft, dt):
        """
        Move aircraft along current edge.
        """

        aircraft.distance_on_edge += aircraft.speed * dt

        if aircraft.distance_on_edge >= aircraft.current_edge.length:
            AircraftPhysics._arrive_at_node(aircraft)

    # -------------------------------------------------

    @staticmethod
    def _arrive_at_node(aircraft):
        """
        Called when aircraft reaches end of edge.
        """

        # 1️⃣ Release occupied edge
        if aircraft.current_edge is not None:
            aircraft.current_edge.release()

        # 2️⃣ Move to node
        arrived_node = aircraft.current_edge.end_node
        aircraft.current_node = arrived_node
        aircraft.current_edge = None
        aircraft.distance_on_edge = 0
        aircraft.speed = 0

        node_type = arrived_node.type

        # 3️⃣ State transitions based on node type

        if node_type == "holding_point":
            aircraft.current_state = "WAITING_CLEARANCE"

        elif node_type == "runway_threshold":
            # Automatically continue TAKEOFF_ROLL
            # Pick outgoing runway edge
            if arrived_node.outgoing_edges:
                next_edge = arrived_node.outgoing_edges[0]
                aircraft.current_edge = next_edge
                next_edge.occupy(aircraft)
                aircraft.current_state = "TAKEOFF_ROLL"

        elif node_type == "air":
            aircraft.current_state = "AIRBORNE"

        elif node_type == "gate":
            aircraft.current_state = "PARKED"

        else:
            aircraft.current_state = "WAITING_CLEARANCE"

