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
            line = Line(line_name, data)
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
    
    # def dijkstra(self, start: str, end: str) -> list[str]:
    #     # Create a dictionary to store the shortest path to each stop
    #     shortest_paths = {stop: (None, float('inf')) for stop in self.getAllStops()}
    #     current_stop = self.getStop(start)
    #     shortest_paths[current_stop] = (None, 0)
    #     visited = set()
    #     priority_queue = [(0, current_stop)]

    #     while priority_queue:
    #         current_distance, current_stop = heapq.heappop(priority_queue)
    #         visited.add(current_stop)

    #         if current_stop.name == end:
    #             break

    #         for next_stop in current_stop.next:
    #             weight = 1  # Assuming each stop has equal weight
    #             distance = current_distance + weight

    #             if next_stop not in visited:
    #                 old_cost = shortest_paths[next_stop][1]
    #                 if distance < old_cost:
    #                     shortest_paths[next_stop] = (current_stop, distance)
    #                     heapq.heappush(priority_queue, (distance, next_stop))

    #     path = []
    #     stop = self.getStop(end)
    #     while stop:
    #         path.append(stop.name)
    #         next_stop = shortest_paths[stop][0]
    #         stop = next_stop

    #     return path[::-1]

    # def getStop(self, name: str) -> Stop:
    #     for stop in self.getAllStops():
    #         if stop.name == name:
    #             return stop
    #     return None

    def shortest_path(self, start:str, end:str) -> list[str]:
        pass
    
    
    def fastest_path(self, start:str, end:str) -> list[str]:
        pass
    
    
    def foremost_path(self, start:str, end:str) -> list[str]:
        pass