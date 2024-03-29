# UKBFG
![alt text](https://github.com/enthusiasticgeek/UKBFG/blob/master/UKBFG.png "UKBFG")
# UnOfficial KiCAD BGA (PCB) Footprint Generator

This is a simple python based tool to generate Ball Grid Array (BGA) PCB footprints for KiCAD EDA http://kicad.org/.

#### A. Dependencies:

**Python 2.7, GTK+ 3.0, LibCairo**

#### B. Installation (Tested on Ubuntu 16.04 LTS):

**__Note:__** Replace **apt** with **apt-get** for older versions of Ubuntu in the following text.

1. Test for Python 2.7+ (usually installed) or install using **sudo apt install libpython2.7\***
2. Test for GTK-3.0+ or install the packages using **sudo apt install libgtk3\*** 
3. Test for Cairo or install the packages using **sudo apt install libcairo\***

#### C. Usage:

1. Download **ukbfg.py** and cd to Download folder **chmod a+x ukbfg.py** and run **./ukbfg.py** and select the BGA parameters (one would need the mechanical dimensions page from the datasheet for a given component IC).

2. Select the **Ball pitch (mm)** of the IC.

3. Select the **Ball diameter (mm)** of the IC.

4. Select the **Ball dimensions (mm)** - Length and Width (both may be different e.g. WBGA-84 package) of the IC. 
   
5. Select the Number of **Pins** of the IC.

6. One may populate or depopulate the pins on the BGA by simply using left click of the mouse, holding and dragging it while selecting the rectangular area (highlighed with a dark green border) and simply clicking **Populate Balls** or **Depopulate Balls** buttons depending on the situation.

7. Magnification between _0 - 100_ is for visualization especially useful to compensate for changes in the other parameters during visualization.

8. One may **save** KiCAD BGA footprints to a drive. These may be later opened up in the KiCAD Footprint Editor Tool inside KiCAD EDA.

**Note: Currently W x L design upto 22 x 22 ball pins BGA is supported using this tool.**

![alt text](https://github.com/enthusiasticgeek/UKBFG/blob/master/ukbfg_screenshot0.png "UKBFG")
   
