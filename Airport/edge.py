class Edge:

    def __init__(self, start_node, end_node, length, max_speed, category):
        self.start_node = start_node
        self.end_node = end_node
        self.length = length
        self.max_speed = max_speed
        self.category = category

        self.occupied_by = None

    # -------------------------------------------------

    def is_free(self):
        return self.occupied_by is None

    # -------------------------------------------------

    def occupy(self, aircraft):
        """
        Attempt to occupy this edge.
        Returns True if successful.
        Returns False if edge is already occupied.
        """

        if not self.is_free():
            return False

        self.occupied_by = aircraft
        return True

    # -------------------------------------------------

    def release(self):
        self.occupied_by = None