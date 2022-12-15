from typing import List
from utils.field.two_d import Coord

def run(input_data: List[str], is_test, **kwargs) -> int:
	sensors = []
	beacons = []
	for d in input_data:
		sensor_str, beacon_str = d.split(": ")
		_, _, xstr, ystr = sensor_str.split()
		sensors.append(Coord(*[int(s[2:]) for s in [xstr[:-1], ystr]]))
		xstr, ystr = beacon_str.split()[-2:]
		beacons.append(Coord(*[int(s[2:]) for s in [xstr[:-1], ystr]]))

	m_dists = []
	for i in range(len(sensors)):
		sensor = sensors[i]
		beacon = beacons[i]
		a = abs(sensor.x - beacon.x)
		b = abs(sensor.y - beacon.y)
		c = a + b
		m_dists.append(c)
	
	size = 20 if is_test else 4000000
	def check(coord: Coord) -> bool:
		if (
			coord.x < 0 or coord.y < 0
		 	or coord.x > size or coord.y > size
		):
			return False
		if coord in beacons:
			return False
		for k in range(len(sensors)):
			sensor = sensors[k]
			m_dist = m_dists[k]
			a = abs(coord.x - sensor.x)
			b = abs(coord.y - sensor.y)
			c = a + b
			if c <= m_dist:
				return False
		return True
	
	for i in range(len(sensors)):
		sensor = sensors[i]
		outer = m_dists[i] + 1
		for j in range(outer + 1):
			if (
				check(coord := Coord(sensor.x - j, sensor.y + (outer - j)))
		       	or check(coord := Coord(sensor.x - j, sensor.y - (outer - j)))
				or (j > 0 and check(coord := Coord(sensor.x + j, sensor.y + (outer - j))))
				or (j > 0 and check(coord := Coord(sensor.x + j, sensor.y - (outer - j))))
			):
				return (coord.x*4000000) + coord.y