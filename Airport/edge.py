class Edge:

    def __init__(self, start_node, end_node, current_state, max_speed, type):
        self.start_node=start_node
        self.end_node=end_node
        self.current_state=current_state
        self.max_speed=max_speed
        self.type=type