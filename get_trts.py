import avb
import sys, pathlib, datetime
from posttools.timecode import Timecode

def get_latest_sequence(bin:avb.file.AVBFile):
	"""Get the most recent sequence from a given bin"""

	return next(bin.toplevel())

def main():
	"""Main program"""

	if len(sys.argv) < 2:
		sys.exit(f"Usage: {pathlib.Path(__file__).name} path_to_bin.avb [another_bin.avb ...]")

	padding = max(len(pathlib.Path(path_bin).name) for path_bin in sys.argv[1:])

	durations = list()

	print("")
	
	for path_bin in sys.argv[1:]:
		with avb.open(path_bin) as file_bin:
			seq = get_latest_sequence(file_bin.content)

			prev_seq_count = len(durations)

			tc_head = Timecode("8:00")
			tc_tail = Timecode("3:23")

			if prev_seq_count == 0:
				tc_head = Timecode("32:21")
			elif prev_seq_count == 8:
				tc_tail = Timecode("9:19:09")

			durations.append(Timecode(seq.length, seq.edit_rate) - tc_head - tc_tail)
			print(f"{pathlib.Path(path_bin).name.ljust(padding+1)}:     Latest Sequence: {seq.name}     Date: {seq.creation_time}     Duration: {durations[-1]+tc_head+tc_tail}     Head: {tc_head}     Tail: {tc_tail}     Adjusted TRT: {durations[-1]}")
		
	print("")
	print(f"Total reels: {len(durations)}     TRT: {sum(durations, Timecode(0, durations[0].rate))}")
	print("")

if __name__ == "__main__":

	main()