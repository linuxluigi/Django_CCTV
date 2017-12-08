#!/bin/sh

# get cam stream and send it in an loop to nginx rtmp server

while true
do
    avconv -y -r 2  -i {{ monitor.stream_source }} \
        -vf "drawtext=fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf':text=%{localtime\}:x=0:y=0:fontsize=24:fontcolor=black" \
        -vcodec libx264 -crf 24 -r 2 -f flv rtmp://localhost/mytv/{{ monitor.stream_key }}
	sleep 5
done