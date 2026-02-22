from railway.station import Station
from railway.route import Railway, Route


"""def test_station():
    station = Station("Minsk")
    assert station.name == "Minsk"
    assert str(station) == "Minsk"


def test_railway():
    first_station = Station("CityA")
    second_station = Station("CityB")
    railway = Railway({first_station, second_station}, 123)
    assert railway.stations == {first_station, second_station}


def test_route():
    first_station = Station("CityA")
    second_station = Station("CityB")
    railway1 = Railway({first_station, second_station}, 123)
    third_station = Station("CityC")
    railway2 = Railway({second_station, third_station}, 124)
    route = Route([railway1, railway2])
    assert route.total_distance == 247
    assert route.railways == [railway1, railway2] """


