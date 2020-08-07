import unittest

from main import Station


class TestStation(unittest.TestCase):
    
    def setUp(self):
        mock_routes_list = [
                {
                    "station": ["A", "B"],
                    "time": 3
                },
                {
                    "station": ["B", "C"],
                    "time": 5
                },
                {
                    "station": ["C", "D"],
                    "time": 2
                },
                {
                    "station": ["D", "A"],
                    "time": 4
                },
        ]
        self.sta_mock = Station("A", "C", {"A", "B", "C", "D"}, mock_routes_list)

    def test_set_neighbours(self):
        self.sta_mock.set_neighbours()
        assert self.sta_mock.neighbours == {'B': 3, 'D': 4}

    def test_set_current_station(self):
        self.sta_mock.best_routes = {'D': {'time': 9999, 'prev': None}, 'B': {'time': 9999, 'prev': None}, 'C': {'time': 9999, 'prev': None}, 'A': {'time': 0, 'prev': None}}
        self.sta_mock.set_current_station()
        assert self.sta_mock.current_station == "A"

    def test_set_min_time(self):
        self.sta_mock.neighbours = {'B': 3, 'D': 4}
        self.sta_mock.best_routes = {'D': {'time': 9999, 'prev': None}, 'B': {'time': 9999, 'prev': None}, 'C': {'time': 9999, 'prev': None}, 'A': {'time': 0, 'prev': None}}
        self.sta_mock.set_min_time()
        assert self.sta_mock.best_routes =={'D': {'time': 4, 'prev': 'A'}, 'B': {'time': 3, 'prev': 'A'}, 'C': {'time': 9999, 'prev': None}, 'A': {'time': 0, 'prev': None}}

    def test_get_initail_routes(self):
        assert self.sta_mock.get_initail_routes() == {'D': {'time': 9999, 'prev': None}, 'B': {'time': 9999, 'prev': None}, 'C': {'time': 9999, 'prev': None}, 'A': {'time': 0, 'prev': None}}

    def test_get_count_stops(self):
        self.sta_mock.best_routes = {'A': {'time': 0, 'prev': None}, 'C': {'time': 6, 'prev': 'D'}, 'D': {'time': 4, 'prev': 'A'}, 'B': {'time': 3, 'prev': 'A'}}
        count = self.sta_mock.get_count_stops()
        assert count == 1

    def test_get_best_routes(self):
        assert self.sta_mock.get_best_routes() == {'A': {'time': 0, 'prev': None}, 'C': {'time': 6, 'prev': 'D'}, 'D': {'time': 4, 'prev': 'A'}, 'B': {'time': 3, 'prev': 'A'}}

    def tearDown(self):
        self.sta_mock = None


if __name__ == '__main__':
    unittest.main()
