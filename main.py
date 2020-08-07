import csv
import sys
import argparse


class Station:

    def __init__(self, source, destination, all_stations, routes_list):

        self.source = source
        self.destination = destination
        self.all_stations = all_stations
        self.routes_list = routes_list

        self.current_station = source
        self.visited = []
        self.best_routes = None
        self.neighbours = None

    def set_neighbours(self):
        neighbours = dict()
        for path in self.routes_list:
            if self.current_station in path["station"]:
                path["station"].remove(self.current_station)
                neighbours[path["station"][0]] = path["time"]
                path["station"].append(self.current_station)
        self.neighbours = neighbours

    def set_current_station(self):
        next_station = None
        previous = infinity
        for k,v in self.best_routes.items():
            if previous > v["time"] and k not in self.visited:
                next_station = k
            if k not in self.visited:
                previous = v["time"]
        self.visited.append(next_station)
        self.current_station = next_station

    def set_min_time(self):
        for k,v in self.neighbours.items():
            sum_time = self.best_routes[self.current_station]["time"] + v
            if self.best_routes[k]["time"] > sum_time:
                self.best_routes[k]["time"] = sum_time
                self.best_routes[k]["prev"] = self.current_station

    def get_initail_routes(self):
        routes = dict()
        for s in self.all_stations:
            time = infinity
            if s == self.current_station:
                time = 0
            routes[s] = {
                "time": time,
                "prev": None 
            }
        return routes

    def get_best_routes(self):
        self.best_routes = self.get_initail_routes()
        for i in range(len(self.all_stations) - 1):
            self.set_current_station()
            self.set_neighbours()
            self.set_min_time()
            if not self.current_station:
                break
        return self.best_routes

    def get_count_stops(self):
        stops = 0 
        des = self.destination
        for i in range(20):
            if self.best_routes[des]["time"] == infinity:
                return stops
            if self.best_routes[des]["prev"] != self.source:
                stops += 1
                des = self.best_routes[des]["prev"]
            else:
                break
        return stops



def read_routes_file(filename):
    routes_list = []
    all_stations = set()
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            routes_list.append({
                "station": [row[0], row[1]],
                "time": int(row[2])
            })
            all_stations.update([row[0], row[1]])
    return routes_list, all_stations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()                                               
    parser.add_argument("--file", "-f", type=str, required=False)
    args = parser.parse_args()  
    file_name = args.file or "routes.csv"
    routes_list, all_stations = read_routes_file(file_name)

    infinity = 9999
    source = input("What station are you getting on the train?: ").upper()
    destination = input("What station are you getting off the train?: ").upper()

    if source not in all_stations or destination not in all_stations:
        print("Sorry, your input is invalid station :(")
    elif source == destination:
        print("You're on the station you would like to go -_-")
    else:
        st = Station(source, destination, all_stations, routes_list)
        best_routes = st.get_best_routes()
        stop_count = st.get_count_stops()
        if best_routes[destination]["time"] != infinity:
            print(f"Result: Best Routes from {source} -> {destination} takes {best_routes[destination]['time']} minutes, with {stop_count} stops.")
        else:
            print(f"Result: No routes from {source} -> {destination}")
