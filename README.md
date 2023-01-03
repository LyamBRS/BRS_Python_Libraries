# BRS Python Libraries
## - Folders & their contents
If you want to learn more about the directory tree or what folders will contain what, you can refer yourself to this document (view through Diagram.net): https://drive.google.com/file/d/148wSuXA7z0FR9rAaGs48DwkEv2R8qK-p/view?usp=share_link.

Here is a short list of the directories and their descriptions:
- **Debug:** <span style="color: #696969;">Contains scripts used for various debugging such as prints and loggings</span>
- **GUI:** <span style="color: #696969;">Contains script for custom Widgets for BRS UI layouts</span>
- **Hardware:** <span style="color: #696969;">Folder containing all scripts and classes related to controlling hardware specific things</span>
- **Network:** <span style="color: #696969;">Contains script used to interface with various ethernet or Wifi aspects. Such as UDP TCP or APIs.</span>
- **PnP:** <span style="color: #696969;">Contains script used to interface with Plug n Play devices connected to the machine</span>
- **Utilities:** <span style="color: #696969;">Contains various script needed by most of the categorized libraries & scripts
(States etc)</span>

## - Classes and their structures
Classes and planned and referenced in the planning section of the available documentation. It is to note that I am no expert in neither planning nor object oriented programming. If you see things that could be made more efficient or faster, please let me know i'd be interested to know why. Note that although i've been programming for a while, Python is pretty new to me and I hate it from the bottom of my heart.

To see classes and their structures, please refer yourself to the planning section available on Google drive through this link: https://drive.google.com/drive/folders/1iPn1Ec0YsjzzDJay5vYSwzTZpcx0zcKS?usp=share_link

<br></br>
# Short Q&A
## - What is this for?
This Python library is what will be used to control and interface with **BRS_Kontrol**.

These are made to ease and simplify the many different existing python libraries that will be required to program **Kontrol**

## - What is BRS Kontrol & BrSpand?
BRS Kontrol is a multitask touchscreen remote which uses a Raspberry Pi as it's platform.

Kontrol's goal is to control a custom built ethernet accessed submarine. Kontrol needs to be  able to access the submarine either via direct Ethernet access, or via WiFi. The submarine will be sending video feed from an onboard camera through websockets and Kontrol needs to be able to show that camera feed as well as perform it's other tasks.

Kontrol must also be able to be customized and control hardware like accelerometers, RGB lights, onboard battery readings, BrSpand card detection and driving.

Kontrol also aims to be as modular as possible in order to allow multiple future projects to use the same platform as their controlling devices. This is done through BrSpand cards which will allow expansions to be plugged in Kontrol allowing more joysticks, antennas, sensors, debuggers, memory or anything you can think of as BrSpand cards will support I2C and SPI bus coming from Kontrol's hardware. Kontrol will be able to detect them and determine if you need to download drivers or update some in order to use the cards.

## - Which libraries are used in this repository?
- Kivy
- Pygame
- win32com

<br></br>
# Documentation
## - Where can I find documentation?
Documentation is available on Google Drive and the developement of Kontrol and it's libraries can be followed through our Discord server: https://discord.gg/HCYFEt2FUB

Documents are available there:
https://drive.google.com/drive/folders/10xdfNCYBKlcLZ3WLmZYxog1Ft2sFqgEQ?usp=sharing
