from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class File:
	name: str
	size: int

@dataclass
class Directory:
	name: str
	files: List[File] = field(default_factory=list)
	subdirs: Dict[str, "Directory"] = field(default_factory=dict)
	parent: Optional["Directory"] = None

	def get_size(self) -> int:
		return sum(f.size for f in self.files) + sum(sd.get_size() for sd in self.subdirs.values())

def run(input_data: List[str], **kwargs) -> int:
	current_directory = Directory(name="/")
	all_dirs = [current_directory]
	i = 1
	while i < len(input_data):
		datum = input_data[i]
		if datum.split(" ")[-1] == "ls":
			i += 1
			while i < len(input_data) and not (datum := input_data[i]).startswith("$"):
				if datum.startswith("dir"):
					dir_name = datum.split(" ")[-1]
					new_dir = Directory(dir_name, parent=current_directory)
					current_directory.subdirs[dir_name] = new_dir
					all_dirs.append(new_dir)
				else: 
					size, file_name = datum.split(" ")
					current_directory.files.append(File(file_name, int(size)))
				i += 1
		elif datum.endswith(".."):
			current_directory = current_directory.parent
			i += 1
		else:
			current_directory = current_directory.subdirs[datum.split(" ")[-1]]
			i += 1
	return sum(d.get_size() for d in all_dirs if d.get_size() <= 100000)
