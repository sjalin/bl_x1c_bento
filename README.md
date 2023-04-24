# bl_x1c_bento
A small python program for monitoring the BambuLab X1C and turning the BentoBox on when it is printing

Example build of hardware on INSERT PAGE HERE

## How to use:
### Build hardware
   1. Connect a relay to PIN 11 pn a raspberry pi
   2. Connect fan power to the other side of the relay
### Install software
run to following
```bash
cd ~
sudo install tmux git
git clone git@github.com:sjalin/bl_x1c_bento.git
pip install -r ./bl_x1c_bento/requirements.txt
touch tmux_start.sh
echo "#!/bin/bash" >> tmux_start.sh
echo "tmux new-session -d -s bento" >> tmux_start.sh
echo "tmux send-keys -t bento 'python projects/bl_x1c_bento/main.py' Enter" >> tmux_start.sh
```

Add the following
```bash
sudo -u pi bash /home/pi/tmux_start.sh &
```
to /etc/rc.local (sudo nano /etc/rc.local), change "pi" to something else if you do not have the standard user

restart
```bash
sudo reboot
```

See that it is working/has started by typing 
```bash
tmux attach
```


## TODO
* Use logging module instead of print