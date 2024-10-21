# ft991alincodxsr8
Some days ago, I wanted to participate in a ham radio contest. The best choice for logging contest data seems to be N1MM.
However, there is no support for the Alinco DX-SR8 that I own.

As the contest was already the other day, I needed a quick solution, and I had the idea to simulate a FT-991A which is supported by N1MM.

To this end, this script simply accepts the CAT commands issued by N1MM on a TCP/IP port and converts them to Alinco's CAT commands that are sent via serial interface.

## Prerequisites
* Python 3
* pySerial library (just run `pip install pyserial` after you have installed Python 3)
* N1MM

## Installation 
Simply copy the script to the directory of your convenience. Adapt the name of the serial port (e.g. `COM7`) at the end of the script. If your port 4711 is already used by another programm, you have
to change this as well.

Connect your Alinco to the serial port (or to USB via a USB/FT-232 adapter), turn your radio on.

Then, run the script from a command line via
```
python server.py
```

After that, run N1MM and select "Configure/Configure Ports, Winkey..." from the menu.
Select Port "TCP"", FT-991A as radio, and enter ``127.0.0.1:4711`` in the ``IP Addr:Port`` field. Leave everything else in the Hardware section unchanged. At your command line, some command should appear. When opening the bandmap, the frequency should correspond to your current frequency.

![Screenshot of the configuation settings of N1MM, as described above](https://github.com/gman1982/ft991alincodxsr8/blob/main/configureN1MM.png)

## Supported commands
For the sake of simplicity, only few commands where implemented yet:
* Frequency selection
* Modulation mode (LSB, USB, FM, CW-L, CW-U, AM)

## Trouble shooting
If you run the program, and it complains about problems with the serial port, first make sure that your serial port is set correctly (check via Window Device Manager), that your connection is good (check e.g. with HamRadioDeluxe or Alincos Channel editor), and that no other program block your serial port.

If the program crashes, in most cases, it was necessary to restart N1MM. To end the software, press ``CTRL+C`` in the command line window.

## Things missing
* Any modulation that is supported by FT-991A, but not by Alinco, is mapped to its nearest corresponsing mode, e.g. RTTY-LSB will just select LSB.
* Only frequency and mode selection is supported. Power, Gain etc. must be set manually.
* Any error thrown or any command not understood by N1MM or Alinco DX-SR8 is simply ignored.
* Please note, that there is no protection against malicious attackers. So it is strictly recommended to run this program only behind a firewall and under continuous supervision. In general, this program should only be started when you are participating in a contest and have full control over your computer and your radio.

## Most important
This a small script from a OM for other YLs and OMs to have fun with your radio and your contests! Feel free to fork, change, re-distribute this script as you want. To this, I published it under the GNU General License

73!
DK2GB
