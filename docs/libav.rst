======================
LibAV Shell Examples
======================

Here some Libav shell code examples::

    # Stream a video to rtmp ngix server
    avconv -i example/video/Big_Buck_Bunny_360p.mp4 -f flv rtmp://localhost/mytv/bigbuckbunny

    # capture cam stream & send it to the ngix rtmp server
    avconv -y -c:v mjpeg -i http://user:pass@yourcam_ip:80/video.cgi -vcodec libx264 -crf 24 -r 2 -f flv rtmp://localhost/mytv/yourcam

