from typing import Dict, List
from enum import Enum

class NodeStatus(Enum):
	AVAILABLE = 0
	BLOCKED = 1
	IN_PROGRESS = 2
	UNLOCKED = 3

class Node:
	def __init__(self, name: str) -> None:
		self.name = name
		self.prereqs = []
		self.deps = []
		self.status = NodeStatus.AVAILABLE

	def add_prereq(self, prereq: str) -> None:
		self.prereqs.append(prereq)
		self.status = NodeStatus.BLOCKED

	def add_dep(self, dep: "Node") -> None:
		self.deps.append(dep)
	
	def clear_prereq(self, dep: str) -> None:
		self.prereqs.remove(dep)
		if not self.prereqs:
			self.status = NodeStatus.AVAILABLE
	
	def claim(self) -> None:
		self.status = NodeStatus.IN_PROGRESS

	def unlock(self) -> None:
		self.status = NodeStatus.UNLOCKED
		for dep in self.deps:
			dep.clear_prereq(self.name)


class Worker:
	def __init__(self) -> None:
		self.working_on: Node = None
		self.available_at = 0
	
	def finish(self) -> None:
		self.working_on.unlock()
		self.working_on = None
	
	def start(self, work_item: Node, finish_time: int) -> None:
		work_item.claim()
		self.working_on = work_item
		self.available_at = finish_time


def run(input_data: List[str], **kwargs) -> int:
	is_test = kwargs["is_test"]
	num_workers = 2 if is_test else 5
	base_unlock_time = 0 if is_test else 60
	
	nodes: Dict[str, Node] = {}
	for req in input_data:
		prereq = nodes.setdefault(req[5], Node(req[5]))
		dep = nodes.setdefault(req[36], Node(req[36]))
		dep.add_prereq(prereq.name)
		prereq.add_dep(dep)
	all_tasks = sorted(nodes.values(), key=lambda t: t.name)
	
	workers = [Worker() for _ in range(num_workers)]
	current_time = 0
	while [n for n in all_tasks if n.status != NodeStatus.UNLOCKED]:
		workers.sort(key=lambda w: w.available_at)
		available_tasks = [
			t for t in all_tasks if t.status == NodeStatus.AVAILABLE
		]
		available_workers = [
			w for w in workers if w.available_at <= current_time
		] 
		
		if not available_tasks or not available_workers:
			next_finished_worker = next(
				w for w in workers if w.working_on
			)
			current_time = next_finished_worker.available_at
			next_finished_worker.finish()
			continue
		
		next_task = available_tasks[0]
		next_worker = available_workers[0]
		time_finished_task = (
			current_time 
			+ base_unlock_time 
			+ ord(next_task.name) 
			- 64
		)
		next_worker.start(next_task, time_finished_task)

	return current_time