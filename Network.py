import os
import data2dict
from Line import Line
from Stop import Stop

class Network:
    def __init__(self, folder_path:str):
        # Crée les lignes
        self._lines:list[Line] = []
        for filename in os.listdir(folder_path):
            data = data2dict.get_data(folder_path + filename)
            line_name = filename.removesuffix('.txt')
            line = Line(line_name, self, data)
            self._lines.append(line)        
        
        # Récupère les arrêts en doublon (instances différentes mais représentants le même arrêt)
        count_stops = {}
        for stop in self.getAllStops():
            if stop.name in count_stops:
                count_stops[stop.name]['count'] += 1
                count_stops[stop.name]['stops'].append(stop)
            else:
                count_stops[stop.name] = {
                    'count': 1,
                    'stops': [stop]
                }
        duplicate_stops = [count_stop['stops'] for count_stop in count_stops.values() if count_stop['count'] > 1]
        
        # Fusionne les arrêts en doublon
        for stop in duplicate_stops:
            for duplicated in stop[1:]:
                stop[0].mergeStop(duplicated)
            

    def getAllStops(self) -> list[Stop]:
        stops = []
        for line in self._lines:
            stops.extend(line.getAllStopsOnLine())
        
        print(stops)
        
        # Supprime les doublons (doublons d'une même instance)
        unique_stops = set()
        for stop in stops:
            unique_stops.add(stop)
        print(unique_stops)
        stops = list(unique_stops)
        print(stops)
                
        return stops
    

    def shortest_path(self, start:str, end:str) -> list[str]:
        pass
    
    
    def fastest_path(self, start:str, end:str) -> list[str]:
        pass
    
    
    def foremost_path(self, start:str, end:str) -> list[str]:
        pass