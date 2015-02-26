# MTK GPS Command Sentence Generator for Python

# Copyright (c) 2015 Calvin McCoy (calvin.mccoy@gmail.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


__valid_baudrates = [4800, 9600, 14400, 19200, 38400, 57600, 115200]


# ##### Fixed Command Strings ########

# Set Sentence Output to default sentences and frequencies
default_sentences = '$PMTK314,-1*04\r\n'

# Restart Receiver using all available data
hot_start = '$PMTK101*32\r\n'

# Restart Receiver without Ephemeris data
warm_start = '$PMTK102*31\r\n'

# Restart Receiver with no initial data
cold_start = '$PMTK103*30\r\n'

# Restart Receiver with no initial data and reset receiver to factory defaults
full_cold_start = '$PMTK104*37\r\n'

# Set Receiver into Standby Mode
standby = '$PMTK161,0*28\r\n'


def crc_calc(input_string):
    """
    Calculates cumulative XOR CRC of inputted string
    :param input_string: Str to CRC
    :return: 2 char CRC str
    """
    crc = 0

    for next_char in input_string:
        ascii_val = ord(next_char)
        crc ^= ascii_val

    hex_crc = hex(crc)

    if crc <= 0xF:
        crc_byte = '0' + hex_crc[2]
    else:
        crc_byte = hex_crc[2:4]

    return crc_byte


def update_nmea_rate(nmearate):
    """
    Returns a valid MTK command sentence that sets the update interval of the reciever
    :param nmearate: float value of update rate in Hertz; must be between 1 and 10
    :return: MTK command str
    """
    if 1 > nmearate > 10:
        return None

    milli_value = int(1000 / nmearate)

    cmd_body = 'PMTK220,' + str(milli_value)

    crc = crc_calc(cmd_body)

    full_string = '$' + cmd_body + '*' + crc + '\r\n'

    return full_string


def update_baudrate(baudrate):
    """
    Returns a valid MTK command sentence that sets the baud rate of serial output of the receiver
    :param baudrate: Int corresponding to valid baud rate
    :return: MTK command string
    """
    if baudrate not in __valid_baudrates:
        return None

    cmd_body = 'PMTK251,' + str(baudrate)

    crc = crc_calc(cmd_body)

    full_string = '$' + cmd_body + '*' + crc + '\r\n'

    return full_string


def update_sentences(en_gll=True, en_rmc=True, en_vtg=True, en_gga=True, en_gsa=True, en_gsv=True, en_mchn=False,
                     gll_int=1, rmc_int=1, vtg_int=1, gga_int=1, gsa_int=1, gsv_int=3, mchn_int=0):
    """
    Returns a valid MTK command sentence that can set the update rate for each of the available NMEA sentence types.
    :param en_gll: Boolean to enable GLL sentences
    :param en_rmc: Boolean to enable RMC sentences
    :param en_vtg: Boolean to enable VTG sentences
    :param en_gga: Boolean to enable GGA sentences
    :param en_gsa: Boolean to enable GSA sentences
    :param en_gsv: Boolean to enable GSV sentences
    :param en_mchn: Boolean to enable MCHN sentences
    :param gll_int: Int for number of update intervals between updates for GLL
    :param rmc_int: Int for number of update intervals between updates for RMC
    :param vtg_int: Int for number of update intervals between updates for VTG
    :param gga_int: Int for number of update intervals between updates for GGA
    :param gsa_int: Int for number of update intervals between updates for GSA
    :param gsv_int: Int for number of update intervals between updates for GSV
    :param mchn_int: Int for number of update intervals between updates for MCHN
    :return: MTK command str
    """
    if en_gll:
        gll_str = str(gll_int)
    else:
        gll_str = '0'

    if en_rmc:
        rmc_str = str(rmc_int)
    else:
        rmc_str = '0'

    if en_vtg:
        vtg_str = str(vtg_int)
    else:
        vtg_str = '0'

    if en_gga:
        gga_str = str(gga_int)
    else:
        gga_str = '0'

    if en_gsa:
        gsa_str = str(gsa_int)
    else:
        gsa_str = '0'

    if en_gsv:
        gsv_str = str(gsv_int)
    else:
        gsv_str = '0'

    if en_mchn:
        mchn_str = str(mchn_int)
    else:
        mchn_str = '0'

    cmd_body = 'PMTK314,' + gll_str + ',' + rmc_str + ',' + vtg_str + ',' + gga_str + ',' + gsa_str + ',' + \
               gsv_str + ',0,0,0,0,0,0,0,0,0,0,0,0,' + mchn_str

    crc = crc_calc(cmd_body)

    full_string = '$' + cmd_body + '*' + crc + '\r\n'

    return full_string
