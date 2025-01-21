from Stop import Stop

class Line:
    def __init__(self, name:str, data:dict):
        self.name = name
        
        self.regular_stops = []
        for stop in data['regular_path']:
            self.regular_stops.append(Stop(stop, data['regular_date_go'][stop], data['regular_date_back'][stop]))
        
        self.holidays_stops = []
        for stop in data['we_holidays_path']:
            self.holidays_stops.append(Stop(stop, data['we_holidays_date_go'][stop], data['we_holidays_date_back'][stop]))