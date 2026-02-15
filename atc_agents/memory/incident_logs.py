from incident import Incident

class Incident_Logs:
    
    def __init__(self, logs):
        self.logs=[]

    def add(self, type_of_incident, timestamp, aircraft_involved, runway, severity_score, resolution, contributing_factors):
        newIncident=Incident(type_of_incident, timestamp, aircraft_involved, runway, severity_score, resolution, contributing_factors)
        self.logs.append(newIncident)

    def filter_by_time(self, timestamp):
        filtered_memory=[]
        for log in self.logs:
            if(log.timestamp>=timestamp):
                filtered_memory.append(log)

        return filtered_memory

    def filter_by_type(self, type_of_incident):
        filtered_memory=[]
        for log in self.logs:
            if(log.type_of_incident==type_of_incident):
                filtered_memory.append(log)

        return filtered_memory

    def filter_by_aricraft(self,aircraft_involved):
        filtered_memory=[]
        for log in self.logs:
            if(log.aircraft_involved==aircraft_involved):
                filtered_memory.append(log)

        return filtered_memory
    
    def filter_by_runway(self,runway):
        filtered_memory=[]
        for log in self.logs:
            if(log.runway==runway):
                filtered_memory.append(log)

        return filtered_memory
    ## make query, summarize and decay later on
