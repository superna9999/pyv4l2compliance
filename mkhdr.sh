#!/bin/sh

set -e

if [ $# -lt 3 ]; then
	echo "Usage: $0 <source file> <format> <dest video header file>"
	exit 1
fi

TMP=`mktemp -d -p $PWD`
OFF=0

case $2 in
	raw)
		cp $1 $TMP/raw
		;;
	h264)
		ffmpeg -i $1 -c:v copy -bsf h264_mp4toannexb $TMP/raw.h264
		mv $TMP/raw.h264 $TMP/raw
		;;
	hevc)
		ffmpeg -i $1 -c:v copy -bsf hevc_mp4toannexb $TMP/raw.h265
		mv $TMP/raw.h265 $TMP/raw
		;;
	mpeg[12])
		ffmpeg -i $1 -c:v copy $TMP/raw.m2v
		mv $TMP/raw.m2v $TMP/raw
		;;
	vp8)
		ffmpeg -i $1 -c:v copy $TMP/raw.ivf
		mv $TMP/raw.ivf $TMP/raw
		;;
	vp9)
		ffmpeg -i $1 -c:v copy $TMP/raw.ivf
		mv $TMP/raw.ivf $TMP/raw
		OFF=44
		;;
	*)
		rm -fr $TMP
		echo "Invalid format (valid raw, h264, hevc, mpeg1, mpeg2, ivf)"
		exit 1
esac

ffprobe -show_packets $TMP/raw | grep "size=" > $TMP/raw.sizes

./pyhdr.py $TMP/raw $OFF

cp $TMP/raw.hdr $3

#rm -fr $TMP

exit 0
