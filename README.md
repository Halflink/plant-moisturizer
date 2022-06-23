# Plant Moisturizer project

## PROJECT
| Project name:    | Halflink/plant-moisturizer |
|------------------|----------------------------|
| Author:          | Jeroen van Zwam            |
| Date:            | 2021-10-25                 |  
| Last update: | 2022-06-19                 |
| Project type:    | Raspberry Pi               |

## Executable
* Start main.py 

## PROJECT DESCRIPTION
This project started with the plants on my balcony needing water every day.
Although the plants are all low- maintenance plants, the location and type of the balcony means they get dry very quick.
To solve this I picked up the idea to create an automated watering system.

### Scope
* Measure moisture levels of plants
* Regular moisturizing of plants
* Check water level in water container
* Air temperature check 
* Browser based interface showing all parameters

### Pi 4 Model B choice
The Pi 3 Model B is still available and might be a cheaper choice. The reason I opted for the Pi4B is that this Pi 
should be able to handle more ampere, and as I plan to use 4-5 sensors, a web service and a relay hat I might need 
that extras.

### DC-DC step-down converter
The pumps need roughly 12 volts to operate properly (I plan to water a lot of plants). The Pi & sensors need a stable 5 volts. 
For this I plan to use a DC-DC step-down converter to create a stable 5 volt for the Pi. 
 
## PI INSTALLATION NOTES
* Connect remotely so we can use the raspberry headless
  * Set up SSH 
  * Set up WIFI
  * Install GIT `sudo apt-get install git`
* I2C for relay HAT:
  * Set up [I2C](https://wiki.52pi.com/index.php?title=DockerPi_4_Channel_Relay_SKU:_EP-0099)
  * Install smbus package for python `sudo apt-get install python3-smbus`
* Use init.json to set up the HAT, GPIO ports etc.
* Set up MCP3008
* Install FLASK `sudo apt-get install python3-flask`

## PARTS LIST*
* 1x Raspberry Pi 4 Model B 2GB RAM
* 1x [MCP3008](https://elektronicavoorjou.nl/product/mcp3008/)
* 1x [Step-down DC-DC Power Converter](https://www.robotshop.com/eu/en/step-down-dc-dc-power-converter-25w.html)
* 1x [4-channel relay hat](https://www.robotshop.com/eu/en/4-channel-relay-hat-raspberry-pi-3b-3b2b.html)
* 1x [Temperature & humidity sensor](https://www.robotshop.com/eu/en/dht22-temperature-humidity-sensor.html)
* 3x [Immersible water pump](https://www.robotshop.com/eu/en/immersible-water-pump-water-tube.html)
* 4x [DFRobot moisture sensor](https://www.robotshop.com/eu/en/dfrobot-moisture-sensor.html)
* Water reservoir (not yet bought)
* watering tubes (not yet bought)
* Housing for raspberry pi & components (not yet bought)

*) Please note that only the major parts are mentioned

## TO DO LIST
* ~~Program relay hat handler~~ 
* ~~Program logging~~
* Program web interface
  * ~~Create moisture chart~~
  * ~~Create buttons to activate pumps~~
  * Create humidity chart
  * Create temperature chart
  * Create current temperature gauge
* Program heartbeat monitoring
  * Set-up e-mail server
* Set-up autostart when booting
* Create enclosure for all the parts
* Create PCB for all electronic parts
* Set up power converter
* Create tubing system and sprinklers
* Create water reservoir
* Find solution for SD card corruption (planning to have a high up-time)

## Progress
### Added relay hat and MCP3008 chip on breadboard
![Alt text](/docs/breadboard_MCP3008.jpg "Added MCP3008")