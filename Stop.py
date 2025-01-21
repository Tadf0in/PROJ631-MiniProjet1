class Stop:
    def __init__(self, name:str, line:object):
        self._name = name
        self._previous = [] # [stop, regular_time, holidays_time]
        self._next = [] # [stop, regular_time, holidays_time]
        self._line = [line] 
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, value):
        self._previous = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value
    
    def __repr__(self):
        return self._name
    
    
    def getNextStopOnLine(self, line:object) -> object:
        for next in self._next:
            if line in next[0].line:
                return next[0]
    
    
    def mergeStop(self, other_stop:object):
        self._previous.extend(other_stop.previous)
        self._next.extend(other_stop.next)
        self._line.extend(other_stop.line)
        
        for previous in other_stop.previous:
            for next in previous[0].next:
                if next[0] == other_stop:
                    next[0] = self
        
        for next in other_stop.next:
            for previous in next[0].previous:
                if previous[0] == other_stop:
                    previous[0] = self
        
        for line in other_stop.line:
            if line.start[0] == other_stop:
                line.start = (self, line.start[1])
            if line.end[0] == other_stop:
                line.end = (self, line.end[1])