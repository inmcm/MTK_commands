# MTK_commands
Python based Generator of MTK Command Sentences for the MTK33X9 GPS Chipset

This small module can be used to easily generated the command and control sentences for the MediaTek MTK3329 and MTK3339
GPS chipsets. This chipset is used a wide array of popular GPS modules and breakouts including:

* [Adafruit Ultimate GPS Breakout]
* [Digilent PmodGPS]
* [Sparkfun GPS Receiver LS20031]
* [43oh MTK3339 GPS Launchpad Boosterpack]


Static sentences and dynamic sentence generation rules were taken from the Globaltop module [datasheet] supplied by Adafruit.
Not all sentences are supported currently. More sentences may be added by request or via pull request.

This module is created for use with [Micropython] and my GPS parsing library [micropyGPS]. It can be used, though, with any Python 2/3
setup to generate needed sentences. Examples given below assume you are running on a pyboard. These commands have been test on the Adafruit Ultimate GPS breakout

## Usage

To use, just copy the file into your project and import it

```sh
>>> import mtk
```

Several static sentences are provided:

```python
>>> mtk.cold_start
'$PMTK103*30\r\n'
>>> mtk.default_sentences
'$PMTK314,-1*04\r\n'
>>> mtk.hot_start
'$PMTK101*32\r\n'
>>> mtk.warm_start
'$PMTK102*31\r\n'
>>> mtk.full_cold_start
'$PMTK104*37\r\n'
>>> mtk.standby
'$PMTK161,0*28\r\n'
```

The main functions currently provided are the ability to generate proper command sentences to the output update rate and serial port baud rate

```python
>>> mtk.update_nmea_rate(2) # Set update rate to 2Hz
'$PMTK220,500*2b\r\n'
>>> mtk.update_baudrate(38400) # Set output baudrate to 38400bps
'$PMTK251,38400*27\r\n'
```

**NOTE:** The update rate and baud rate changes take effect immediately after the command is issued. You'll need to reinitialize your serial port to the new baud rate right after you issue the command

You can also generate a command sentence to alter which NMEA sentences are outputed and how often using `update_sentences()`. By default, all the standard NMEA sentences are enabled with an update interval of 1 except GSV sentences. You can easily disable sentences and adjust their updates rates:

```python
# Disable GGA,GSA,and GSV sentences. Set VTG update interval to 3
>>> mtk.update_sentences(en_gga=False,en_gsv=False,en_gsa=False,vtg_int=3)
'$PMTK314,1,1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*2b\r\n'
```

Reply and status commands from the GPS module can be parsed using the *MtkCommandRx* object. The `update()` method accepts serial characters and returns the PMTK sentence when a valid one is recieved.
```python
>>> from mtk import *
>>> ack_test = '$PMTK001,604,3*32\r\n'
>>> my_test = MtkCommandRx()
>>> for char in ack_test:
...    result = my_test.update(char) 
...    if result:
...         print('Found Sentence:', result)       
...         
Found Sentence: PMTK001,604,3*32
```

The following example can used on the [pyboard] to disable all sentences but RMC, set the update rate to 10Hz, and finally change the baudrate to 115200bps
```python
>>> from pyb import UART
>>> import mtk
>>> from mtk import *
>>> 
>>> baud = 9600
# Start UART Assuming 9600bps default
>>> uart = UART(3, baud)
>>> 
# Initialize Command Checker
>>> mtk_chk = MtkCommandRx()
>>> 
# Turn off all Sentences but RMC
>>> uart.write(mtk.update_sentences(en_gga=False,en_gsv=False,en_gsa=False,en_vtg=False,en_gll=False))
>>> 
# Check for Confirmation Command
>>> result = None
>>> while not result:
...     while uart.any():
...         result = mtk_chk.update(chr(uart.readchar()))
...			if result:
...				if result[-4] == '3':
...					print('Command Succeded:', result)
...					break
>>> 
# Set Update Rate to 10Hz
>>> uart.write(mtk.update_nmea_rate(10))
>>> 
# Check for Confirmation of Command
>>> result = None
>>> while not result:
...		while uart.any():
...			result = mtk_chk.update(chr(uart.readchar()))
...			if result:
...				if result[-4] == '3':
...					print('Command Succeded:', result)
...					break
>>> 
# Set Baudrate to 115200bps
>>> baud = 115200
>>> uart.write(mtk.update_baudrate(baud))
# No Confirmation is Given on Baud Rate Change
```

[Adafruit Ultimate GPS Breakout]:http://www.adafruit.com/products/746
[Digilent PmodGPS]:https://www.digilentinc.com/Products/Detail.cfm?NavPath=2,401,1038&Prod=PMOD-GPS
[Sparkfun GPS Receiver LS20031]:https://www.sparkfun.com/products/8975
[43oh MTK3339 GPS Launchpad Boosterpack]:http://store.43oh.com/index.php?route=product/product&product_id=81
[datasheet]:http://www.adafruit.com/datasheets/PMTK_A11.pdf
[Micropython]:http://micropython.org/
[micropyGPS]:https://github.com/inmcm/micropyGPS
[pyboard]:http://docs.micropython.org/en/latest/quickref.html
