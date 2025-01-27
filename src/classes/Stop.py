class Stop:
    def __init__(self, name:str, line:object, date:dict):
        self._name = name
        self._previous = [] # [[stop, line], [stop, line], ...]
        self._next = [] # [[stop, line], [stop, line], ...]
        self._line = [line] 
        self._date = {
            line.name: date
        }
    
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
        
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
    
    def __repr__(self):
        return self._name + str(self._line)
    
    
    def getNextStopOnLine(self, line:object) -> object:
        for next_stop, next_line in self.next:
            if next_line == line:
                return next_stop
            
            
    def getPreviousStopOnLine(self, line:object) -> object:
        for previous_stop, previous_line in self.previous:
            if previous_line == line:
                return previous_stop
    
    
    def mergeStop(self, other_stop:object):        
        self.previous.extend(other_stop.previous)
        self.next.extend(other_stop.next)
        self.line.extend(other_stop.line)
        for line_name, date in other_stop.date.items():
            self.date[line_name] = date
        
        for previous in other_stop.previous:
            for next in previous[0].next:
                if next[0] == other_stop:
                    next[0] = self
        
        for next in other_stop.next:
            for previous in next[0].previous:
                if previous[0] == other_stop:
                    previous[0] = self
        
        for line in other_stop.line:
            if line.start == other_stop:
                line.start = self
            if line.end == other_stop:
                line.end = self