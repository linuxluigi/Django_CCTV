# Django_CCTV


## Deploy

http://mezzanine.jupo.org/docs/deployment.html?highlight=deploy

**do not install as root user**

```bash
$ pip install fabric
$ fab secure
$ fab install
$ fab deploy
```

# Extra

## Generate Self-Signed Certificate

```bash
$ sudo openssl req -new -x509 -days 365 -nodes -out /usr/local/nginx/conf/cctv.crt -keyout /usr/local/nginx/conf/cctv.key
$ sudo chmod 600 /usr/local/nginx/conf/cctv.crt
$ sudo chmod 600 /usr/local/nginx/conf/cctv.key
```

## SSH

```bash
$ ssh-keygen -R stream.linuxluigi.com
```

```bash
ssh root@stream.linuxluigi.com
adduser fubu
adduser fubu sudo
sed -i 's/%sudo	ALL=(ALL:ALL) ALL/%sudo ALL=NOPASSWD: ALL/g' /etc/sudoers
cp -r /root/.ssh /home/fubu/.ssh
chown -R fubu:fubu /home/fubu/.ssh
```

## Install & use LetsEncrypt

```bash
$ sudo /etc/init.d/nginx stop
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install python-certbot-apache
$ sudo certbot --apache -d stream.linuxluigi.com
```

## Streaming

Stream to server.

```bash
$ avconv -i example/video/Big_Buck_Bunny_360p.mp4 -f flv rtmp://127.0.0.1:1935/mytv/start
```

View stream

```bash
mpv https://207.154.249.112/stream/hls/start.m3u8
```

View Stream information 

```bash
$quvi dump https://207.154.249.112/stream/hls/start.m3u8
```

curl --insecure -i -X OPTIONS -H "Origin: http://207.154.249.112:443" \
    -H 'Access-Control-Request-Method: POST' \
    -H 'Access-Control-Request-Headers: Content-Type, Authorization' \
    "https://207.154.249.112/stream/hls/start.m3u8"
