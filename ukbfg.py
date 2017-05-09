#!/usr/bin/env python
# May 1, 2017
# License: MIT License
#####################################################################################################################################################
#Copyright (c) 2017 Pratik M Tambe (enthusiasticgeek)  <enthusiasticgeek@gmail.com> 
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#######################################################################################################################################################
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import math
import cairo
import time
import datetime

class MouseButtons:

    LEFT_BUTTON = 1
    CENTER_BUTTON = 2
    RIGHT_BUTTON = 3


class PyApp(Gtk.Window):

    def __init__(self):
        super(PyApp, self).__init__()

        self.BEGIN_MOUSE_X = 0
        self.BEGIN_MOUSE_Y = 0
        self.END_MOUSE_X = 0
        self.END_MOUSE_Y = 0
       
        # Initialize with some reasonable parameters
        self.SCALING = 50
        self.PACKAGE = 'BGA_PKG'
        self.NUM_PINS_LENGTH = 10    
        self.NUM_PINS_WIDTH = 10    
        self.LENGTH = 9.0 # BGA length 9 mm   # Vertical     
        self.WIDTH = 9.0  # BGA width 9 mm    # Horizontal   
        self.OFFSET_X = 100
        self.OFFSET_Y = 100
        self.BALL_PITCH = 0.8 # ball pitch is 0.08 mm
        self.BALL_DIAMETER = 0.45 # ball diameter is 0.04 mm
        self.set_title("UNOFFICIAL KiCAD BGA FOOTPRINT GENERATOR [UKBFG]")
        #self.set_size_request(int(self.BALL_PITCH*self.SCALING*self.NUM_PINS_WIDTH)+self.OFFSET_X+200, int(self.BALL_PITCH*self.SCALING*self.NUM_PINS_LENGTH)+self.OFFSET_Y+200)
        self.set_position(Gtk.WindowPosition.CENTER)
        # DEC alphabet nomenclature implemented to avoid I (1), O (0) and S (5) - Letters that confuse with numbers.
        self.COL = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','T','U','V','W','X','Y','Z']
        self.ROW = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        self.RESULT = ''

        # Parameters for the math calculation
        self.CALC_LENGTH = (self.NUM_PINS_LENGTH-1)*self.BALL_PITCH
        self.CALC_WIDTH = (self.NUM_PINS_WIDTH-1)*self.BALL_PITCH
        self.CALC_BALL_DIAMETER = self.BALL_DIAMETER

        self.connect("destroy", Gtk.main_quit)

        self.darea = Gtk.DrawingArea()
        self.darea.set_size_request(int(self.BALL_PITCH*self.SCALING*self.NUM_PINS_WIDTH)+self.OFFSET_X+50, int(self.BALL_PITCH*self.SCALING*self.NUM_PINS_LENGTH)+self.OFFSET_Y+50)
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK | Gdk.EventMask.BUTTON1_MOTION_MASK)  
 
        self.populate = []
        self.darea.connect("button-press-event", self.on_button_press)
        self.darea.connect("button-release-event", self.on_button_release)
        self.darea.connect("motion_notify_event", self.on_motion_notify_event)

        self.vbox = Gtk.VBox(False,2)
        self.vbox.pack_start(self.darea, False, False, 0)

        self.hbox = Gtk.HBox(False,2)
        self.vbox1 = Gtk.VBox(False,2)
        self.vbox2 = Gtk.VBox(False,2)
        self.vbox3 = Gtk.VBox(False,2)
        self.vbox4 = Gtk.VBox(False,2)
        self.vbox5 = Gtk.VBox(False,2)
        self.vbox6 = Gtk.VBox(False,2)
        self.vbox7 = Gtk.VBox(False,2)
        self.hbox.pack_start(self.vbox1, False, False, 0)
        self.hbox.pack_start(self.vbox2, False, False, 0)
        self.hbox.pack_start(self.vbox3, False, False, 0)
        self.hbox.pack_start(self.vbox4, False, False, 0)
        self.hbox.pack_start(self.vbox5, False, False, 0)
        self.hbox.pack_start(self.vbox6, False, False, 0)
        self.hbox.pack_start(self.vbox7, False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
       
        hseparator = Gtk.HSeparator()
        self.ball_pitch_label = Gtk.Label("")
        self.ball_pitch_label.set_label("<b>Ball Pitch (mm)</b>")
        self.ball_pitch_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkgreen")[1])
        self.ball_pitch_label.set_use_markup(True)
        self.ball_pitch_entry = Gtk.Entry()
        self.ball_pitch_entry.set_visibility(True)
        self.ball_pitch_entry.set_max_length(5)
        self.ball_pitch_entry.set_text(str(self.BALL_PITCH))
        self.ball_pitch_button = Gtk.Button("")
        for child in self.ball_pitch_button : 
            child.set_label("<b>Update Ball Pitch</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])
        ball_pitch_mils = self.BALL_PITCH/0.0254
        self.ball_pitch_mils_label = Gtk.Label(str(ball_pitch_mils) + " mil")
        self.ball_pitch_mils_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("purple")[1])


        self.vbox1.pack_start(hseparator, False, False, 0)
        self.vbox1.pack_start(self.ball_pitch_label, False, False, 0)
        self.vbox1.pack_start(self.ball_pitch_entry, False, False, 0)
        self.vbox1.pack_start(self.ball_pitch_button, False, False, 0)
        self.vbox1.pack_start(self.ball_pitch_mils_label, False, False, 0)
        
        self.ball_pitch_button.connect("clicked", self.on_ball_pitch_button)
       
        hseparator = Gtk.HSeparator()
        self.ball_diameter_label = Gtk.Label("")
        self.ball_diameter_label.set_label("<b>Ball Diameter (mm) </b>")
        self.ball_diameter_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkgreen")[1])
        self.ball_diameter_label.set_use_markup(True)
        self.ball_diameter_entry = Gtk.Entry()
        self.ball_diameter_entry.set_visibility(True)
        self.ball_diameter_entry.set_max_length(5)
        self.ball_diameter_entry.set_text(str(self.BALL_DIAMETER))
        self.ball_diameter_button = Gtk.Button("")
        for child in self.ball_diameter_button : 
            child.set_label("<b>Update Ball Diameter</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])
        ball_diameter_mils = self.BALL_DIAMETER/0.0254
        self.ball_diameter_mils_label = Gtk.Label(str(ball_diameter_mils) + " mil")
        self.ball_diameter_mils_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("purple")[1])

        self.vbox2.pack_start(hseparator, False, False, 0)
        self.vbox2.pack_start(self.ball_diameter_label, False, False, 0)
        self.vbox2.pack_start(self.ball_diameter_entry, False, False, 0)
        self.vbox2.pack_start(self.ball_diameter_button, False, False, 0)
        self.vbox2.pack_start(self.ball_diameter_mils_label, False, False, 0)
        
        self.ball_diameter_button.connect("clicked", self.on_ball_diameter_button)

        hseparator = Gtk.HSeparator()
        self.ball_dimensions_label = Gtk.Label("")
        self.ball_dimensions_label.set_label("<b>IC Dimensions (mm) [LxW] </b>")
        self.ball_dimensions_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkgreen")[1])
        self.ball_dimensions_label.set_use_markup(True)
        self.ball_dimensions_entry_length = Gtk.Entry()
        self.ball_dimensions_entry_length.set_visibility(True)
        self.ball_dimensions_entry_length.set_max_length(5)
        self.ball_dimensions_entry_length.set_text(str(self.LENGTH))
        self.ball_dimensions_entry_width = Gtk.Entry()
        self.ball_dimensions_entry_width.set_visibility(True)
        self.ball_dimensions_entry_width.set_max_length(5)
        self.ball_dimensions_entry_width.set_text(str(self.WIDTH))
        self.ball_dimensions_button = Gtk.Button("")
        for child in self.ball_dimensions_button : 
            child.set_label("<b>Update Ball dimensions</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])


        self.vbox3.pack_start(hseparator, False, False, 0)
        self.vbox3.pack_start(self.ball_dimensions_label, False, False, 0)
        self.vbox3.pack_start(self.ball_dimensions_entry_length, False, False, 0)
        self.vbox3.pack_start(self.ball_dimensions_entry_width, False, False, 0)
        self.vbox3.pack_start(self.ball_dimensions_button, False, False, 0)

        self.ball_dimensions_button.connect("clicked", self.on_ball_dimensions_button)
 
        hseparator = Gtk.HSeparator()
        self.pins_label = Gtk.Label("")
        self.pins_label.set_label("<b>Pins</b>")
        self.pins_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkgreen")[1])
        self.pins_label.set_use_markup(True)
        self.pins_entry_length = Gtk.Entry()
        self.pins_entry_length.set_visibility(True)
        self.pins_entry_length.set_max_length(5)
        self.pins_entry_length.set_text(str(self.NUM_PINS_LENGTH))
        self.pins_entry_width = Gtk.Entry()
        self.pins_entry_width.set_visibility(True)
        self.pins_entry_width.set_max_length(5)
        self.pins_entry_width.set_text(str(self.NUM_PINS_WIDTH))
        self.pins_button = Gtk.Button("")
        for child in self.pins_button : 
            child.set_label("<b>Update pins</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])


        self.vbox4.pack_start(hseparator, False, False, 0)
        self.vbox4.pack_start(self.pins_label, False, False, 0)
        self.vbox4.pack_start(self.pins_entry_length, False, False, 0)
        self.vbox4.pack_start(self.pins_entry_width, False, False, 0)
        self.vbox4.pack_start(self.pins_button, False, False, 0)
        
        self.pins_button.connect("clicked", self.on_pins_button)

        hseparator = Gtk.HSeparator()
        self.populate_depopulate_balls_label = Gtk.Label("")
        self.populate_depopulate_balls_label.set_label("<b>Select the area to populate or depopulate\nBGA balls by holding left mouse button\nand dragging</b>")
        self.populate_depopulate_balls_label.set_use_markup(True)
        self.populate_depopulate_balls_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("blue")[1])
        self.populate_balls_button = Gtk.Button("")
        for child in self.populate_balls_button : 
            child.set_label("<b>Populate Balls</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])

        self.depopulate_balls_button = Gtk.Button("")
        for child in self.depopulate_balls_button : 
            child.set_label("<b>Depopulate Balls</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])

        self.vbox5.pack_start(hseparator, False, False, 0)
        self.vbox5.pack_start(self.populate_depopulate_balls_label, False, False, 0)
        self.vbox5.pack_start(self.populate_balls_button, False, False, 0)
        self.vbox5.pack_start(self.depopulate_balls_button, False, False, 0)
 
        self.populate_balls_button.connect("clicked", self.on_populate_balls_button)
        self.depopulate_balls_button.connect("clicked", self.on_depopulate_balls_button)
 
        hseparator = Gtk.HSeparator()
        self.magnification_label = Gtk.Label("")
        self.magnification_label.set_label("<b>Magnification\n(Visualization Only)</b>")
        self.magnification_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkgreen")[1])
        self.magnification_label.set_use_markup(True)
        self.magnification_entry = Gtk.Entry()
        self.magnification_entry.set_visibility(True)
        self.magnification_entry.set_max_length(5)
        self.magnification_entry.set_text(str(self.SCALING))
        self.magnification_button = Gtk.Button("")
        for child in self.magnification_button : 
            child.set_label("<b>Magnification [0,100]</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])

        self.vbox6.pack_start(hseparator, False, False, 0)
        self.vbox6.pack_start(self.magnification_label, False, False, 0)
        self.vbox6.pack_start(self.magnification_entry, False, False, 0)
        self.vbox6.pack_start(self.magnification_button, False, False, 0)
        
        self.magnification_button.connect("clicked", self.on_magnification_button)
 
        hseparator = Gtk.HSeparator()
        self.save_label = Gtk.Label("")
        self.save_label.set_label("<b>Footprint Output</b>")
        self.save_label.set_use_markup(True)
        self.save_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkgreen")[1])
        self.package_entry = Gtk.Entry()
        self.package_entry.set_visibility(True)
        self.package_entry.set_max_length(10)
        self.package_entry.set_text(str(self.PACKAGE))
        self.save_button = Gtk.Button("")
        for child in self.save_button : 
            child.set_label("<b>Save KiCAD Footprint</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])
        self.about_button = Gtk.Button("")
        for child in self.about_button : 
            child.set_label("<b>About UKBFG</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])
        self.exit_button = Gtk.Button("")
        for child in self.exit_button : 
            child.set_label("<b>Exit UKBFG</b>")
            child.set_use_markup(True)
            child.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.parse("darkred")[1])

        self.vbox7.pack_start(hseparator, False, False, 0)
        self.vbox7.pack_start(self.save_label, False, False, 0)
        self.vbox7.pack_start(self.package_entry, False, False, 0)
        self.vbox7.pack_start(self.save_button, False, False, 0)
        self.vbox7.pack_start(self.about_button, False, False, 0)
        self.vbox7.pack_start(self.exit_button, False, False, 0)
        
        self.save_button.connect("clicked", self.on_save_button)
        self.about_button.connect("clicked", self.on_about_button)
        self.exit_button.connect("clicked", self.on_exit_button)


        self.add(self.vbox)
        self.show_all()

        #initialize
        for x in range(0, self.NUM_PINS_WIDTH):
          for y in range(0, self.NUM_PINS_LENGTH):
            self.populate.append([x,y])

    def on_save_button(self, widget):
        if self.LENGTH <= self.CALC_LENGTH or self.WIDTH <= self.CALC_WIDTH:
           dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
               Gtk.ButtonsType.CANCEL, "Error: Length/width <= (#balls-1)*pitch")
           dialog.format_secondary_text(
               "Incorrect calculation. Please update one or more parameters: length, width, ball pitch, pins.")
           dialog.run()
           dialog.destroy()
           return False

        self.PACKAGE = str(self.package_entry.get_text())
        dialog = Gtk.FileChooserDialog("Please choose a kicad file", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        filter_kicad = Gtk.FileFilter()
        filter_kicad.set_name("KiCAD footprint")
        filter_kicad.add_pattern("*.kicad_mod")
        dialog.add_filter(filter_kicad)
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
           #print("File selected: " + dialog.get_filename())
           #buf = self.view.get_buffer()
           #self.RESULT = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
           kicad_filename = dialog.get_filename()
           # check file extension. If no file extension add it
           if ".kicad_mod" not in kicad_filename:
              kicad_filename += ".kicad_mod"
           try:
                open(kicad_filename, 'w').write(self.RESULT)
           except SomeError as err:
                print('Could not save %s: %s' % (kicad_filename, err))
        elif response == Gtk.ResponseType.CANCEL:
                print("Cancel clicked")
        dialog.destroy()


    def on_exit_button(self, widget):
        Gtk.main_quit()
        

    def on_about_button(self, widget):
        about = Gtk.AboutDialog(PyApp,self)
        about.set_program_name("Unofficial KiCAD BGA Footprint Generator (UKBFG)")
        about.set_version("Version: 0.1")
        about.set_copyright("Copyright (c) 2017 Pratik M Tambe <enthusiasticgeek@gmail.com>")
        about.set_comments("A simple tool for generating KiCAD BGA footprint")
        about.set_website("https://github.com/enthusiasticgeek")
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size("UKBFG.png", 300, 185))
        about.run()
        about.destroy()

    def on_populate_balls_button(self, widget):
        if self.BEGIN_MOUSE_X < self.END_MOUSE_X and self.BEGIN_MOUSE_Y < self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be populated")                     
                         if [x,y] not in self.populate:
                            self.populate.append([x,y])
  
        elif self.BEGIN_MOUSE_X < self.END_MOUSE_X and self.BEGIN_MOUSE_Y > self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be populated")                     
                         if [x,y] not in self.populate:
                            self.populate.append([x,y])
  
        elif self.BEGIN_MOUSE_X > self.END_MOUSE_X and self.BEGIN_MOUSE_Y < self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be populated")                     
                         if [x,y] not in self.populate:
                            self.populate.append([x,y])
 
        elif self.BEGIN_MOUSE_X > self.END_MOUSE_X and self.BEGIN_MOUSE_Y > self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be populated")                     
                         if [x,y] not in self.populate:
                            self.populate.append([x,y])
  
        else:
            print "Not a rectangle! Please select a rectangle"
        self.darea.queue_draw()

    def on_depopulate_balls_button(self, widget):
        if self.BEGIN_MOUSE_X < self.END_MOUSE_X and self.BEGIN_MOUSE_Y < self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be depopulated")                     
                         while [x,y] in self.populate: self.populate.remove([x,y])

  
        elif self.BEGIN_MOUSE_X < self.END_MOUSE_X and self.BEGIN_MOUSE_Y > self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be depopulated")                     
                         while [x,y] in self.populate: self.populate.remove([x,y])
  
        elif self.BEGIN_MOUSE_X > self.END_MOUSE_X and self.BEGIN_MOUSE_Y < self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be depopulated")                     
                         while [x,y] in self.populate: self.populate.remove([x,y])
 
        elif self.BEGIN_MOUSE_X > self.END_MOUSE_X and self.BEGIN_MOUSE_Y > self.END_MOUSE_Y:
           for x in range(0, self.NUM_PINS_WIDTH):
               for y in range(0, self.NUM_PINS_LENGTH):
                   if x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X < self.BEGIN_MOUSE_X and \
                      x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X > self.END_MOUSE_X and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y < self.BEGIN_MOUSE_Y and \
                      y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y > self.END_MOUSE_Y :
                         #print(str(self.COL[y]+str(self.ROW[x]))+ " is to be depopulated")                     
                         while [x,y] in self.populate: self.populate.remove([x,y])
 
        else:
            print "Not a rectangle! Please select a rectangle"
        self.darea.queue_draw()

    def erase_ball(cr,x,y):
        # Draw the Ball Grid Array Balls
        cr.set_source_rgb(0.8, 0.8, 0.8)
        cr.arc(x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X, y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y, self.BALL_DIAMETER/2*self.SCALING, 0, 2*math.pi)
        cr.fill()
        self.darea.queue_draw()

    def draw_ball(cr,x,y):
        # Draw the Ball Grid Array Balls
        cr.set_source_rgb(0.6, 0.6, 0.6)
        cr.arc(x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X, y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y, self.BALL_DIAMETER/2*self.SCALING, 0, 2*math.pi)
        cr.fill()
        self.darea.queue_draw()

    def erase_ball_text(cr,x,y):
        # Draw the Ball Grid Array Balls Text 
        cr.set_source_rgb(0.8, 0.8, 0.8)
        cr.move_to(x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X, y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y)
        cr.show_text(str(self.COL[y]+str(self.ROW[x])))
        self.darea.queue_draw()

    def draw_ball_text(cr,x,y):
        # Draw the Ball Grid Array Balls Text 
        cr.set_source_rgb(0.0, 0.0, 1.0)
        cr.move_to(x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X, y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y)
        cr.show_text(str(self.COL[y]+str(self.ROW[x])))
        self.darea.queue_draw()

    def update_area(self):
        self.darea.set_size_request(int(self.BALL_PITCH*self.SCALING*self.NUM_PINS_WIDTH)+self.OFFSET_X+50, int(self.BALL_PITCH*self.SCALING*self.NUM_PINS_LENGTH)+self.OFFSET_Y+50)

    def on_ball_pitch_button(self, widget):
        #TODO Other sanity checks -> try except block
        ball_pitch = float(self.ball_pitch_entry.get_text())
        if isinstance(ball_pitch, (int, float)) == True:
           self.BALL_PITCH = ball_pitch
           ball_pitch_mils = self.BALL_PITCH/0.0254
           self.ball_pitch_mils_label.set_text(str(ball_pitch_mils) + " mil")
           self.update_area()
           self.darea.queue_draw()
        else:
           print ("Invalid pitch " + str(ball_pitch)) 

    def on_ball_diameter_button(self, widget):
        #TODO Other sanity checks -> try except block
        ball_diameter = float(self.ball_diameter_entry.get_text())
        if isinstance(ball_diameter, (int, float)) == True:
           self.BALL_DIAMETER = ball_diameter
           ball_diameter_mils = self.BALL_DIAMETER/0.0254
           self.ball_diameter_mils_label.set_text(str(ball_diameter_mils) + " mil")
           self.update_area()
           self.darea.queue_draw()
        else:
           print ("Invalid diameter " + str(ball_diameter)) 

    def on_ball_dimensions_button(self, widget):
        #TODO Other sanity checks -> try except block
        length = float(self.ball_dimensions_entry_length.get_text())
        width = float(self.ball_dimensions_entry_width.get_text())
        if isinstance(length, (int, float)) == True and isinstance(width, (int, float)) == True:
           self.LENGTH = length
           self.WIDTH = width
           self.update_area()
           self.darea.queue_draw()
        else:
           print ("Invalid dimensions " + str(length) + " " + str(width))

    def on_pins_button(self, widget):
        #TODO Other sanity checks -> try except block
        pins_length = int(self.pins_entry_length.get_text())
        pins_width = int(self.pins_entry_width.get_text())
        if isinstance(pins_length, (int)) == True and isinstance(pins_width, (int)) == True:
           self.NUM_PINS_LENGTH = pins_length
           self.NUM_PINS_WIDTH = pins_width
           #if self.NUM_PINS_WIDTH < max(self.populate,key=lambda item:item[0])[0]:
           #for i in range(len(self.populate)):
           #    if self.populate[i][0] > self.NUM_PINS_WIDTH:
           #       print self.populate[i] 
           #        while [self.populate[i][0],self.populate[i][1]] in self.populate: self.populate.remove([self.populate[i][0],self.populate[i][1]])
           
           #if self.NUM_PINS_LENGTH < max(self.populate,key=lambda item:item[1])[1]:
           #for i in range(len(self.populate)):
           #    if self.populate[i][1] > self.NUM_PINS_LENGTH:
           #       print self.populate[i] 
           #        while [self.populate[i][0],self.populate[i][1]] in self.populate: self.populate.remove([self.populate[i][0],self.populate[i][1]])
 
           self.update_area()
           self.darea.queue_draw()
        else:
           print ("Invalid pins " + str(pins)) 

    def on_magnification_button(self, widget):
        #TODO Other sanity checks -> try except block
        magnification = int(self.magnification_entry.get_text())
        if isinstance(magnification, (int)) == True:
           self.SCALING = magnification
           self.update_area()
           self.darea.queue_draw()
        else:
           print ("Invalid magnification " + str(magnification)) 

    def on_button_press(self, w, e):
        #print 'PRESS: ', e.x, ' ', e.y
        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.LEFT_BUTTON:
            self.BEGIN_MOUSE_X = e.x
            self.BEGIN_MOUSE_Y = e.y
        self.darea.queue_draw()

    def on_button_release(self, w, e):
        #print 'RELEASE: ',e.x, ' ', e.y
        if e.type == Gdk.EventType.BUTTON_RELEASE \
            and e.button == MouseButtons.LEFT_BUTTON:
            self.END_MOUSE_X = e.x
            self.END_MOUSE_Y = e.y
        self.darea.queue_draw()

    def on_motion_notify_event(self, w, e):
        #print 'MOVING: ',e.x, ' ', e.y
        if e.type == Gdk.EventType.MOTION_NOTIFY: 
            self.END_MOUSE_X = e.x
            self.END_MOUSE_Y = e.y
        self.darea.queue_draw()
  
    def on_draw(self, widget, cr):

        # Update parameters for the math calculation
        self.CALC_LENGTH = (self.NUM_PINS_LENGTH-1)*self.BALL_PITCH
        self.CALC_WIDTH = (self.NUM_PINS_WIDTH-1)*self.BALL_PITCH
        self.CALC_BALL_DIAMETER = self.BALL_DIAMETER

        #Initialize
        self.RESULT=''
        cr.set_source_rgb(0.8, 0.8, 0.8)
        cr.select_font_face("Times New Roman", cairo.FONT_SLANT_NORMAL, 
            cairo.FONT_WEIGHT_NORMAL)

        # If BGA count exceeds 23*23 pins
        cr.set_source_rgb(0.0, 0.0, 0.0)
        if(( self.NUM_PINS_LENGTH < 2 or self.NUM_PINS_LENGTH > 23) or ( self.NUM_PINS_WIDTH < 2 or self.NUM_PINS_WIDTH > 23 )):
            cr.move_to(self.OFFSET_X-99, self.OFFSET_Y-40)
            cr.show_text("BGA PIN [Width or Length] COUNT outside [2,23]")
            return False

        # Set Axis names

        # COL - Y - AXIS
        cr.set_source_rgb(0.0, 0.0, 1.0)
        for y in range(0, self.NUM_PINS_LENGTH):
            cr.move_to(self.OFFSET_X-20, self.OFFSET_X+self.BALL_PITCH*self.SCALING*y)
            cr.show_text(str(self.COL[y]))
 
        # ROW - X - AXIS
        cr.set_source_rgb(0.0, 0.0, 1.0)
        for x in range(0, self.NUM_PINS_WIDTH):
            cr.move_to(self.OFFSET_Y+self.BALL_PITCH*self.SCALING*x, self.OFFSET_Y-20)
            cr.show_text(str(self.ROW[x]))
        
        # Draw the Ball Grid Array BGA rectangular plan that connect first BGA ball to the last BGA ball 
        cr.set_source_rgb(0.8, 0.8, 0.8)
        cr.rectangle(self.OFFSET_X,self.OFFSET_Y,(self.NUM_PINS_WIDTH-1)*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH, (self.NUM_PINS_LENGTH-1)*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH)
        cr.fill()

        #outer rectangle that defines BGA
        cr.set_source_rgb(0.8, 0.4, 0.4)
        cr.rectangle(self.OFFSET_X - (self.WIDTH-self.BALL_PITCH*self.NUM_PINS_WIDTH)/2, self.OFFSET_Y - (self.LENGTH-self.BALL_PITCH*self.NUM_PINS_LENGTH)/2,(self.NUM_PINS_WIDTH-1)*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+(self.WIDTH-self.BALL_PITCH*self.NUM_PINS_WIDTH),(self.NUM_PINS_LENGTH-1)*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+(self.LENGTH-self.BALL_PITCH*self.NUM_PINS_LENGTH))
        cr.stroke()

        # Draw the Ball Grid Array Balls
        for x in range(0, self.NUM_PINS_WIDTH):
          for y in range(0, self.NUM_PINS_LENGTH):
            if [x,y] in self.populate:
              cr.set_source_rgb(0.6, 0.6, 0.6)
            else:
              cr.set_source_rgb(0.8, 0.8, 0.8)
            cr.arc(x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X, y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y, self.BALL_DIAMETER/2*self.SCALING, 0, 2*math.pi)
            cr.fill()
 
        # Draw the Ball Grid Array Balls Text 
        for x in range(0, self.NUM_PINS_WIDTH):
          for y in range(0, self.NUM_PINS_LENGTH):
            if [x,y] in self.populate:
              cr.set_source_rgb(0.0, 0.0, 1.0)
            else:
              cr.set_source_rgb(0.8, 0.8, 0.8)
            cr.move_to(x*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X, y*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y)
            cr.show_text(str(self.COL[y]+str(self.ROW[x])))

        # Draw the text indicating BGA pitch
        cr.move_to(self.OFFSET_X,(self.OFFSET_Y+(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y)/2)
        cr.set_source_rgb(1.0, 0.0, 0.0)
        cr.set_font_size(self.BALL_PITCH*0.3*self.SCALING)
        cr.show_text("  "+str(self.BALL_PITCH) + " mm pitch")

        # Draw the line indicating BGA pitch
        cr.set_source_rgb(1.0, 0.0, 0.0)
        cr.set_line_width(2)
        cr.move_to(self.OFFSET_X, self.OFFSET_Y)
        cr.line_to(self.OFFSET_X, (self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y)
        cr.stroke()

        # Draw the text indicating BGA length
        cr.move_to(self.OFFSET_X-99,int(self.OFFSET_Y+(self.NUM_PINS_LENGTH-1)*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y)/2)
        cr.set_source_rgb(0.3, 0.4, 0.5)
        cr.set_font_size(self.BALL_PITCH*0.3*self.SCALING)
        cr.show_text("  "+str(self.LENGTH) + " mm length")


        # Draw the line indicating BGA length
        cr.set_source_rgb(0.3, 0.4, 0.5)
        cr.set_line_width(2)
        cr.move_to(self.OFFSET_X - 40, self.OFFSET_Y - (self.LENGTH-self.BALL_PITCH*self.NUM_PINS_LENGTH)/2)
        cr.line_to(self.OFFSET_X - 40, (self.NUM_PINS_LENGTH-1)*(self.BALL_PITCH*self.NUM_PINS_LENGTH)*self.SCALING/self.NUM_PINS_LENGTH+self.OFFSET_Y+(self.LENGTH-self.BALL_PITCH*self.NUM_PINS_LENGTH)/2)
        cr.stroke()

        # Draw the text indicating BGA width
        cr.move_to(int(self.OFFSET_X+(self.NUM_PINS_WIDTH-1)*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X)/2, self.OFFSET_Y - 40)
        cr.set_source_rgb(0.3, 0.4, 0.5)
        cr.set_font_size(self.BALL_PITCH*0.3*self.SCALING)
        cr.show_text("  "+str(self.WIDTH) + " mm width")


        # Draw the line indicating BGA width
        cr.set_source_rgb(0.3, 0.4, 0.5)
        cr.set_line_width(2)
        cr.move_to(self.OFFSET_X - (self.WIDTH-self.BALL_PITCH*self.NUM_PINS_WIDTH)/2, self.OFFSET_Y - 40)
        cr.line_to((self.NUM_PINS_WIDTH-1)*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X+(self.WIDTH-self.BALL_PITCH*self.NUM_PINS_WIDTH)/2, self.OFFSET_Y - 40)
        cr.stroke()


        # Draw the text indicating BGA diameter
        cr.move_to(int(self.OFFSET_X+(self.NUM_PINS_WIDTH-1)*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X)/2, self.OFFSET_Y - 80)
        cr.set_source_rgb(0.3, 0.4, 0.0)
        cr.set_font_size(self.BALL_PITCH*0.3*self.SCALING)
        cr.show_text("  "+str(self.BALL_DIAMETER) + " mm diameter")

        # Draw the line indicating BGA width
        cr.set_source_rgb(0.3, 0.4, 0.0)
        cr.set_line_width(2)
        cr.arc(int(self.OFFSET_X+(self.NUM_PINS_WIDTH-1)*(self.BALL_PITCH*self.NUM_PINS_WIDTH)*self.SCALING/self.NUM_PINS_WIDTH+self.OFFSET_X)/2, self.OFFSET_Y - 60, self.BALL_DIAMETER/2*self.SCALING, 0, 2*math.pi)
        cr.fill()
 
        cr.set_source_rgb(0.3, 0.4, 0.5)
        #if self.BEGIN_MOUSE_X != self.END_MOUSE_X and self.BEGIN_MOUSE_Y != self.END_MOUSE_Y:
        cr.rectangle(self.BEGIN_MOUSE_X, self.BEGIN_MOUSE_Y, self.END_MOUSE_X - self.BEGIN_MOUSE_X , self.END_MOUSE_Y - self.BEGIN_MOUSE_Y)
        cr.stroke()

        #tedit timestamp
        self.dt = datetime.datetime.now()
        self.CALC_TEDIT = hex(int(time.mktime(self.dt.timetuple()))).upper().replace('0X','')

        self.RESULT += "(module BGA-"+str(self.PACKAGE)+"_"+str(self.NUM_PINS_WIDTH)+"x"+str(self.NUM_PINS_LENGTH)+"_"+str(self.WIDTH)+"x"+str(self.LENGTH)+"mm_Pitch"+str(self.BALL_PITCH)+"mm (layer F.Cu) (tedit "+str(self.CALC_TEDIT)+")" + "\n"
        self.RESULT += "  (descr \"BGA-"+str(self.PACKAGE)+", "+str(self.NUM_PINS_WIDTH)+"x"+str(self.NUM_PINS_LENGTH)+", "+str(self.WIDTH)+"x"+str(self.LENGTH)+"mm package, pitch "+str(self.BALL_PITCH)+"mm\")" + "\n"
        self.RESULT += "  (tags BGA-"+str(self.PACKAGE)+")" + "\n"
        self.RESULT += "  (attr smd)" + "\n"
        self.RESULT += "  (fp_text reference REF** (at 0 "+ str(-self.CALC_WIDTH/2-1.50-self.BALL_DIAMETER) +") (layer F.SilkS)" + "\n"
        self.RESULT += "    (effects (font (size 1 1) (thickness 0.15)))" + "\n"
        self.RESULT += "  )" + "\n"
        self.RESULT += "  (fp_text value BGA-"+str(self.PACKAGE)+"_"+str(self.NUM_PINS_WIDTH)+"x"+str(self.NUM_PINS_LENGTH)+"_"+str(self.WIDTH)+".0x"+str(self.LENGTH)+".0mm_Pitch"+str(self.BALL_PITCH)+"mm (at 0 "+ str(self.CALC_WIDTH/2+1.50+self.BALL_DIAMETER) +") (layer F.Fab)" + "\n"
        self.RESULT += "    (effects (font (size 1 1) (thickness 0.15)))" + "\n"
        self.RESULT += "  )" + "\n"

        # Below parameters may be adjusted.

        # Top left -> right angular F.Silk
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2+0.1)+" -"+ str(+self.LENGTH/2-1.70)+") (end -"+ str(self.WIDTH/2+0.1)+" -"+ str(self.LENGTH/2+0.1)+") (layer F.SilkS) (width 0.12))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2+0.1)+" -"+ str(+self.LENGTH/2+0.1)+") (end -"+ str(self.WIDTH/2-1.70)+" -"+ str(self.LENGTH/2+0.1)+") (layer F.SilkS) (width 0.12))" + "\n"

        # F.SilkS Box
        self.RESULT += "  (fp_line (start "+ str(self.WIDTH/2)+" -"+ str(+self.LENGTH/2)+") (end -"+ str(self.WIDTH/2)+" -"+ str(self.LENGTH/2)+") (layer F.SilkS) (width 0.12))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2)+" -"+ str(+self.LENGTH/2)+") (end -"+ str(self.WIDTH/2)+" "+ str(self.LENGTH/2)+") (layer F.SilkS) (width 0.12))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2)+" "+ str(+self.LENGTH/2)+") (end "+ str(self.WIDTH/2)+" "+ str(self.LENGTH/2)+") (layer F.SilkS) (width 0.12))" + "\n"
        self.RESULT += "  (fp_line (start "+ str(self.WIDTH/2)+" "+ str(+self.LENGTH/2)+") (end "+ str(self.WIDTH/2)+" -"+ str(self.LENGTH/2)+") (layer F.SilkS) (width 0.12))" + "\n"

        # F.Fab Box
        self.RESULT += "  (fp_line (start "+ str(self.WIDTH/2-0.1)+" -"+ str(+self.LENGTH/2-0.1)+") (end -"+ str(self.WIDTH/2-0.1)+" -"+ str(self.LENGTH/2-0.1)+") (layer F.Fab) (width 0.1))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2-0.1)+" -"+ str(+self.LENGTH/2-0.1)+") (end -"+ str(self.WIDTH/2-0.1)+" "+ str(self.LENGTH/2-0.1)+") (layer F.Fab) (width 0.1))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2-0.1)+" "+ str(+self.LENGTH/2-0.1)+") (end "+ str(self.WIDTH/2-0.1)+" "+ str(self.LENGTH/2-0.1)+") (layer F.Fab) (width 0.1))" + "\n"
        self.RESULT += "  (fp_line (start "+ str(self.WIDTH/2-0.1)+" "+ str(+self.LENGTH/2-0.1)+") (end "+ str(self.WIDTH/2-0.1)+" -"+ str(self.LENGTH/2-0.1)+") (layer F.Fab) (width 0.1))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2-0.1)+" -"+ str(+self.LENGTH/2-0.5)+") (end -"+ str(self.WIDTH/2-0.5)+" -"+ str(self.LENGTH/2-0.1)+") (layer F.Fab) (width 0.1))" + "\n"

        # F.CrtYd Box
        self.RESULT += "  (fp_line (start "+ str(self.WIDTH/2+0.7)+" -"+ str(+self.LENGTH/2+0.7)+") (end -"+ str(self.WIDTH/2+0.7)+" -"+ str(self.LENGTH/2+0.7)+") (layer F.CrtYd) (width 0.05))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2+0.7)+" -"+ str(+self.LENGTH/2+0.7)+") (end -"+ str(self.WIDTH/2+0.7)+" "+ str(self.LENGTH/2+0.7)+") (layer F.CrtYd) (width 0.05))" + "\n"
        self.RESULT += "  (fp_line (start -"+ str(self.WIDTH/2+0.7)+" "+ str(+self.LENGTH/2+0.7)+") (end "+ str(self.WIDTH/2+0.7)+" "+ str(self.LENGTH/2+0.7)+") (layer F.CrtYd) (width 0.05))" + "\n"
        self.RESULT += "  (fp_line (start "+ str(self.WIDTH/2+0.7)+" "+ str(+self.LENGTH/2+0.7)+") (end "+ str(self.WIDTH/2+0.7)+" -"+ str(self.LENGTH/2+0.7)+") (layer F.CrtYd) (width 0.05))" + "\n"

        #Origin X and Y for SMD balls
        for i in range(0, len(self.populate)):
            pt_x = -self.CALC_WIDTH/2+self.populate[i][0]*self.BALL_PITCH
            pt_y = -self.CALC_LENGTH/2+self.populate[i][1]*self.BALL_PITCH
            self.RESULT += "(pad "+str(self.COL[self.populate[i][1]]+str(self.ROW[self.populate[i][0]]))+" smd circle (at "+str(pt_x)+" "+str(pt_y)+") (size "+str(self.CALC_BALL_DIAMETER)+" "+str(self.CALC_BALL_DIAMETER)+") (layers F.Cu F.Paste F.Mask))" + "\n"

        self.RESULT += "  #3D model section is commented below. Uncomment if WRL file available" + "\n"
        self.RESULT += "  #(model Housings_BGA.3dshapes/BGA-"+str(self.PACKAGE)+"_"+str(self.NUM_PINS_WIDTH)+"x"+str(self.NUM_PINS_LENGTH)+"_"+str(self.WIDTH)+"x"+str(self.LENGTH)+"mm_Pitch"+str(self.BALL_PITCH)+"mm.wrl" + "\n"
        self.RESULT += "  #  (at (xyz 0 0 0))" + "\n"
        self.RESULT += "  #  (scale (xyz 1 1 1))" + "\n"
        self.RESULT += "  #  (rotate (xyz 0 0 0))" + "\n"
        self.RESULT += "  #)" + "\n"

        self.RESULT += ")" + "\n"
        #print self.RESULT
        return False

PyApp()
Gtk.main()

