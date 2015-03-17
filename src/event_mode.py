# Copyright (c) 2015, University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

from nocvision_config import *
from rgb_to_hex import *
from restart import *
from display_values import *


def event_mode(event_start_usr_def,packet_op):
      epoch_label = canvas.create_text(x_epoch_label,y_epoch_label,anchor=tk.CENTER)
      packet_info_txt = canvas.create_text(x_info_label,y_info_label)
      globals()['newidreqested'] = 0
      epoch_asc = sorted(epoch,key=int)
      packet_event_option = []
      global nxt_timestamp
      nxt_timestamp = event_start_usr_def

      packetlabel = tk.Label(frame2, text="Packet id(s)")
      packetlabel.grid(row=0,column=0)
      id_selected = [tk.IntVar()]
      packetCBBox = [0]
      num_id=0
      for items in list(set(event_packet_ids)):
        if (items == "-1"):
      	  packetCBBox[num_id] = tk.Checkbutton(frame2,text="pin items",variable=id_selected[num_id],onvalue=1,offvalue=0)
	else:
      	  packetCBBox[num_id] = tk.Checkbutton(frame2,text=items,variable=id_selected[num_id],onvalue=1,offvalue=0)
      	packetCBBox[num_id].grid(row=1+num_id,column=0)
	num_id=num_id+1
	packetCBBox.append(0)
      	id_selected.append(tk.IntVar())
      packetCBBox[num_id] = tk.Checkbutton(frame2,text='all',variable=id_selected[num_id],onvalue=1,offvalue=0)
      packetCBBox[num_id].grid(row=2+num_id,column=0)

      packetidbutton = tk.Button(frame2, text="enter",command=exit_gui)
      packetidbutton.grid(row=1,column=3)
      packetexitbutton = tk.Button(frame2, text="exit",command=exit_sys)
      packetexitbutton.grid(row=1,column=4)
      frame1.mainloop()
      packet_id = []
      packetlabel.grid_remove()
      packetidbutton.grid_remove()
      packetexitbutton.grid_remove()

      for i in range(num_id+1):
      	packetCBBox[i].grid_remove()

      if (id_selected[num_id].get()):
      	for items in list(set(event_packet_ids)):
      	   packet_id.append(eval(items))
      else:      
      	for i in range(num_id):
      	   if (id_selected[i].get()):
	      packet_id.append(eval(list(set(event_packet_ids))[i]))
      intensity = []
      for k in (range(len(packet_id))):
      	intensity.append('#%02X%02X%02X'%(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
      packetexitbutton = tk.Button(frame2, text="exit",command=exit_sys)
      packetexitbutton.grid(row=0,column=1)
      packetnxtbutton = tk.Button(frame2, text="next>>",repeatinterval=1, repeatdelay=1000, command=lambda: packetnext(ts=nxt_timestamp,epoch_asc=epoch_asc,packet_id=packet_id,sign=1,intensity=intensity,epoch_label=epoch_label,packet_info_txt=packet_info_txt,packet_op=packet_op))
      packetnxtbutton.grid(row=0,column=2)
      packetprevbutton = tk.Button(frame2, text="<<prev",repeatinterval=1, repeatdelay=1000, command=lambda: packetnext(ts=prev_timestamp,epoch_asc=epoch_asc,packet_id=packet_id, sign=-1,intensity=intensity,epoch_label=epoch_label,packet_info_txt=packet_info_txt,packet_op=packet_op))
      packetprevbutton.grid(row=0,column=0)
      packetnewidbutton = tk.Button(frame2, text="enter new id",command=lambda: newidreq(packet_id=packet_id,epoch_label=epoch_label))
      packetnewidbutton.grid(row=1,column=1)
      packetrestartbutton = tk.Button(frame2, text="enter options again", command=restart)
      packetrestartbutton.grid(row=2,column=1)


      frame1.mainloop()
      canvas.delete(epoch_label)
      canvas.delete(packet_info_txt)
      packetexitbutton.grid_remove()
      packetnxtbutton.grid_remove()
      packetprevbutton.grid_remove()
      packetrestartbutton.grid_remove()
      packetnewidbutton.grid_remove()

def newidreq(packet_id,epoch_label):
   canvas.delete(epoch_label)
   for i in range(len(packet_id)):
      canvas.delete(id_labels[i])
      canvas.delete(id_rects[i])
   for child in frame1.winfo_children():
      child.grid_remove()
   globals()['newidreqested'] = 1
   exit_gui()

def search2Dlist(l, elem):
   column = 0
   for row,i in enumerate(l):
      try:
         column = i.index(elem)
      except ValueError:
         continue
      return row,column
   return -1


def packetnext(ts,epoch_asc,packet_id,sign,intensity,epoch_label,packet_info_txt,packet_op):
      iter = 0
      i = 0
      global nxt_timestamp
      global prev_timestamp 
      global curr_timestamp 
      canvas.itemconfig(epoch_label,text='')
      canvas.itemconfig(packet_info_txt,text='')
      canvas_vc.grid_remove()
      frame3.grid_remove()
      for k in range(len(packet_id)):
         canvas.delete(id_labels[k])
	 canvas.delete(id_rects[k])
      max_packet_id = max(packet_id)
      min_packet_id = min(packet_id)
      normalized_packet_id = 0.0

      for i in range(nodes):
	 row = (int)(math.floor(i / xnodes));
	 column = i%xnodes;
	 canvas.itemconfig(router_id[row][column],fill = 'white')
         for j in range(4):
	    canvas.itemconfig(link_id[i][j],fill = 'black')

      while (iter != 1):
               section = 'clock = %d' %ts
               packet = eval(eventConfig.get(section,'packet'))
               for k in range(len(packet_id)):
                  if search2Dlist(packet,packet_id[k]) != -1:
                     i,j = search2Dlist(packet,packet_id[k])
                     col = 'red'
		     link_intensity = '#%02X%02X%02X'%(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		     if j != 4:
                     	canvas.itemconfig(link_id[i][j],fill = intensity[k])
		     else:
	          	row = (int)(math.floor(i / xnodes));
		  	column = i%xnodes;
	          	canvas.itemconfig(router_id[row][column],fill = intensity[k])
                     canvas.itemconfig(epoch_label, text = 'clock = %d'%ts)
		     if (packet_id[k]>=0):
                       id_rects[k] = canvas.create_rectangle(30,50+50*k,70,70+50*k,fill = intensity[k])
                       id_labels[k] = canvas.create_text(80,60+50*k,text='packet id %d'%packet_id[k],anchor='w')
                     iter = 1

                  for row,i in enumerate(packet):
		    try:
		      column = i.index(-1)
	              col = 'red'
	              j = (int)(math.floor(row / xnodes));
		      k = row%xnodes;
	              canvas.itemconfig(router_id[j][k],fill = col)
                    except ValueError:
                      continue

	      
               if sign == 1:
                  if event_epoch_asc.index(ts) < len(event_epoch_asc) - 1:
                     prev_timestamp = curr_timestamp
                     curr_timestamp = nxt_timestamp
                     nxt_timestamp = event_epoch_asc[event_epoch_asc.index(ts)+1]
                     ts = nxt_timestamp
                  else:
	             if (event_epoch_asc.index(curr_timestamp) < len(event_epoch_asc) - 1):
                        prev_timestamp = curr_timestamp
		     else:
                        prev_timestamp = prev_timestamp
                     curr_timestamp = nxt_timestamp
                     nxt_timestamp = curr_timestamp
                     ts = nxt_timestamp
                     iter = 1
                     
               elif event_epoch_asc.index(ts) != 0:
                  nxt_timestamp = curr_timestamp
                  curr_timestamp = prev_timestamp
                  prev_timestamp = event_epoch_asc[event_epoch_asc.index(ts)-1]
                  ts = prev_timestamp
               else:
	          if (event_epoch_asc.index(curr_timestamp)):
                     nxt_timestamp = curr_timestamp
		  else:
                     nxt_timestamp = nxt_timestamp
                  curr_timestamp = prev_timestamp
                  prev_timestamp = curr_timestamp
                  ts = prev_timestamp
                  iter = 1

               if (ts > event_epoch_asc[len(event_epoch_asc) - 1]) | (ts < event_epoch_asc[0]):
                  break
         
	 

      globals()['display'] = 1
      for i in range(nodes):
         for j in range(4):
	    if link_id[i][j] != 0:
	       canvas.tag_bind (link_id[i][j],"<Double-Button-1>",lambda event, arg=(curr_timestamp,packet_info_txt,packet_op,'undef','undef',1,'undef'):display_values(event,arg))
               canvas.tag_bind (link_id[i][j],"<Shift-ButtonRelease>",lambda event, arg=(curr_timestamp,packet_info_txt,packet_op,'undef','undef',1,'undef'):display_values(event,arg))

      if iter == 0:
         canvas.itemconfig(epoch_label, text = 'No more packets with given ids found!')
         for i in range(nodes):
            for j in range(4):
	       if link_id[i][j] !=0:
                  canvas.tag_unbind (link_id[i][j],"<Double-Button-1>")
                  canvas.tag_unbind (link_id[i][j],"<Shift-ButtonRelease>")
