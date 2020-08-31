#Key logger
To change the MAC address of a network interface, you need to install
the module pynput by typing on command line:
```
pip3 install argparse termcolor
```
To run the program, you need to type for example this command on bash:
```bash
sudo python3 mac_changer.py -i eth0 -hw 00:11:22:33:44:55 
```
To check which parameters you can insert, you can type the command:
```bash
sudo python3 mac_changer.py --help 
```
An example of output of the command is shown in the following image:
![output](output.png)
