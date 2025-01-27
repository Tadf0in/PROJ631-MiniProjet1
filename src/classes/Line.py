from .Stop import Stop

class Line:
    def __init__(self, name:str, data:dict, network:object, color:str='black'):
        self._name = name
        self._color = color
        self._network = network
        
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
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value

    @property
    def network(self):
        return self._network
    
    @network.setter
    def network(self, value):
        self._network = value

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
    
    
    def addStop(self, stop_name):
        stop = Stop(stop_name, self)
        self.end.next.append([stop, self])
        stop.previous.append([self.end, self])
        self.end = stop
        self.network.mergeDuplicateStops()
        
    
    def removeStop(self, stop:Stop):
        if self.start == self.end:
            self.network.lines.remove(self)
            
        elif self.start == stop:
            self.start = stop.getNextStopOnLine(self)
            self.start.previous.remove([stop, self])
            stop.next.remove([self.start, self])
            
        elif self.end == stop:
            self.end = stop.getPreviousStopOnLine(self)
            self.end.next.remove([stop, self])
            stop.previous.remove([self.end, self])
        
        else:
            previous_stop = stop.getPreviousStopOnLine(self)
            next_stop = stop.getNextStopOnLine(self)
            
            previous_stop.next.remove([stop, self])
            previous_stop.next.append([next_stop, self])
            stop.previous.remove([previous_stop, self])
            
            next_stop.previous.remove([stop, self])
            next_stop.previous.append([previous_stop, self])
            stop.next.remove([next_stop, self])
        
        stop.line.remove(self)
        

        
            