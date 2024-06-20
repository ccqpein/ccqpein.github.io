---
layout: post
title: Re-make my Raspberry Pi system, again.
---

Last year, I wrote a post titled [Re-make my Raspberry Pi after a stupid mistake](https://ccqpein.me/Re-make-my-Raspberry-Pi-after-a-stupid-mistake/). A few days ago, my Raspberry Pi screwed up again, and I had to re-make the system once more.

I mentioned in my last post that a great tutorial ([HackerShackOfficial/Raspberry-Pi-VNC-Mac](https://github.com/HackerShackOfficial/Raspberry-Pi-VNC-Mac)) helped me a lot in setting up the Raspberry Pi to connect with my Mac. Unfortunately, I found that it is a bit outdated now. So, I am writing this post to record what I did and hopefully provide some tips to others.

## VNC ##

Firstly, I needed to install `tightvncserver` like before. We will come back to `tightvncserver` later.

## Netatalk ##

Problems appeared when I tried to install `netatalk`. For some reason, `netatalk` could not be found. So, I had to go to the `netatalk` source code and [install](https://github.com/Netatalk/netatalk/blob/main/INSTALL.md) it locally by myself.

Fortunately, most dependencies can be installed painlessly with `apt`.

Something has changed from before; I needed to create the file `/usr/local/etc/afp.conf` and change its contents to:

```
[Homes]
basedir regex = /home
```

Furthermore, I created the `/etc/systemd/system/netatalk.service` file:

```
[Unit]
Description=Netatalk AFP fileserver for Macintosh clients
After=network.target

[Service]
ExecStart=/usr/local/sbin/netatalk -d
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

After creating the service file, I ran the following systemd commands:

```
sudo systemctl daemon-reload

sudo systemctl enable netatalk

sudo systemctl start netatalk
```

## avahi-daemon ##

`sudo apt install avahi-daemon` is the same as before. I needed to add the file `/etc/avahi/services/afpd.service` with the following content:

```xml
<?xml version="1.0" standalone='no'?><!--*-nxml-*-->
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
   <name replace-wildcards="yes">%h</name>
   <service>
      <type>_afpovertcp._tcp</type>
      <port>548</port>
   </service>
</service-group>
```

And the `/etc/avahi/services/rfb.service`:

```xml
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">%h</name>
  <service>
    <type>_rfb._tcp</type>
    <port>5901</port>
  </service>
</service-group>
```

## Back to VNC ##

I tried to add the `tightvncserver` to systemd, but I failed because of permission problems. It appears that systemd wants it to run as root, but for some reasons, it needs to be run as a user.

So, I created the script `vncserver :1 -geometry 1920x1080 -depth 24` and modified `~/.vnc/xstartup` to:

```
xrdb "$HOME/.Xresources"
startlxde &
```

Otherwise, the screen share would show just a blank grey screen.

## Plex ##

One of my Raspberry Pi's functions is serving as my Plex host server. I installed Plex, and the only thing that stopped me was a permission problem. Plex could not read or write to the user's owned folder, as Plex runs as the `plex` user.

Thanks to someone on Reddit, I learned that I could just change the running user of Plex by adding the following to `/etc/systemd/system/plexmediaserver.service.d/override.conf`:

```
[Service]
User=pi
Group=pi
```

## End ##

That's it. There were a lot of details, dependencies, and configurations. I think I will collect all the setup commands somewhere in case it screws up again in the future.
