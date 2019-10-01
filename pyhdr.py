import sys
from scanf import scanf
from struct import pack

stream_name = "test-25fps.h264"
stream_name_sizes = "test-25fps.h264.sizes"
output_filename = "test-25fps.h264.hdr"

if __name__ == "__main__":
	verbose = False

	if len(sys.argv) < 2:
		exit("Need at least one argument")

	stream_name = sys.argv[1]
	stream_name_sizes = stream_name + '.sizes'
	output_filename = stream_name + '.hdr'
	
	try:
		streamfile = open(stream_name, "r")
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

	data = streamfile_sizes.readlines()

	sizes_list = []

	subs = 'size='
	sizes = list(filter(lambda x: subs in x, data))

	for s in sizes:
		__null__, sz = scanf('%s=%u', str(s))
		sizes_list.append(sz)

	for i in range(0, len(sizes_list)):
#		output_file.write(pack("!4s", b"Vhdr"))
		output_file.write(pack("!4s", b"rdhV"))
		
		packet = streamfile.read(sizes_list[i])
		
		output_file.write(pack("!I", sizes_list[i]))
		output_file.write(packet)

		if verbose:
			print len(packet)

	streamfile_sizes.close()
	streamfile.close()
	output_file.close()
