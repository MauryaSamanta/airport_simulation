##Agent class defines all the components of the agent-----memory and what it can see
## member functions: percieve()-->to get output from the perception component, that is, to see
## analyze()--->to analyse the current situation which came from percieve
## decide()--->to decide from the anlysis using LLM
## communicate()---->pass instruction to pilot agent
## take_feedback()---->take feedback from pilot
## reflect()--->reflect from this situation and store in memory

class Agent:
    
    def __init__(self, sector_scope, config):
        self.sector_scope = sector_scope
        self.memory = ATCMemory()
        self.current_snapshot = None  ## from perceive()
        self.current_assessment = None ## from analyze()
        self.pending_decisions = []
        self.active_conversations = {}
