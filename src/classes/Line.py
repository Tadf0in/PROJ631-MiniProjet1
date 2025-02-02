from .Stop import Stop

class Line:
    def __init__(self, name:str, data:dict, network:object):
        self._name = name
        self._color = data['color']
        self._data = data
        self._network = network
        
        self._start = None
        self._end = None
        for stop_name in data['regular_path']:
            self.addStop(stop_name, check_merge=False)
            
        
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
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value

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
        stops = [stop for stop in self._parcours()]
        if len(stops) == 1 and stops[0] == None:
            return []
        return stops
    
    
    def addStop(self, stop_name, date=None, check_merge=True):
        if not date:
            if stop_name in self.data['regular_path']:
                date = {
                    'regular_date_go': self.data['regular_date_go'][stop_name],
                    'regular_date_back': self.data['regular_date_back'][stop_name],
                    'we_holidays_date_go': self.data['we_holidays_date_go'][stop_name],
                    'we_holidays_date_back': self.data['we_holidays_date_back'][stop_name],
                }
            else:
                start_name = self.data['regular_path'][0]
                date = {
                    'regular_date_go': ['-' for _ in range(len(self.data['regular_date_go'][start_name]))],
                    'regular_date_back': ['-' for _ in range(len(self.data['regular_date_back'][start_name]))],
                    'we_holidays_date_go': ['-' for _ in range(len(self.data['we_holidays_date_go'][start_name]))],
                    'we_holidays_date_back': ['-' for _ in range(len(self.data['we_holidays_date_back'][start_name]))],
                }
        
        stop = Stop(stop_name, self, date)
        
        if self.start == None and self.end == None:
            self.start = stop
            self.end = stop
        else:     
            self.end.next.append([stop, self])
            stop.previous.append([self.end, self])
            self.end = stop
            
        if check_merge:
            self.network.mergeDuplicateStops()
    
    
    def removeStop(self, stop:Stop):
        if self.start == stop and self.end == stop:
            self.start = None
            self.end = None
            
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
        
        
    def moveUpStop(self, stop:Stop):
        # Si 1er arrêt de la ligne = déjà tout en haut = rien à faire
        if self.start == stop:
            return 
        
        # Si 2eme arret de la ligne = cas particulier
        old_start = None
        if self.start.getNextStopOnLine(self) == stop:
            old_start = self.start
            self.removeStop(old_start) # Change le self.start
            ok_stops_names = [self.start.name]
        
        else:      
            # Récupère tous les arrêts précédents l'arrêt à déplacer
            ok_stops_names = []
            current = self.start
            while current.getNextStopOnLine(self) != stop:
                ok_stops_names.append(current.name)
                current = current.getNextStopOnLine(self)
            
        # Supprime tous les arrêts d'après (du précédent l'arrêt à déplacer, juqu'à la fin)
        other_stops = self.getAllStopsOnLine() 
        for other_stop in self.getAllStopsOnLine():
            if other_stop.name in ok_stops_names:
                other_stops.remove(other_stop)
            else:
                self.removeStop(other_stop)

        if old_start:
            # Réajoute l'ancien départ supprimé
            self.addStop(old_start.name, old_start.date, check_merge=False)
        else:
            # Ajoute l'arrêt à déplacer
            self.addStop(stop.name, stop.date, check_merge=False)
            other_stops.remove(stop)
        
        # Réajoute les autre arrêts
        for other_stop in other_stops:
            self.addStop(other_stop.name, other_stop.date, check_merge=False)
                
        self.network.mergeDuplicateStops()
        
        
    def moveDownStop(self, stop:Stop):
        next_stop = stop.getNextStopOnLine(self)
        if next_stop:
            self.moveUpStop(next_stop)
                