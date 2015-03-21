# ----------------------------------------
# NoCVision
# Copyright 2014 The Regents of the University of Michigan
# Vaibhav Gogte, Ritesh Parikh, Valeria Bertacco
# 
# NocVision is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------------------------

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


def trafficnext(ts,epoch_asc,sign,option_prop_selected,family_selected,epoch_skip_steps,option_selected,epoch_jump_usr_def,packet_op,epoch_label,packet_info_txt):
      iter = 0
      no_of_loops = 0
      global nxt_timestamp
      global prev_timestamp 
      global curr_timestamp 
      canvas.itemconfig(epoch_label,text='')
      canvas.itemconfig(packet_info_txt,text='')
      if  (option_prop_selected == 'accumulate') | (option_prop_selected == 'average') | (option_prop_selected == 'maximum'):
         packet_retr = [[0 for l in range(4)] for l in range(nodes)]
         vc_parameters = [[[0 for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
         router_retr = [0 for l in range(nodes)]
	 temp_var = 0
      elif option_prop_selected == 'minimum':
         packet_retr = [[(float('Infinity')) for l in range(4)] for l in range(nodes)]
         temp_var = float('inf')
         router_retr = [float('Infinity') for l in range(nodes)]
         vc_parameters = [[[float('Infinity') for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]

      router_info_acc = [0 for i in range(nodes)]
      vc_param_retr = [[[0 for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
      canvas_vc.grid_remove()
      frame3.grid_remove()
      packet_normalized = [[0.0 for x in range(4)] for x in range(nodes)]
      router_normalized = [0.0 for x in range(nodes)]
      intensity = [['#000fff000' for x in range(4)] for x in range(nodes)]
      
      for elem in epoch_asc:
         if iter == 0:
            if elem == ts:
               packet = [[0 for i in range(4)] for i in range(nodes)]


	       if family_selected == 'link':
	          for i in range(epoch_skip_steps):
		     try:
		        section = 'clock = %d' %(elem-(epoch_smallest_step*i))
		        for a in range(nodes):
			   for b in range(4):
			      if (option_prop_selected == 'accumulate') | (option_prop_selected == 'average'):
   		                 packet_retr[a][b] += (eval(config.get(section,option_selected)))[a][b]
			      elif (option_prop_selected == 'minimum'):
			         if packet_retr[a][b] > (eval(config.get(section,option_selected)))[a][b]:
				    packet_retr[a][b] = (eval(config.get(section,option_selected)))[a][b]
			      else:
			         if  packet_retr[a][b] < (eval(config.get(section,option_selected)))[a][b]:
				    packet_retr[a][b] = (eval(config.get(section,option_selected)))[a][b]
                        no_of_loops+=1

		     except ConfigParser.NoSectionError:
		        packet_retr = packet_retr

	          if option_prop_selected == 'average':
	             for a in range(nodes):
	                for b in range(4):
	                   packet[a][b] = packet_retr[a][b]/no_of_loops
	          else:
	             packet = packet_retr




	       elif family_selected == 'vc':
	          for i in range(epoch_skip_steps):
		     try:
		        section = 'clock = %d' %(elem-(epoch_smallest_step*i))
                        vc_param_retr = eval(config.get(section,option_selected))
		        for a in range(nodes):
			   for b in range(4):
			      for c in range(num_vcs):
		                 if (option_prop_selected == 'accumulate') | (option_prop_selected == 'average'):
  		                    vc_parameters[a][b][c] += vc_param_retr[a][b][c]

		                 elif option_prop_selected == 'minimum':
		                    if vc_parameters[a][b][c] > vc_param_retr[a][b][c]:
		                       vc_parameters[a][b][c] = vc_param_retr[a][b][c]
		                 else:
		                    if  vc_parameters[a][b][c] < vc_param_retr[a][b][c]:
		                       vc_parameters[a][b][c] = vc_param_retr[a][b][c]
			      
                        no_of_loops+=1
		     except ConfigParser.NoSectionError:
		        packet = packet

                     if option_prop_selected == 'average':
                        for j in range (nodes):
                           for k in range(4):
                              for l in range(num_vcs):
                       	         vc_parameters[j][k][l] = vc_parameters[j][k][l]/no_of_loops


                  for a in range(nodes):
                     for b in range(4):
                        for c in range(num_vcs):
                              if (option_prop_selected == 'accumulate') | (option_prop_selected == 'average'):
                                 packet_retr[a][b] = packet_retr[a][b] + vc_parameters[a][b][c]
                              elif option_prop_selected == 'minimum':
                                 if packet_retr[a][b] > vc_parameters[a][b][c]:
                                    packet_retr[a][b] = vc_parameters[a][b][c]
                              else:
                                 if  packet_retr[a][b] < vc_parameters[a][b][c]:
                                    packet_retr[a][b] = vc_parameters[a][b][c]
                  if (option_prop_selected == 'average'):
                     for a in range(nodes):
                        for b in range(4):
                           packet[a][b] = packet_retr[a][b]/num_vcs
                  else:
	             packet = packet_retr


               elif family_selected == 'router':
                 for i in range(epoch_skip_steps):
                    try:
                       section = 'clock = %d' %(elem-(epoch_smallest_step*i))
                       for j in range(nodes):
                          if (option_prop_selected == 'accumulate') | (option_prop_selected == 'average'):
                             router_retr[j] += (eval(config.get(section,option_selected)))[j]
                          elif (option_prop_selected == 'minimum'):
                  	   if router_retr[j] > (eval(config.get(section,option_selected)))[j]:
                                router_retr[j] = (eval(config.get(section,option_selected)))[j]
                  	  else:
                  	    if  router_retr[j] < (eval(config.get(section,option_selected)))[j]:
                  		    router_retr[j] = (eval(config.get(section,option_selected)))[j]
                       no_of_loops += 1
                    except:
                       router_retr = router_retr
	         if option_prop_selected == 'average':
	           for a in range(nodes):
	             router_info_acc[a] = router_retr[a]/no_of_loops
	         else:
	           router_info_acc = router_retr


## Calculating router values based on the inflowing packets in it through adjacent links.
               if ((family_selected == 'link') | (family_selected == 'vc')):
                 if (option_prop_selected == 'accumulate') :
                  for a in range(nodes):
                     try:
                        if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <= (nodes-1)):
                           router_retr[a] += packet[a-xnodes][2]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+xnodes][0] >=0) & (link[a+xnodes][0] <= (nodes-1)):
                           router_retr[a] += packet[a+xnodes][0]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a-1][1] >=0) & (link[a-1][1] <= (nodes-1)):
                           router_retr[a] += packet[a-1][1]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+1][3] >=0) & (link[a+1][3] <= (nodes-1)):
                           router_retr[a] += packet[a+1][3]
                     except:
                        router_retr[a] = router_retr[a]
	          router_info_acc = router_retr

	         elif (option_prop_selected == 'minimum'):
                  for a in range(nodes):
                     try:
                        if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <=(nodes-1)):
			   if router_retr[a] > packet[a-xnodes][2]:
                              router_retr[a] = packet[a-xnodes][2]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+xnodes][0] >=0) & (link[a+xnodes][0] <= (nodes-1)):
			   if router_retr[a] > packet[a+xnodes][0]:
                              router_retr[a] = packet[a+xnodes][0]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a-1][1] >=0) & (link[a-1][1] <= (nodes-1)):
			   if router_retr[a] > packet[a-1][1]:
                              router_retr[a] = packet[a-1][1]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+1][3] >=0) & (link[a+1][3] <= (nodes-1)):
			   if router_retr[a] > packet[a+1][3]:
                              router_retr[a] = packet[a+1][3]
                     except:
                        router_retr[a] = router_retr[a]             
	          router_info_acc = router_retr

	         elif (option_prop_selected == 'maximum'):
                  for a in range(nodes):
                     try:
                        if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <=(nodes-1)):
			   if router_retr[a] < packet[a-xnodes][2]:
                              router_retr[a] = packet[a-xnodes][2]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+xnodes][0] >=0) & (link[a+xnodes][0] <= (nodes-1)):
			   if router_retr[a] < packet[a+xnodes][0]:
                              router_retr[a] = packet[a+xnodes][0]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a-1][1] >=0) & (link[a-1][1] <= (nodes-1)):
			   if router_retr[a] < packet[a-1][1]:
                              router_retr[a] = packet[a-1][1]
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+1][3] >=0) & (link[a+1][3] <= (nodes-1)):
			   if router_retr[a] < packet[a+1][3]:
                              router_retr[a] = packet[a+1][3]
                     except:
                        router_retr[a] = router_retr[a]             
	          router_info_acc = router_retr

                 elif (option_prop_selected == 'average') :
                  for a in range(nodes):
		     no_of_loops = 0
                     try:
                        if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <= (nodes-1)):
                           router_retr[a] += packet[a-xnodes][2]
			   no_of_loops+=1
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+xnodes][0] >=0) & (link[a+xnodes][0] <= (nodes-1)):
                           router_retr[a] += packet[a+xnodes][0]
			   no_of_loops+=1
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a-1][1] >=0) & (link[a-1][1] <= (nodes-1)):
                           router_retr[a] += packet[a-1][1]
			   no_of_loops+=1
                     except:
                        router_retr[a] = router_retr[a]
                     try:
                        if (link[a+1][3] >=0) & (link[a+1][3] <= nodes-1):
                           router_retr[a] += packet[a+1][3]
			   no_of_loops+=1
                     except:
                        router_retr[a] = router_retr[a]

                     router_info_acc[a] = router_retr[a]/no_of_loops
               if sign == 1:
	          if (nxt_timestamp + epoch_jump_usr_def) <= epoch_asc[len(epoch_asc)-1]:
	             prev_timestamp = curr_timestamp
	             curr_timestamp = nxt_timestamp
                     nxt_timestamp = curr_timestamp + epoch_jump_usr_def
		  else:
	             prev_timestamp = curr_timestamp
	             curr_timestamp = nxt_timestamp
                     nxt_timestamp = curr_timestamp
		     
	       elif (prev_timestamp - epoch_jump_usr_def) >= epoch_asc[0]:
	          nxt_timestamp = curr_timestamp
	          curr_timestamp = prev_timestamp
		  prev_timestamp = curr_timestamp - epoch_jump_usr_def
	       else:
	          nxt_timestamp = curr_timestamp
	          curr_timestamp = prev_timestamp
		  prev_timestamp = curr_timestamp
               
	       iter = 1
               if ((family_selected == 'link') | (family_selected == 'vc')):
	         max_traffic = 0
	         for i in range(nodes):
	           for j in range(4):
		     if packet[i][j] > max_traffic:
		        max_traffic = packet[i][j]
	         min_traffic = max_traffic
	         for i in range(nodes):
	           for j in range(4):
		     if (link[i][j] >= 0) & (link[i][j] <= (nodes-1)):
		        if packet[i][j] < min_traffic:
			   min_traffic = packet[i][j]
	         for i in range(nodes):
	           for j in range(4):
		     if (link[i][j] >=0) & (link[i][j] <= (nodes-1)) & (max_traffic-min_traffic != 0):
		        packet_normalized[i][j] = (packet[i][j]-min_traffic)/(max_traffic-min_traffic)
		        intensity[i][j] = rgb_to_hex(((0.8*(math.ceil(packet_normalized[i][j] * 4095))),0,(4095 -(math.ceil(packet_normalized[i][j] * 4095)))))

		     else:
		        packet_normalized[i][j] = 0.0
		        intensity[i][j] = rgb_to_hex(((0.8*(math.ceil(packet_normalized[i][j] * 4095))),0,(4095 -(math.ceil(packet_normalized[i][j] * 4095)))))
	         canvas.itemconfig(epoch_label, text = 'clock = %d'%elem)
                 for i in range(nodes):
                   for j in range(4):
		     if (link[i][j] >= 0) & (link[i][j] <= (nodes-1)):
		        canvas.itemconfig(link_id[i][j], fill = intensity[i][j])
	       max_traffic = 0.0
	       for i in range(nodes):
	         if router_info_acc[i] > max_traffic:
	           max_traffic = router_info_acc[i]
	       min_traffic = max_traffic
	       for i in range(nodes):
		 if router_info_acc[i] < min_traffic:
		   min_traffic = router_info_acc[i]
	       for i in range(nodes):
	         if (int)(max_traffic-min_traffic) != 0:
		   router_normalized[i] = (router_info_acc[i]-min_traffic)/(max_traffic-min_traffic)
		   intensity[i] = rgb_to_hex((4095 - (math.ceil(router_normalized[i] * 4095)), 4095, 4095 - (math.ceil(router_normalized[i] * 4095))))
		 else:
 		   router_normalized[i] = 0.0
		   intensity[i] = rgb_to_hex((0, 4095 - 0.8*(math.ceil(router_normalized[i] * 4095)), 0))
               f = figure(figsize=(2.5, 8),facecolor='w')
               gca().set_visible(False)
	       if ((family_selected == 'link') | (family_selected == 'vc')):
                 my_cmap = cm.get_cmap('BlueRed')
	       else:
                 my_cmap = cm.get_cmap('Greenblack')
               norm = matplotlib.colors.Normalize(min_traffic, max_traffic)
               cmmapable = cm.ScalarMappable(norm, my_cmap)
               cmmapable.set_array(range((int)(min_traffic), (int)(max_traffic)))
               cb = colorbar(cmmapable)
               if (family_selected == "link"):
	         cb.set_label('%s'%option_selected,fontsize=14,labelpad=-70)
               else:
                 cb.set_label('link traffic',fontsize=14,labelpad=-70)
	       cb.ax.yaxis.tick_left()
               for l in cb.ax.yaxis.get_ticklabels():
                 l.set_size('large')
               dataplot = FigureCanvasTkAgg(f,master=frame1)
	       dataplot.show()
	       dataplot.get_tk_widget().grid(row=0,column=0,sticky=tk.E)

## Displaying router values
		           
	       canvas.itemconfig(epoch_label, text = 'clock = %d'%elem)

               for i in range(nodes):
	          row = (int)(math.floor(i / xnodes));
		  column = i%xnodes;
	          canvas.itemconfig(router_id[row][column],fill = intensity[i])

      if iter == 0:
	 canvas.delete(epoch_label)
         for i in range(nodes):
	    row = (int)(math.floor(i / xnodes))
	    column = i%xnodes
            canvas.tag_unbind (router_id[row][column],"<Shift-ButtonRelease>")
            for j in range(4):
               if link_id[i][j] !=0:
	          if family_selected == 'link':
	            if family_selected == 'vc':
                      canvas.tag_unbind (link_id[i][j],"<Double-Button-1>")
                    canvas.tag_unbind (link_id[i][j],"<Shift-ButtonRelease>")
      for i in range(nodes):
	 row = (int)(math.floor(i / xnodes))
	 column = i%xnodes
         canvas.tag_bind (router_id[row][column],"<Shift-ButtonRelease>",lambda event, arg=(curr_timestamp,packet_info_txt,packet_op,option_prop_selected,family_selected,epoch_skip_steps,option_selected):display_values(event,arg))
         for j in range(4):
            if link_id[i][j] != 0:
	      if family_selected == 'link':
                if family_selected == 'vc':
	          canvas.tag_bind (link_id[i][j],"<Double-Button-1>",lambda event, arg=(curr_timestamp,packet_info_txt,packet_op,option_prop_selected,family_selected,epoch_skip_steps,option_selected):display_values(event,arg))
                canvas.tag_bind (link_id[i][j],"<Shift-ButtonRelease>",lambda event, arg=(curr_timestamp,packet_info_txt,packet_op,option_prop_selected,family_selected,epoch_skip_steps,option_selected):display_values(event,arg))


def interval_mode(epoch_start_usr_def,option_prop_selected,family_selected,epoch_skip_steps,option_selected,epoch_jump_usr_def,packet_op):
   epoch_asc = sorted(epoch,key=int)
   global nxt_timestamp
   epoch_label = canvas.create_text(x_epoch_label,y_epoch_label,anchor=tk.CENTER)
   packet_info_txt = canvas.create_text(x_info_label,y_info_label)
   nxt_timestamp = epoch_start_usr_def
      
   trafficexitbutton = tk.Button(frame2, text="exit", command=exit_sys)
   trafficexitbutton.grid(row=0,column=1)
   trafficnextbutton = tk.Button(frame2, text="next>>", repeatinterval=1, repeatdelay=1000, command=lambda: trafficnext(ts=nxt_timestamp,epoch_asc=epoch_asc,sign=1,option_prop_selected=option_prop_selected,family_selected=family_selected,epoch_skip_steps=epoch_skip_steps,option_selected=option_selected,epoch_jump_usr_def=epoch_jump_usr_def,packet_op=packet_op,epoch_label=epoch_label,packet_info_txt=packet_info_txt))
   trafficnextbutton.grid(row=0,column=2)
   trafficprevbutton = tk.Button(frame2, text="<<prev", repeatinterval=1, repeatdelay=1000, command=lambda: trafficnext(ts=prev_timestamp,epoch_asc=epoch_asc,sign=-1,option_prop_selected=option_prop_selected,family_selected=family_selected,epoch_skip_steps=epoch_skip_steps,option_selected=option_selected,epoch_jump_usr_def=epoch_jump_usr_def,packet_op=packet_op,epoch_label=epoch_label,packet_info_txt=packet_info_txt))
   
   trafficprevbutton.grid(row=0,column=0)
   trafficrestartbutton = tk.Button(frame2, text="enter options again", command=restart)
   trafficrestartbutton.grid(row=1,column=1)
   frame1.mainloop()
   canvas.delete(epoch_label)
   canvas.delete(packet_info_txt)
   trafficexitbutton.grid_remove()
   trafficnextbutton.grid_remove()
   trafficprevbutton.grid_remove()
   trafficrestartbutton.grid_remove()


