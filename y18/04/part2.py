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

	guard_predictably_asleep = None
	min_predictably_asleep = None
	days_predictably_asleep = 0
	for guard, sleep_log in guard_sleep_log.items():
		most_asleep = Counter(sleep_log).most_common()[0]
		if most_asleep[1] > days_predictably_asleep:
			days_predictably_asleep = most_asleep[1]
			guard_predictably_asleep = guard
			min_predictably_asleep = most_asleep[0]
	
	return guard_predictably_asleep * min_predictably_asleep
