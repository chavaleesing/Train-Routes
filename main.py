import csv
import pprint

paths = []
with open('routes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        paths.append({
            "station": [row[0], row[1]],
            "time": int(row[2])
        })

class Station:

    def __init__(self, name):
        self.source = name
        self.name = name
        self.neighbours = None
        self.all_stations = self.get_all_stations(paths)
        self.visited = []
        self.routes = self.initail_routes()

    def get_neighbours(self):
        neighbours = dict()
        for path in paths:
            if self.name in path["station"]:
                path["station"].remove(self.name)
                neighbours[path["station"][0]] = path["time"]
                path["station"].append(self.name)
        # print(neighbours)
        self.neighbours = neighbours
        return neighbours

    def initail_routes(self):
        routes = dict()
        infinite = 999
        for s in self.all_stations:
            routes[s] = {
                "time": infinite,
                "prev": None 
            }
            if s == self.name:
                routes[s] = {
                "time": 0,
                "prev": None 
            }
        return routes

    def find_next_station(self):
        next_station = None
        previous = 999
        for k,v in self.routes.items():
            if previous > v["time"] and k not in self.visited:
                next_station = k
            if k not in self.visited:
                previous = v["time"]
        # print(f"next_station: {next_station}")
        self.visited.append(next_station)
        self.name = next_station

    def replace_with_min_time(self):
        for k,v in self.neighbours.items():
            sum_time = self.routes[self.name]["time"] + v
            if self.routes[k]["time"] > sum_time:
                self.routes[k]["time"] = sum_time
                self.routes[k]["prev"] = self.name

    def get_all_stations(self, paths):
        all_stations = set()
        for path in paths:
            all_stations.update(path["station"])
        # print(f"all_stations = {all_stations}, {len(all_stations)}")
        all_stations = list(all_stations)
        all_stations.sort()
        return all_stations


def shortest_path(source):
    s1 = Station(source)
    s1.initail_routes()
    for r in range(len(s1.routes)-1):
        s1.find_next_station()
        s1.get_neighbours()
        s1.replace_with_min_time()
        if not s1.name:
            break
    # pprint.pprint(s1.routes)
    return s1.routes

def count_stops(routes, src, des):
    stops = 0 
    for i in range(20):
        if routes[des]["time"] == 999:
            return stops
        if routes[des]["prev"] != src:
            stops += 1
            des = routes[des]["prev"]
        else:
            break
    return stops

infinity = 999
source = input("What station are you getting on the train?: ").upper()
destination = input("What station are you getting off the train?: ").upper()

routes = shortest_path(source)
stop_count = count_stops(routes, source, destination)
if routes[destination]["time"] != infinity:
    print(f"Result: Best Routes from {source} -> {destination} takes {routes[destination]['time']}, with {stop_count} stops.")
else:
    print(f"Result: No routes from {source} -> {destination}")
