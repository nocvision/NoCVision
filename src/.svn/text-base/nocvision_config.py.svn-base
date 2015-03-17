from __future__ import division
from matplotlib.pylab import *
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import Tkinter as tk
import math
import ConfigParser
import re
import matplotlib.cm as cm
import numpy as np
import random
from operator import itemgetter

from connectivity import *
from get_family import *

packets = {}
curr_timestamp = -1 
prev_timestamp = -1 
nxt_timestamp = -1 
src = 0
dest = 0
section = ''
node_width = 40
node_spacing = 40

id_labels = [0 for x in range(10)]
id_rects = [0 for x in range(10)]
restart_params = 1
i=0
j=0
x0=0
x1=0
y0=0
y1=0

newidreqested = 1

display = 0

## Custom Colormap for matplotlib
cdict = {'red':   ((0.0,  1.0, 1.0),
                   (1.0,  0.0, 0.0)),

         'green': ((0.0,  0.0, 0.0),
                   (1.0,  0.0, 0.0)),

         'blue':  ((0.0,  0.0, 0.0),
                   (1.0,  0.0, 0.0))}

cdict1 = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 0.1),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 1.0),
                   (0.5, 0.1, 0.0),
                   (1.0, 0.0, 0.0))
        }
cdict_green = {'red':   ((0.0, 1.0, 1.0),
                   (1.0, 0.0, 0.0)),

         'green': ((0.0, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),

         'blue':  ((0.0, 1.0, 1.0),
                   (1.0, 0.0, 0.0))
        }

blue_red = LinearSegmentedColormap('BlueRed', cdict1)
green_black = LinearSegmentedColormap('Greenblack', cdict_green)
plt.register_cmap(cmap=blue_red)
plt.register_cmap(cmap=green_black)
fig = Figure(figsize=(5,4), dpi=100)


nodes = 0
def exit_gui():
   frame1.quit()

def exit_sys():
   sys.exit()

root = tk.Tk()
root.wm_title("NoCVision")
top = root.winfo_toplevel()
top.rowconfigure(0,weight=1)
top.columnconfigure(0,weight=1)
frame1 = tk.Frame(root)
frame1.rowconfigure(0,weight=1)
frame1.columnconfigure(0,weight=1)
frame1.grid()
frame2 = tk.Frame(frame1)
frame2.rowconfigure(0,weight=1)
frame2.columnconfigure(0,weight=1)
frame2.grid(row=2,column=1)
frame3 = tk.Frame(frame1)
frame3.rowconfigure(0,weight=1)
frame3.columnconfigure(0,weight=1)



try:
   conf_file_name = sys.argv[1]
except:
   print "Error: Argument missing, please provide configuration file"
   exit_sys()
init_file = open(conf_file_name,'r')
value_regex = re.compile('^(\D*)(:)(.*)\n$')

with open(conf_file_name,'r') as init_file:
   for line in init_file:
      if 'k:' in line:
         xnodes = eval(value_regex.search(line).groups()[2])
      elif 'topology:' in line:
         topology = eval(value_regex.search(line).groups()[2])
      elif 'num_vcs:' in line:
         num_vcs = eval(value_regex.search(line).groups()[2])



x_epoch_label = 300 - node_spacing/2 + (((int)(math.floor(((300 + (node_width+node_spacing)*xnodes) + (300+node_width + (node_width+node_spacing)*xnodes))/2))) - ((int)(math.floor((300 + (300+node_width))/2))))/2
y_epoch_label = (int)(math.floor((200 + (200+node_width))/2)) - 80
x_info_label = 300 - node_spacing/2 + (((int)(math.floor(((300 + (node_width+node_spacing)*xnodes) + (300+node_width + (node_width+node_spacing)*xnodes))/2))) - ((int)(math.floor((300 + (300+node_width))/2))))/2
y_info_label = (int)(math.floor((200 + (200+node_width))/2)) - 60
canvas_height =  ((int)(math.floor(((300 + (node_width+node_spacing)*xnodes) + (300+node_width + (node_width+node_spacing)*xnodes))/2))) + 100
canvas_width = ((int)(math.floor(((300 + (node_width+node_spacing)*xnodes) + (300+node_width + (node_width+node_spacing)*xnodes))/2))) + 100

canvas = tk.Canvas(frame1,bg="#FFFFFF",height=canvas_height ,width=canvas_width,relief=tk.GROOVE,bd=4)
hbar = tk.Scrollbar(frame1,orient=tk.HORIZONTAL)
hbar.config(command=canvas.xview)
vbar = tk.Scrollbar(frame1,orient=tk.VERTICAL)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set)


nodes = xnodes * xnodes
link = [[0 for i in range(4)] for i in range(nodes)]
link = connectivity(topology,xnodes)
x_node_st = 20
x_node_end = xnodes*node_width + (xnodes-1)*node_spacing
y_node_st = 20
y_node_end = xnodes*node_width + (xnodes-1)*node_spacing
router_id = [[0 for x in xrange(xnodes)] for x in xrange(xnodes)]
router_id_txt = [[0 for x in xrange(xnodes)] for x in xrange(xnodes)]

colorbarxcoord = 100 
colorbarycoord = (int)(200 + math.floor((xnodes*(node_width) + (xnodes-1)*(node_spacing))/2) )

packet = [[0 for i in range(4)] for i in range(nodes)]
router_info_acc = [0.0 for i in range(nodes)]
vc_parameters = [[[0 for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
link_id = [[0 for x in range(4)] for x in range(nodes)]

canvas_vc = tk.Canvas(frame1,bg="#FFFFFF",height=800,width=400)
def extract_config(file_path):
   new_file = open('config_file.log','w')
   old_file = open(file_path)
   for line in old_file:
      if (re.search('^motivator_.*',line) != None) | (re.search('^\[clock.*',line) != None):
         new_file.write(line)


extract_config(conf_file_name)

config = ConfigParser.ConfigParser()
config.read('config_file.log')
epoch_list = config.sections()
epoch = []
epochpattern = re.compile('^\D*(\d*)$')
for elem in epoch_list:
   epoch.append(eval(epochpattern.search(elem).groups()[0]))

for section in config.sections():
   try:
      for option in config.options(section):
         if (get_family(nodes,num_vcs,eval(config.get(section,option))) == -1):
	    print "Invalid format section: %s, option: %s"%(section,option)
	    exit_sys()
   except ConfigParser.NoOptionError:
      continue


eventParsePattern = re.compile(r'^(motivator):(\D*):')
clockPattern = re.compile(r'(clock_)(\d*)')
pidPattern = re.compile(r'(pid_)(\d*)')
nodePattern = re.compile(r'(node_)(\d*)')
linkPattern = re.compile(r'(link_)(\D*\d*)')
vcPattern = re.compile(r'(vc_)(\d*)')

eventConfig = ConfigParser.ConfigParser()
event_packet_ids = []
event_info = {}
event_dict = []
event_dict_asc = []

with open(conf_file_name,'r') as event_file:
   for line in event_file:
      if (eventParsePattern.search(line) != None):
	 event_info = {
         "transaction": eventParsePattern.search(line).groups()[1],
         "clock": eval(clockPattern.search(line).groups()[1]),
         "pid": eval(pidPattern.search(line).groups()[1]),
         "node": eval(nodePattern.search(line).groups()[1]),
         "link": eval(linkPattern.search(line).groups()[1]),
         "vc": eval(vcPattern.search(line).groups()[1])
	 }
         event_dict.append(event_info) 
         if eventParsePattern.search(line).groups()[1] == 'trans':
	   event_packet_ids.append(pidPattern.search(line).groups()[1])
	 if ((eventParsePattern.search(line).groups()[1] == 'pin') | (eventParsePattern.search(line).groups()[1] == 'unpin')):
	   event_packet_ids.append("-1")

def createConfigParser(eventConfig, transaction, clock,pid,node,link,vc):
   packet = [[0 for i in range(5)] for i in range(nodes)]
   vc_packets = [[[0 for i in range(num_vcs)] for i in range(5)] for i in range(nodes)]
   event_sections = eventConfig.sections()
   if (eventConfig.has_section('clock = %d'%clock) == False):
     try:
       packet = eval(eventConfig.get(event_sections[len(event_sections)-1],'packet'))
       for i in range(nodes):
         for j in range(5):
           if(packet[i][j] == -1):
             packet[i][j] = -1
	   else:
             packet[i][j] = 0

     except:
       packet = [[0 for i in range(5)] for i in range(nodes)]
     eventConfig.add_section('clock = %d'%clock)
   else:
     packet = eval(eventConfig.get('clock = %d'%clock,'packet'))

   if (eventConfig.has_section('clock = %d'%clock) == False):
      eventConfig.add_section('clock = %d'%clock)
      

   if (eventConfig.has_option('clock = %d'%clock, 'vc_packets') == True):
      vc_packets = eval(eventConfig.get('clock = %d'%clock,'vc_packets'))
   else:
      vc_packets = [[[0 for i in range(num_vcs)] for i in range(5)] for i in range(nodes)]
   if (transaction == 'pin'):
     link = -1
     pid = -1
   elif (transaction == 'unpin'):
     link = -1
     pid = 0
   vc_packets[node][link][vc] = pid
   packet[node][link] = pid
   eventConfig.set('clock = %d'%clock,'packet', (str)(packet))
   eventConfig.set('clock = %d'%clock,'vc_packets', (str)(vc_packets))
   return eventConfig

event_dict_asc = sorted(event_dict,key=itemgetter('clock'))
for item in event_dict_asc:
  eventConfig = createConfigParser(eventConfig, item['transaction'], item['clock'], item['pid'], item['node'], item['link'], item['vc'])
  

event_epoch_list = eventConfig.sections()
eventEpochpattern = re.compile('^(\D*) = (\d*)')
event_epoch = []
for elem in event_epoch_list:
   event_epoch.append(eval(eventEpochpattern.search(elem).groups()[1]))


event_epoch_asc = sorted(event_epoch,key=int)

parameter_options = []
parameter_options_nodup = []
for i in epoch_list:
   parameter_options.extend(config.options(i))

for i in parameter_options:
   if i not in parameter_options_nodup:
      parameter_options_nodup.append(i)
parameter_options = parameter_options_nodup

packet_trace=tk.IntVar()
option_sel =tk.StringVar()
event_start_ip = tk.IntVar()
parameter_options_sorted = []
option_prop = ['accumulate', 'minimum', 'maximum', 'average']
op_prop_sel = tk.StringVar()

epoch_asc = sorted(epoch,key=int)
try:
 epoch_smallest_step = epoch_asc[1] - epoch_asc[0]
except:
 epoch_smallest_step = 0 
