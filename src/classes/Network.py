import os
from ..data2dict import get_data
from .Line import Line
from .Stop import Stop
from datetime import timedelta


class Network:
    def __init__(self, folder_path:str):
        # Crée les lignes
        self._folder_path = folder_path
        self._lines:list[Line] = []
        for filename in os.listdir(folder_path):
            data = get_data(os.path.join(folder_path, filename))
            line_name = filename.removesuffix('.txt')
            line = Line(line_name, data, self)
            self._lines.append(line)        
        
        self.mergeDuplicateStops()
        
    @property
    def folder_path(self):
        return self._folder_path
    
    @folder_path.setter
    def folder_path(self, value):
        self._folder_path = value      
    
    @property
    def lines(self):
        return self._lines
    
    @lines.setter
    def lines(self, value):
        self._lines = value
            

    def getAllStops(self) -> list[Stop]:
        stops = []
        for line in self._lines:
            stops.extend(line.getAllStopsOnLine())

        # Supprime les doublons (doublons d'une même instance)
        stops = list(set(stops))
                
        return stops
    
    
    def getStop(self, name: str) -> Stop:
        for stop in self.getAllStops():
            if stop.name == name:
                return stop
    
    
    def mergeDuplicateStops(self):
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
                   
    
    def dijkstra(self, start_name:str, end_name:str, start_datetime, algorithm) -> list[Stop]:
        start = self.getStop(start_name)
        end = self.getStop(end_name)
        
        # Initialisation
        unvisited = self.getAllStops()
        paths = {stop.name: (None, float('inf')) for stop in unvisited}
        paths[start.name] = (start, 0)
        
        # Calcule les distances
        while len(unvisited) > 0:
            # On choisit le prochain noeud avec la plus petite distance
            current = min(unvisited, key=lambda stop: paths[stop.name][1])
            if paths[current.name][1] == float('inf'):
                return None # Pas de chemin
            
            # Si destination atteinte on s'arrête
            if current == end:
                break
            
            print(unvisited, '\n', paths, '\n', current)
            
            # Met à jour les distances
            for linked_stop, line in current.previous + current.next:
                
                # Si arrêt déjà visiter on skip
                if linked_stop not in unvisited:
                    continue
                
                current_distance = paths[current.name][1]
                current_datetime = start_datetime + timedelta(minutes=current_distance)
                
                weight = current.getWeight(linked_stop, current_datetime, algorithm)
                
                old_distance = paths[linked_stop.name][1]
                new_distance = current_distance + weight
                
                if new_distance < old_distance:
                    paths[linked_stop.name] = (current, new_distance)
                
            unvisited.remove(current)        
                
        # Récupère le plus court chemin
        path = []
        stop = end
        while stop and stop != start:
            path.append(stop)
            stop = paths[stop.name][0]
        path.append(start)

        return path[::-1]
    

    def shortest_path(self, start_name:str, end_name:str, start_datetime) -> list[Stop]:
        shortest = self.dijkstra(start_name, end_name, start_datetime, "Shortest")
        print("Shortest : ", shortest)
        return shortest
    
    
    def fastest_path(self, start_name:str, end_name:str, start_datetime) -> list[Stop]:
        fastest = self.dijkstra(start_name, end_name, start_datetime, "Fastest")
        print("Fastest : ", fastest)
        return fastest
    
    
    def foremost_path(self, start_name:str, end_name:str) -> list[Stop]:
        pass