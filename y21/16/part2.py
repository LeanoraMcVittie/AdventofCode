from typing import List, Tuple
from utils.math import product


class Packet:
	def __init__(self) -> None:
		self.version = None
		self.type_id = None
		self.subpackets = []
		self.value = None

	def calculate(self) -> int:
		return {
			4: lambda _: self.value,
			0: lambda sps: sum(sp.calculate() for sp in sps),
			1: lambda sps: product(sp.calculate() for sp in sps),
			2: lambda sps: min(sp.calculate() for sp in sps),
			3: lambda sps: max(sp.calculate() for sp in sps),
			5: lambda sps: 1 if sps[0].calculate() > sps[1].calculate() else 0,
			6: lambda sps: 1 if sps[0].calculate() < sps[1].calculate() else 0,
			7: lambda sps: 1 if sps[0].calculate() == sps[1].calculate() else 0,
		}[self.type_id](self.subpackets)


class Message:
	packets = []
	def __init__(self) -> None:
		pass
	
	def parse_packets(self, bin_str) -> Tuple[int, Packet]:
		packet = Packet()
		packet.version = int(bin_str[:3], base=2)
		packet.type_id = int(bin_str[3:6], base=2)

		if packet.type_id == 4:
			index = 6
			read_next = True
			value_bin_str = ""
			while read_next:
				value_bin_str += bin_str[index+1:index+5]
				if bin_str[index] == "0":
					read_next = False
				index += 5
			packet.value = int(value_bin_str, base=2)
		else:
			if bin_str[6] == "0": 
				total_subpackets_len = int(bin_str[7:22], base=2)
				subpackets_end = 22 + total_subpackets_len
				index = 22
				while index < subpackets_end:
					try:
						index_increase, subpacket = self.parse_packets(bin_str[index:])
					except ParsingError:
						import pdb; pdb.set_trace()
					packet.subpackets.append(subpacket)
					index += index_increase
				if index != subpackets_end:
					raise Exception("index should match end of subpackets")
			elif bin_str[6] == "1":
				total_subpackets_count = int(bin_str[7:18], base=2)
				index = 18
				for _ in range(total_subpackets_count):
					try:
						index_increase, subpacket = self.parse_packets(bin_str[index:])
					except ParsingError:
						import pdb; pdb.set_trace()
					index += index_increase
					packet.subpackets.append(subpacket)
			else: raise Exception("not possible for binary")

		Message.packets.append(packet)
		return index, packet


def run(input_data: List[str]) -> int:
	bin_str = str(bin(int(input_data[0], base=16)))[2:].zfill(len(input_data[0])*4)
	Message.packets = []
	_, packet = Message().parse_packets(bin_str)
	return packet.calculate()
