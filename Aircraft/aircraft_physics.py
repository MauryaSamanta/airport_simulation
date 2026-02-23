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

        aircraft.altitude += aircraft.vertical_speed * dt

        if aircraft.altitude < 0:
            aircraft.altitude = 0

        if aircraft.current_state == "AIRBORNE":

        # Continue straight ahead from runway heading
            heading_vector_x = 0.5
            heading_vector_y = -1.0

            magnitude = (heading_vector_x**2 + heading_vector_y**2) ** 0.5
            heading_vector_x /= magnitude
            heading_vector_y /= magnitude

            aircraft.x += heading_vector_x * aircraft.speed * dt
            aircraft.y += heading_vector_y * aircraft.speed * dt

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

        # Vertical motion update
        elif aircraft.current_state == "AIRBORNE":
            aircraft.vertical_speed = 5.0     # climb rate (m/s)
        elif aircraft.current_state == "ON_FINAL":
            aircraft.vertical_speed = -4.0    # descent rate
        else:
            aircraft.vertical_speed = 0.0

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

        aircraft.distance_on_edge += aircraft.speed * dt

        start = aircraft.current_edge.start_node
        end = aircraft.current_edge.end_node

        progress = aircraft.distance_on_edge / aircraft.current_edge.length
        progress = min(progress, 1)

        aircraft.x = start.x + progress * (end.x - start.x)
        aircraft.y = start.y + progress * (end.y - start.y)

        if aircraft.distance_on_edge >= aircraft.current_edge.length:
            AircraftPhysics._arrive_at_node(aircraft)

    # -------------------------------------------------

    @staticmethod
    def _arrive_at_node(aircraft):
        """
        Called when aircraft reaches end of edge.
        """

        # Save edge reference BEFORE clearing
        finished_edge = aircraft.current_edge

        # Release occupied edge
        if finished_edge is not None:
            finished_edge.release()

        arrived_node = finished_edge.end_node

        aircraft.current_edge = None
        aircraft.distance_on_edge = 0

        node_type = arrived_node.type

        # -------------------------------------------------
        # HOLDING POINT
        # -------------------------------------------------
        if node_type == "holding_point":
            aircraft.current_node = arrived_node
            aircraft.speed = 0
            aircraft.current_state = "WAITING_CLEARANCE"

        # -------------------------------------------------
        # RUNWAY THRESHOLD
        # -------------------------------------------------
        elif node_type == "runway_threshold":
            aircraft.current_node = arrived_node
            aircraft.speed = 0

            if arrived_node.outgoing_edges:
                next_edge = arrived_node.outgoing_edges[0]

                if next_edge.is_free():
                    next_edge.occupy(aircraft)
                    aircraft.current_edge = next_edge
                    aircraft.current_node = None
                    aircraft.current_state = "TAKEOFF_ROLL"

        # -------------------------------------------------
        # AIR (THIS IS THE FIX)
        # -------------------------------------------------
        elif node_type == "air":
            # DO NOT zero speed
            aircraft.current_node = None
            aircraft.current_state = "AIRBORNE"
            # keep speed as is

        # -------------------------------------------------
        # GATE
        # -------------------------------------------------
        elif node_type == "gate":
            aircraft.current_node = arrived_node
            aircraft.speed = 0
            aircraft.current_state = "PARKED"

        # -------------------------------------------------
        # CONTINUE TAXI IF ROUTE EXISTS
        # -------------------------------------------------
        else:
            aircraft.current_node = arrived_node

            if aircraft.route_queue:
                aircraft._proceed_to_next_edge()
            else:
                aircraft.speed = 0
                aircraft.current_state = "WAITING_CLEARANCE"