# SDN supporting PFCP for 5G Networks

Key words: Software Defined Networking (SDN) | 5G | Python | Flask | OpenAirInterface (OAI) | PFCP 

### Short description of the project:
Packet Forwarding Control Protocol (PFCP) is a 3GPP protocol used between the control plane and the user plane function to manage the user traffic. It is one of the main protocols introduced in the 5G Next Generation Core Network, but also used in the 4G/LTE EPC to implement the Control and User Plane Separation (CUPS). PFCP is used by the Serving Gateway Control plane to control the Serving Gateway User plane. It is similar to OpenFlow, which is used in Software Defined Networking (SDN). The latter is a new trend on networking, where the data plane is separated from the control plane; a centralized controller is used to manage the network elements using Southbound API, such as OpenFlow. On the other hand, the Northbound API exposed by the controller, is used to allow remote applications to control the forwarding elements of the data plane.

The content of the project is a SDN controller that is able to communicate with the remote user plane elements via the PFCP protocol.

### Project Structure

    .
    ├── pfcp5g                                       
    │   ├── ...
    │   ├── app                 
    │   │   ├── ...
    │   │   ├── TLV.py                 # Parsing library
    │   │   ├── models.py              # Define the database structure
    │   │   ├── pfcp.py                # Class for the pfcp packets
    │   │   ├── pfcp_types.py          # Define all pfcp message types and information element types
    │   │   ├── request_handler.py     # Handle received pfcp requests  
    │   │   ├── routes.py              # Northbound functions (flask server REST API)
    │   │   ├── sdn5g.db               # File of Alchemy local database
    │   │   ├── utils.py               # Utilities functions
    │   │   └──...
    │   ├── dropAll.py                 # Purg the local database
    │   ├── pfcp5g.py                  # Flask application file 
    │   ├── showAssociations.py        # Display associations in the database using python CLI
    │   ├── showSessions.py            # Display sessions in the database CLI
    │   └── ...
    ├── spgw_u.conf                    # SPGW_U configuration file
    └── README.md


### Installation of the Open Air Interface SPGW-U:
1. Install python 3.7 :
```cmd
$ sudo apt install python3.7
```
2. Install a new alternative to python pointing to Python3.7 installed in the previous setup. This setup should be followed only in case the current version of python that is installed in your computer is not compliant with the software:
```cmd
$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
```
3. Use the alternative installed :
```cmd
$ sudo update-alternatives --config python
```
4. Clone the git of the Open Air Interface ( « develop » Branch ) :
```cmd
$ git clone https://github.com/OPENAIRINTERFACE/openair-cn-cups.git
```
5. Install fmt Library :
```cmd
$ git clone https://github.com/fmtlib/fmt.git
$ cd fmt
$ cmake .
$ make
$ sudo make install
```

6. Install the SPGWU’s  dependencies by using the script « build_spgwu »  with option “ –I “:
```cmd
$ cd openair-cn-cups/build/scripts
$ ./build_spgwu –I
```
Accept the installation of all the dependencies.<br>
7. Build the spgwu with the same script without any option :
```cmd
$ ./build_spgwu
```
8. Now  to start the SPGWU, get the configuration file “ spgw_u.conf ”. And run the following commande from where you put the spgw_u.conf file :
```cmd
$ sudo spgwu –c spgw_u.conf
```
The SPGWU now should be running on the address 127.0.0.2 and listening on the port 8805 which is the PFCP Port (You should set those values in the configuration file)

### Installation of 5G SDN Controller:
1. Download the 5G SDN Controller and extract the zip
2. Install the flask server
```cmd
$ sudo apt install python3-flask
$ export FLASK_APP=~/pfcp5g/pfcp5g.py ( change this to the path of the file pfcp5g.py )
```
NB : this line needs to be done at every restart of the machine, to avoid doing it every time, add the line to the end of the file ~/.bashrc
3. Install pip3 to install the Python3 libraries needed :
```cmd
$ sudo apt install python3-pip
```
4. Install any other python3 missing libraries using pip3 like: <br>
- flask_sqlalchemy <br>

OR

- Any other missing library  <br>

Using:
```cmd
$ sudo pip3 install [LIBRARY_NAME]
```
### Installation of Postman :
1. Install Postman using snap :
```cmd
$ sudo snap install postman 
```

### Run the controller and the SPGW-U
You need to run the SDN controller **first** and then the SPGW-U. This happens because the SPGW-U as soon as it is up and running, sends an association request to the controller. <br>
Remember : <br>
	To run the SDN Controller:
  ```cmd
  $ flask run
  ```
To run the SPGW-U: 

  ```cmd
  $ sudo spgwu –c spgw_u.conf
   ```
In order to test the different functionalities of the controller, you should provide the elements that are required for each method.<br>
For example, if you want to send a heartbeat to the SPGW-U, you should only include the IP address of the SPGW-U. The expected JSONs are stated above each method, insides the routes.py file.


### Authors:
- [PAPAGORA Niki](https://www.linkedin.com/in/niki-papagora-467b5b184/)
- [ALIOUI Dhiaeddine](https://www.linkedin.com/in/dhiaeddine-alioui/)
- [BOUAOUN Radhwen](https://www.linkedin.com/in/radhwen-bouaoun/)

# SDN-5G
