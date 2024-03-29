# bl_x1c_bento
A small python program for monitoring the BambuLab X1C and turning the BentoBox on when it is printing

Example build of hardware on INSERT PAGE HERE

## How to use:
### Build hardware
   1. Connect a relay to PIN 17 pn a raspberry pi
   2. Connect fan power to the other side of a transisor

#### Detailed build instructions
https://www.printables.com/model/516646-bambu-lab-x1c-bento-box-fan-controller?fbclid=IwAR3u0gIyjtkez5R3z-f9CspmMOMTlxndO_3BLBmhLX5g-z_dN5bXPZnnJDU

Notes: 
* Using a Gaptec LMO78_05-1.0 DC/DC for converting the 24V to 5V for driving the Raspberry pi

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
cd bl_x1c_bento
cp config_example.py config.py
```
Edit config.py to fit your needs
printer_password can be found in printer menu (will get proper path to this)


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
