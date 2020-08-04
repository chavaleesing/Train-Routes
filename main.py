import csv

paths = []
all_stations = set()
all_source = set()
all_destination = set()
shortest_path = {}
with open('routes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        paths.append(row)
        all_stations.add(row[0])
        all_stations.add(row[1])
        all_source.add(row[0])
        all_destination.add(row[1])

all_stations2 =  ["A","B","C","D","E","F","G","H","I","J"]
# station = all_stations.pop()
# station="A"
# all_stations.remove(station)

for station in all_stations2:
    all_stations.remove(station)
    temp = dict()

    for st in all_stations2:
        if st != station:
            temp[st] = 999

    visited = [station]
    print()

    def find_by_source(st, tt=0):
        for src, des, time in paths:
            time = int(time)
            new_time = tt+time
            if src == st and des not in visited:
                try:
                    old_time = temp[des]
                except:
                    old_time = 999
                if new_time <= old_time:
                    temp[des] = new_time
            elif des == st and src not in visited:
                try:
                    old_time = temp[src]
                except:
                    old_time = 999
                if new_time <= old_time:
                    temp[src] = new_time

    def find_next():
        min_time = 999
        for k,v in temp.items():
            if v < min_time and k not in visited:
                min_time = v
        # min_time = min(temp.values())
        next_station = None
        for k,v in temp.items():
            if v == min_time and k not in visited:
                next_station = k
        return next_station, min_time


    find_by_source(station)
    next_station, min_time = find_next()
    visited.append(station)

    for i in range(len(all_stations2)):
        find_by_source(next_station, min_time)
        visited.append(next_station)
        next_station, min_time = find_next()

    print(f"{station}: {temp}")
    shortest_path[station] = temp
# print(shortest_path)
# print(paths)

