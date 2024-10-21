 # 
 # This file is part of the FT-991A <-> Alinco Adapter (https://github.com/gman1982/ft991alincodxsr8).
 # Copyright (c) 2024 Gereon Schueller, DK2GB.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

import socket
import time
import serial
import sys

freq='001421200'

def handleCmd(cmd):
    global freq
    global mode
        
    try:
        if cmd.startswith(b'IF'):
            if (len(cmd) == 28):
                return cmd
            else:
            
                f = getFreq()
                print(f)
                freq = convFreqAlincoYaesu(f)
                
                m = getMode()
                print(m)
                mode = convModeAlincoYaesu(m)
        
                memory='000'
                clar='+0000'
                clarRX='0'
                clarTX='0'
                #mode='2'
                vfo='0'
                ctss='0'
                p9='00'
                simplex='0'
                return 'IF' + memory + freq + clar + clarRX +clarTX+mode+vfo+ctss+p9+simplex+';'
        if cmd.startswith(b'OI'):
            print("OI")
            
            f = getFreq()
            print(f)
            freq = convFreqAlincoYaesu(f)
            
            m = getMode()
            print(m)
            mode = convModeAlincoYaesu(m)
            
            memory='000'
            clar='+0000'
            clarRX='0'
            clarTX='0'
            vfo='0'
            ctss='0'
            p9='00'
            simplex='0'
            return 'OI' + memory + freq + clar + clarRX +clarTX+mode+vfo+ctss+p9+simplex+';'
        if cmd.startswith(b'FT'):
            return "FT0;"
        if cmd.startswith(b'AG0'):
            return "AG0000;"
        if cmd.startswith(b'AI0'):
            return "AI0;"
        if cmd.startswith(b'MD0'):
            y = cmd[-1:]
            mode = convModeYaesuAlinco(y)
            setMode(mode)
            return cmd.decode("ASCII") + ";"
        if cmd.startswith(b'FR0'):
            return "FR0;"
        if cmd.startswith(b'FA'):
            freq = cmd[2:11].decode("ASCII")
            alinco = convFreqYaesuAlinco(freq)
            setFreq(alinco)
            
            return cmd.decode("ASCII") + ";" #FA014200000
        print(f"Unknown: {cmd}")
    except:
        print("Error in command handling:", sys.exc_info())
    return ""
    
def sendCmd(inp):
    print(inp)
    inp = inp.encode("ascii","ignore")
    ser.write(inp + b'\r\n')


def setFreq(freq):
    sendCmd(f"AL~RW_RXF{freq}")
    
def getFreq():
        ser.write(b'AL~RR_RXF\r\n')
        out = b''
        # let's wait 50 milli-seconds before reading output (let's give device time to answer)
        time.sleep(0.05)
        while ser.inWaiting() > 0:
            out += ser.read(1)
            
        if out != '':
            print(f"Freq response {out}") 
            response = out.decode("ASCII")
            return response.splitlines()[1]
            
def convFreqAlincoYaesu(freq):
    return freq.zfill(9)
    
def convFreqYaesuAlinco(freq):
    return freq[1:] + '0'
    
    
def setMode(mode):
    sendCmd(f"AL~RW_RFM{mode}")
    
def getMode():
        ser.write(b'AL~RR_RFM\r\n')
        out = b''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(0.05)
        while ser.inWaiting() > 0:
            out += ser.read(1)
            
        if out != '':
            print(f"Freq response {out}") 
            response = out.decode("ASCII")
            return response.splitlines()[1]
    
def convModeAlincoYaesu(code):
    print(f"Converting Alinco code /{code}/")
    match code:
        case '00':
            return '2'
        case '01':
            return '1'
        case '02':
            return '3'
        case '03':
            return '7'
        case '04':
            return '5'
        case '05':
            return '4'
    return '2'
    
def convModeYaesuAlinco(code):
    print(f"Converting Yaesu code /{code}/")
    
    match code:
        case b'2' | b'9' | b'C':
            return '00'
        case b'1' | b'6' | b'8':
            return '01'
        case b'3':
            return '02'
        case b'7':
            return '03'
        case b'5' | b'D':
            return '04'
        case b'4' | b'A' | b'B' | b'E':
            return '05'
    return '05'
        

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 4711  # Port to listen on (non-privileged ports are > 1023)

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM7',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                 data = conn.recv(1024)
            except(socket.error, e):
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    print('No data available')
                    continue
                else:
                    # a "real" error occurred
                    print(e)
                    sys.exit(1)
            else:
                if (len(data) > 0):
                    # got a message
                    print(f"Received {data}")
                    cmds = data.split(b';')
                    for cmd in cmds:
                        if len(cmd) > 0:
                            print(f"Got command {cmd}")
                            ans = handleCmd(cmd)
                            print(f"Answer {ans}")
                            conn.sendall(ans.encode("ASCII"))
                  