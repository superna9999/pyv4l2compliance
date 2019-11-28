#!/usr/bin/env python3
import sys
from struct import pack

stream_name = "test-25fps.h264"
stream_name_sizes = "test-25fps.h264.sizes"
output_filename = "test-25fps.h264.hdr"

if __name__ == "__main__":
	verbose = False

	if len(sys.argv) < 2:
		exit("Need at least one argument")
	
	if len(sys.argv) > 2:
		offset = int(sys.argv[2])
	else:
		offset = 0

	stream_name = sys.argv[1]
	stream_name_sizes = stream_name + '.sizes'
	output_filename = stream_name + '.hdr'
	
	try:
		streamfile = open(stream_name, "rb")
	except IOError:
		exit("Can't open %s" % stream_name)
	
	try:
		streamfile_sizes = open(stream_name_sizes, "r")
	except IOError:
		exit("Can't open %s" % stream_name_sizes)
	
	try:
		output_file = open(output_filename, "wb")
	except IOError:
		exit("Can't open %s" % output_filename)

	streamfile.seek(offset)

	data = streamfile_sizes.readlines()

	sizes_list = []

	subs = 'size='
	sizes = list([x for x in data if subs in x])

	for s in sizes:
		sz = s.split("=")[1].split("\n")
		sizes_list.append(int(sz[0]))

	for i in range(0, len(sizes_list)):
		output_file.write(pack("!4s", b"rdhV"))
		
		packet = streamfile.read(int(sizes_list[i]))
		
		output_file.write(pack("!I", sizes_list[i]))
		output_file.write(packet)

		if verbose:
			print(len(packet))

	streamfile_sizes.close()
	streamfile.close()
	output_file.close()
