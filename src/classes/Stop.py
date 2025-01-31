from datetime import datetime, timedelta
from vacances_scolaires_france import SchoolHolidayDates
from jours_feries_france import JoursFeries


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
    
    
    def isFerieOrHolidays(self, date:datetime) -> bool:
        return JoursFeries.is_bank_holiday(date, zone="Métropole") or SchoolHolidayDates().is_holiday(date)
    
    
    def getLineDirection(self, to_stop:object, at_datetime:datetime) -> tuple:
        # Férié ou pas
        if self.isFerieOrHolidays(at_datetime.date()):
            key = 'we_holidays_date_'
        else:
            key = 'regular_date_'
            
        # Détermine le sens de la ligne
        for next_stop, line in self.next:
            if next_stop == to_stop:
                key += 'go'
                return line, key
        else:
            for previous_stop, line in self.previous:
                if previous_stop == to_stop:
                    key += 'back'
                    return line, key
                
    
    def getNextHoraire(self, at_datetime:datetime, line:object, direction:str) -> tuple[int, datetime]:
        for i, horaire in enumerate(self.date[line.name][direction]):
            if horaire == '-':
                continue
            
            horaire_time = datetime.strptime(horaire, '%H:%M').time()
            horaire_datetime = datetime.combine(at_datetime.date(), horaire_time)
            
            if horaire_datetime >= at_datetime:
                return i, horaire_datetime
        
        # Plus du bus aujourd'hui -> celui du lendemain matin
        else:
            tomorrow = datetime.combine(at_datetime.date(), datetime.min.time()) + timedelta(days=1)
            return self.getNextHoraire(tomorrow, line, direction)
        
        
    def getArrivalHoraire(self, to_stop:object, at_datetime:datetime) -> tuple[datetime, datetime]:     
        line, key = self.getLineDirection(to_stop, at_datetime)
        if not key:
            return float('inf') # Arrêts pas reliés (ça ne devrait pas arriver)
        
        index_horaire, from_horaire_datetime = self.getNextHoraire(at_datetime, line, key)
        
        # Horaire d'arrivée au prochain arrêt
        for to_horaire in to_stop.date[line.name][key][index_horaire:]:
            if to_horaire != '-':
                break   
        
        # Terminus pour le reste de la journée -> prochain bus le lendemain
        else:
            tomorrow = datetime.combine(at_datetime.date(), datetime.min.time()) + timedelta(days=1)
            return to_stop.getNextHoraire(tomorrow, line, key)
        
        to_horaire_time = datetime.strptime(to_horaire, '%H:%M').time()
        to_horaire_datetime = datetime.combine(at_datetime.date(), to_horaire_time)
        
        return from_horaire_datetime, to_horaire_datetime