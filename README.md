# UKBFG
# UnOfficial KiCAD BGA Footprint Generator (UKBFG)

This is a simple python based tool to generate Ball Grid Array (BGA) footprints for KiCAD EDA http://kicad-pcb.org/.

Dependencies:

Python 2.7, GTK+ 3.0, LibCairo

Installation (Tested on Ubuntu 16.04 LTS):

Note: Replace *apt* with *apt-get* for older versions of Ubuntu

1. Test for Python 2.7+ (usually installed) or install using *sudo apt install libpython2.7\**
2. Test for GTK-3.0+ or install the packages using *sudo apt install libgtk3\** 
3. Test for Cairo or install the packages using *sudo apt install libcairo\**

Usage:

1. Download *ukbfg.py* and cd to Download folder *chmod a+x ukbfg.py* and run *./ukbfg.py* and select the BGA parameters (one would need the mechanical dimensions page from the datasheet for a given component).

2. Select the Ball pitch (mm) of the IC.

3. Select the Ball diameter (mm) of the IC.

4. Select the Ball dimensions (mm) - Length/Width (both assumed to be same) of the IC. 

   Note: Since almost all ICs that I have encouuntered in BGA are assumed to be square, it is highly recommended to keep Length/Width to be the same. 
   
5. Select the Number of Pins of the IC.

6. One may populate or depopulate the pins on the BGA by simply using left click of the mouse, holding and dragging it while selecting the rectangular area (highlighed with a dark green border) and simply clicking *Populate Balls* or *Depopulate Balls* buttons depending on the situation.

7. Magnification between 0 - 100 is for visualization especially useful to compensate for changes in the other parameters during visualization.

8. One may save KiCAD BGA footprints to a drive. These may be later opened up in the KiCAD Footprint Editor Tool inside KiCAD EDA.


   
