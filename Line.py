from Stop import Stop

class Line:
    def __init__(self, name:str, data:dict):
        self._name = name
        
        start_name = data['regular_path'][0]
        self._start = Stop(start_name, self)
        current = self._start
        for stop_name in data['regular_path'][1:]:
            stop = Stop(stop_name, self)
            current.next.append([stop, self])
            stop.previous.append([current, self])
            current = stop
        
        self._end = current
        
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
        current = self.start
        while current != self.end:
            yield current
            current = current.getNextStopOnLine(self)
        yield current
        
    
    def getAllStopsOnLine(self):
        return [stop for stop in self._parcours()]
        