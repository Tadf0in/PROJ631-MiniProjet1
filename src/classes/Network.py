import os
from ..data2dict import get_data
from .Line import Line
from .Stop import Stop
from datetime import datetime


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
        stops.sort(key=lambda stop: stop.name)
                
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
        paths = {stop.name: (None, float('inf'), float('inf'), datetime.max) for stop in unvisited}
        paths[start.name] = (start, 0, 0, start_datetime) # (stop, nb_arcs (shortest), tps trajet (fastest), datetime arrivée (foremost))
        
        # L'aglorithme va déterminer sur quel critère on se base pour prendre le minimum
        index_algos = {
            "Shortest": 1,
            "Fastest": 2,
            "Foremost": 3
        }
        index_algo = index_algos[algorithm]             
        
        # Calcule les distances
        while len(unvisited) > 0:
            # On choisit le prochain noeud avec la plus petite distance
            current = min(unvisited, key=lambda stop: paths[stop.name][index_algo])
                        
            if paths[current.name][index_algo] == float('inf'):
                return None # Pas de chemin
            
            # Si destination atteinte on s'arrête
            if current == end:
                break
            
            # Met à jour les distances
            for linked_stop, line in current.previous + current.next:
                
                # Si arrêt déjà visiter on skip
                if linked_stop not in unvisited:
                    continue
                
                # Calcule le nouveau nb d'arcs
                current_nb_edges = paths[current.name][index_algos['Shortest']]
                new_nb_edges = current_nb_edges + 1
                
                # Calcul la nouvelle heure d'arrivée
                current_datetime = paths[current.name][index_algos["Foremost"]]
                current_wait_datetime, new_datetime = current.getArrivalHoraire(linked_stop, current_datetime)
                
                # Calcule le nouveau temps de trajet
                travel_time = int((new_datetime - current_wait_datetime).total_seconds() / 60)
                wait_time = int((current_wait_datetime - current_datetime).total_seconds() / 60)
                current_time = paths[current.name][index_algos['Fastest']]
                new_time = current_time + travel_time
                if current != start:
                    new_time += wait_time
                
                # Si plus petit sur le critère de l'algo alors on remplace
                new_weight = (current, new_nb_edges, new_time, new_datetime)
                if new_weight[index_algo] < paths[linked_stop.name][index_algo]:
                    paths[linked_stop.name] = new_weight
                    
                # Ambiguïté si même distance -> regarde autre critère
                elif algorithm == "Fastest" and new_weight[index_algos['Fastest']] == paths[linked_stop.name][index_algos['Fastest']]:
                    if new_weight[index_algos['Foremost']] < paths[linked_stop.name][index_algos['Foremost']]:
                        paths[linked_stop.name] = new_weight
                    
            unvisited.remove(current)        
                
        # Récupère le plus court chemin
        path = []
        stop = end
        while stop and stop != start:
            path_stop = paths[stop.name]
            path.append((stop, *path_stop[1:]))
            stop = path_stop[0]
        path.append((start, *paths[start.name][1:]))

        return path[::-1]