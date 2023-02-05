---
layout: post
title: Re-make my Raspberry Pi after a stupid mistake
---

I was trying to play around using my local mac emacs slime to connect the swank server on my raspberry pi. Initially, it cannot work, but I use the ssh tunnel to forward the ports to make it work. However, I try to figure out why it cannot connect directly. It is because the raspberry pi doesn't open the port. 

So I installed the `ufw` and added the port `4005` (swank default port) to rule, then `sudo ufw enable`, then restarted the raspberry pi, then I lost my permission of ssh because the port `22` doesn't open. It is an extremely stupid mistake. 

## Try to solve the problem first ##

The easiest way is to connect a keyboard, a mouse, and a monitor. Unfortunately, I don't have a micro HDMI for the monitor, either a mouse or a keyboard. 

### mount the SD card to  macOS ###

So I was thinking if I could mount the SD card to my mac and change the ufw rules located in `/etc/ufw/user.rules`. However, I need to install the macfuse and ext4fuse to mount the ext4 file system which my raspberry pi is using. 

Furthermore, ext4fuse cannot install through homebrew. So I find this [repo](https://github.com/gerard/ext4fuse) and built it in my local. And need to restart to change the kernel extension preference in safe mode for using the macfuse.

After all these operations, `sudo ./ext4fuse /dev/disk6s2 ~/Desktop/rasberry-pi -o allow_other,rw` to mount the SD card file system to `~/Desktop/rasberry-pi`.

But, the `,rw` is unnecessary because the file system is read-only. It is sad that I saw the config file but cannot change it.

## Re-make raspberry pi system ##

Looks like I have to re-make my raspberry pi system. Luckily, raspberry pi has a very easy management app to re-make the whole system. This is the official document: https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system

The thing is, in advanced options, I can init setting the ssh, hostname, username, password, and wifi. I don't remember they being there in 2019 (the time I bought this raspberry pi), but it is very convenient it has.

### ufw first ###

This time I do the ufw first in case something is wrong again, then I can re-make the system again without losing a lot of work. 

My raspberry pi is hosted inside the intern network in my home, so I can run `sudo ufw allow from 192.168.0.0/16` to achieve it. 

### some packages ###

Then I need to install some packages I would like to use. Emacs, zsh, etc.

### VNC ###

The major usage of my raspberry pi is becoming my disk mounting point and plex server. Back in 2019, I found an amazing tutorial that made the connection between raspberry pi and mac. Here is the link: https://github.com/HackerShackOfficial/Raspberry-Pi-VNC-Mac

The only thing that needs to worry about is the `netatalk` might changes its configuration in 2019. I keep getting the 

> There are no shares available or you are not allowed to access them on the server. 

when I try to connect it. 

After some search, I just need to change (un-comment) the configuration of `netatalk` 

```
[Homes]
basedir regex = /home
```

Then the connection is good.
