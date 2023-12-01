from typing import List
from datetime import datetime
from collections import Counter, defaultdict
import re

def run(input_data: List[str], **kwargs) -> int:
	input_data.sort(
		key=lambda k: datetime.strptime(k[1:17], "%Y-%m-%d %H:%M")
	)
	guard_num = None
	guard_sleep_log = defaultdict(list)
	for log in input_data:
		date = datetime.strptime(log[1:17], "%Y-%m-%d %H:%M")
		if "Guard" in log:
			guard_num = int(re.match(".*#([0-9]+).*", log)[1])
			continue
		if "falls asleep" in log:
			start_min = date.minute
			continue
		if "wakes up" in log:
			guard_sleep_log[guard_num].extend(
				range(start_min, date.minute)
			)
			continue
		raise Exception("strangely formatted input")

	guard_asleep_longest = None
	total_mins_asleep = 0
	for guard, sleep_log in guard_sleep_log.items():
		if len(sleep_log) > total_mins_asleep: 
			total_mins_asleep = len(sleep_log)
			guard_asleep_longest = guard

	mode_min = Counter(
		guard_sleep_log[guard_asleep_longest]
	).most_common(1)[0][0]
	return guard_asleep_longest * mode_min
		

		
