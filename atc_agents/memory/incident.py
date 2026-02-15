class Incident:
    
    def __init__(self, type_of_incident, timestamp, aircraft_involved, runway, severity_score, resolution, contributing_factors):
        self.type_of_incident=type_of_incident
        self.timestamp=timestamp
        self.aircraft_involved=aircraft_involved
        self.runway=runway
        self.severity_score=severity_score
        self.resolution=resolution
        self.contributing_factors=contributing_factors

