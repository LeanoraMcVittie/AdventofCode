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
	_size: Optional[int] = None

	@property
	def size(self) -> int:
		if self._size is None:
			self._size = sum(f.size for f in self.files) + sum(sd.size for sd in self.subdirs.values())
		return self._size

def run(input_data: List[str], **kwargs) -> int:
	current_directory = Directory(name="/")
	all_dirs = [current_directory]
	i = 1
	while i < len(input_data):
		datum = input_data[i]
		i += 1
		if datum.split()[-1] == "ls":
			while i < len(input_data) and not (datum := input_data[i]).startswith("$"):
				if datum.startswith("dir"):
					dir_name = datum.split()[-1]
					new_dir = Directory(dir_name, parent=current_directory)
					current_directory.subdirs[dir_name] = new_dir
					all_dirs.append(new_dir)
				else: 
					size, file_name = datum.split()
					current_directory.files.append(File(file_name, int(size)))
				i += 1
		elif datum.endswith(".."):
			current_directory = current_directory.parent
		else:
			current_directory = current_directory.subdirs[datum.split()[-1]]
	return sum(d.size for d in all_dirs if d.size <= 100000)
