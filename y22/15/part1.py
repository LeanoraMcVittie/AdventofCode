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
	
	test_row = 10 if is_test else 2000000
	in_range = []
	for i in range(len(sensors)):
		sensor = sensors[i]
		m_dist = m_dists[i]
		if test_row in range(sensor.y - m_dist, sensor.y + m_dist + 1):
			in_range.append(i)
	
	min_x = min(c.x for c in sensors + beacons)
	max_x = max(c.x for c in sensors + beacons)
	count = 0
	for x in range(min_x, max_x+1):
		if Coord(x, test_row) in beacons:
			continue
		for i in in_range:
			sensor = sensors[i]
			m_dist = m_dists[i]
			a = abs(x - sensor.x)
			b = abs(test_row - sensor.y)
			c = a + b
			if c <= m_dist:
				count += 1
				break
	return count