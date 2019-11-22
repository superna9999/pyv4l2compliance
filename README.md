# Automated way

## Convert video (video+audio, or video only) files

- mp4/ts with h264

```
./mkhdr.sh /path/to/video.mp4 h264 video.h264.hdr
```

- mp4 with h265

```
./mkhdr.sh /path/to/video.mp4 h265 video.h265.hdr
```

- ts/avi/mpg/mp4 with mpeg1/mpeg2

```
./mkhdr.sh /path/to/video.m2v mpeg2 video.mpeg2.hdr
```

- webm with vp9/vp8

```
./mkhdr.sh /path/to/video.webm vp8 video.vp8.hdr
```

- raw bitstream (264, 265 or m2v)

```
./mkhdr.sh /path/to/video.264 raw video.264.hdr
```
## And run the v4l2-complience test

v4l2-compliance --stream-from-hdr test-25fps.h264.hdr -s250 -d /dev/video1

# Manual Way

## Howto prepare 'sizes' file

ffprobe -show_packets test-25fps.h264 | grep "size=" > test-25fps.h264.sizes

## Use the python script to prepare the .hdr file for v4l2-compliance

python pyhdr.py test-25fps.h264

## And run the v4l2-complience test

v4l2-compliance --stream-from-hdr test-25fps.h264.hdr -s250 -d /dev/video1
