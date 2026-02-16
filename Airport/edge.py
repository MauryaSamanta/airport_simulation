class Edge:

    def __init__(self, start_node, end_node, length, max_speed, category):
        self.start_node=start_node
        self.end_node=end_node
        self.length=length
        self.max_speed=max_speed
        self.category=category
        self.occupied_by=None
        # self.category=category

    def occupy(self, aircraft):
        self.occupied_by=aircraft
    
    def release(self):
        self.occupied_by=None