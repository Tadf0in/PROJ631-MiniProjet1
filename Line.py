from Stop import Stop

class Line:
    def __init__(self, name:str, network:object, data:dict):
        self._name = name
        self._network = network
        
        start_name = data['regular_path'][0]
        self._start = (Stop(start_name, self), data['regular_date_go'][start_name])
        current = self._start[0]
        for stop_name in data['regular_path'][1:]:
            stop = Stop(stop_name, self)
            current.next.append([stop, data['regular_date_go'][stop_name], data['we_holidays_date_go'][stop_name]])
            stop.previous.append([current, data['regular_date_back'][current.name], data['we_holidays_date_back'][current.name]])
            current = stop
        
        self._end = (current, data['regular_date_back'][current.name])
        
    @property
    def name(self):
        return self._name

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value
        
    def __repr__(self):
        return self._name
    
    
    def _parcours(self):
        current = self._start[0]
        while current != self._end[0]:
            yield current
            current = current.getNextStopOnLine(self)
        yield current
        
    
    def getAllStopsOnLine(self):
        return [stop for stop in self._parcours()]
    
    
    def getStop(self, name:str) -> Stop:
        stop = self._start[0]
        while stop.next != []:
            if stop.name == name:
                return stop
            stop = stop.getNextStopOnLine(self)
            
            
    def parcours(self, start_name:str, end_name:str, date:str) -> list[str]:
        end = self.getStop(end_name)
        
        current = self.getStop(start_name)
        while current != end:
            print(current)
            current = current.getNextStopOnLine(self)
        