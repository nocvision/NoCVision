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

def display_values(event,args):
   link_clicked_dir = -2
   curr_timestamp = args[0]
   packet_info_txt = args[1]
   packet_op = args[2]
   option_prop_selected = args[3]
   family_selected = args[4]
   epoch_skip_steps = args[5]
   option_selected = args[6]
   packet = [[0 for i in range(4)] for i in range(nodes)]
   no_of_loops = 0
   router_info_acc = [0 for i in range(nodes)]
   vc_param_retr = [[[0 for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
   
   if packet_op !=2:
      if  (option_prop_selected == 'accumulate') | (option_prop_selected == 'average') | (option_prop_selected == 'maximum'):
         packet_retr = [[0 for l in range(4)] for l in range(nodes)]
         router_retr = [0.0 for l in range(nodes)]
         temp_var = 0
         vc_parameters = [[[0 for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
      elif option_prop_selected == 'minimum':
         packet_retr = [[(float('Infinity')) for l in range(4)] for l in range(nodes)]
         router_retr = [float('Infinity') for l in range(nodes)]
         temp_var = float('inf')
         vc_parameters = [[[float('Infinity') for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
   else:
      vc_parameters = [[[0 for i in range(num_vcs)] for i in range(4)] for i in range(nodes)]
    
   link_clicked_id =  event.widget.find_closest(event.x, event.y)[0]
   for i in range(nodes):
      for j in range(4):
         row = (int)(math.floor(i/xnodes))
	 column = i%xnodes
         if link_id[i][j] == link_clicked_id:
            link_clicked_router = i
            link_clicked_dir = j
	    break
	 elif router_id[row][column] == link_clicked_id:
	    link_clicked_router = i
	    link_clicked_dir = -1
	    break
   if packet_op !=2:
      if family_selected == 'vc':
            no_of_loops = 0
            for i in range(epoch_skip_steps):
               try:
                  section = 'clock = %d' %(curr_timestamp-(epoch_smallest_step*i))
                  vc_param_retr = eval(config.get(section,option_selected))
                  for a in range(nodes):
                     for b in range(4):
           	        temp_var = 0
           	        for c in range(num_vcs):
           	           temp_var = temp_var + vc_param_retr[a][b][c]

           	           if (option_prop_selected == 'accumulate') | (option_prop_selected == 'average'):
           	              vc_parameters[a][b][c] += vc_param_retr[a][b][c]
           	           elif option_prop_selected == 'minimum':
           	              if vc_parameters[a][b][c] > vc_param_retr[a][b][c]:
           	                 vc_parameters[a][b][c] = vc_param_retr[a][b][c]
           	           else:
           	              if  vc_parameters[a][b][c] < vc_param_retr[a][b][c]:
           	                 vc_parameters[a][b][c] = vc_param_retr[a][b][c]

                  no_of_loops += 1
               except ConfigParser.NoSectionError:
                  vc_parameters = vc_parameters 
                  
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
           	        if packet_retr[a][b] < vc_parameters[a][b][c]:
           	           packet_retr[a][b] = vc_parameters[a][b][c]

            if (option_prop_selected == 'average'):
               for a in range(nodes):
                  for b in range(4):
                     packet[a][b] = packet_retr[a][b]/num_vcs
            else:
               packet = packet_retr

             
      elif family_selected == 'link':
         if display == 0:
            for i in range(epoch_skip_steps):
               try:
                  section = 'clock = %d' %(curr_timestamp-(epoch_smallest_step*i))
                  for a in range(nodes):
                     for b in range(4):
                        if (option_prop_selected == 'accumulate') | (option_prop_selected == 'average'):
      		         packet_retr[a][b] += (eval(config.get(section,option_selected)))[a][b]
                        elif (option_prop_selected == 'minimum'):
           	         if packet_retr[a][b] > (eval(config.get(section,option_selected)))[a][b]:
           		    packet_retr[a][b] = (eval(config.get(section,option_selected)))[a][b]
                        else:
           	         if packet_retr[a][b] < (eval(config.get(section,option_selected)))[a][b]:
           		    packet_retr[a][b] = (eval(config.get(section,option_selected)))[a][b]
                  no_of_loops+=1
               except:
                  packet_retr = packet_retr 

            if option_prop_selected == 'average':
               for a in range(nodes):
                  for b in range(4):
                     packet[a][b] = packet_retr[a][b]/no_of_loops
            else:
               packet = packet_retr

         else:
            section = 'clock = %d' %(curr_timestamp)
            packet = eval(config.get(section,option_selected))


      if (family_selected == 'vc') | (family_selected == 'link'):
         if (option_prop_selected == 'accumulate') :
            for a in range(nodes):
               try:
                  if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <=(nodes-1)):
                     router_retr[a] += packet[a-xnodes][2]
               except:
                  router_retr[a] = router_retr[a]
               try:
                  if (link[a+xnodes][0] >=0) &  (link[a+xnodes][0] <=(nodes-1)):
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
                  if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <= (nodes-1)):
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
                  if (link[a+1][3] >=0) & (link[a+1][3] <=(nodes-1)):
          	     if router_retr[a] > packet[a+1][3]:
                        router_retr[a] = packet[a+1][3]
               except:
                  router_retr[a] = router_retr[a]             
            router_info_acc = router_retr
         
         elif (option_prop_selected == 'maximum'):
            for a in range(nodes):
               try:
                  if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <= (nodes-1)):
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
                  if (link[a-xnodes][2] >=0) & (link[a-xnodes][2] <=(nodes-1)):
                     router_retr[a] += packet[a-xnodes][2]
          	     no_of_loops+=1
               except:
                  router_retr[a] = router_retr[a]
               try:
                  if (link[a+xnodes][0] >=0) & (link[a+xnodes][0] <=(nodes-1)):
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
                  if (link[a+1][3] >=0) & (link[a+1][3] <=(nodes-1)):
                     router_retr[a] += packet[a+1][3]
          	     no_of_loops+=1
               except:
                  router_retr[a] = router_retr[a]
         
               router_info_acc[a] = router_retr[a]/no_of_loops
      else: 
               no_of_loops = 0
               for i in range(epoch_skip_steps):
                  try:
                     section = 'clock = %d' %(curr_timestamp-(epoch_smallest_step*i))
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

   else:
      section = 'clock = %d' %curr_timestamp
      packet = eval(eventConfig.get(section,'packet'))
      vc_parameters = eval(eventConfig.get(section,'vc_packets'))



   if eval(event.type) == 4:
      canvas_vc.delete(tk.ALL)

      packets_in_vc = vc_parameters[link_clicked_router][link_clicked_dir]
      canvas.itemconfig(packet_info_txt,text="")

      direction = ''
      max_vc_packet = 0
      vc_rect_ids = [0 for x in xrange(num_vcs)]
      vc_txt_ids = [0 for x in xrange(num_vcs)]
      vc_packet_ids = [0 for x in xrange(num_vcs)]
      vc_label = 0
      for i in range(num_vcs):
         if packets_in_vc[i] > max_vc_packet:
            max_vc_packet = packets_in_vc[i]
      min_vc_packet = max_vc_packet
      for i in range(num_vcs):
         if packets_in_vc[i] < min_vc_packet:
            min_vc_packet = packets_in_vc[i]

      packet_normalized = [0.0 for x in range(num_vcs)]
      intensity = ['#000fff000' for x in range(num_vcs)]
      for i in range(num_vcs):
         if ((max_vc_packet-min_vc_packet)!=0):
            packet_normalized[i] = (packets_in_vc[i]-min_vc_packet)/(max_vc_packet-min_vc_packet)
            intensity[i] = rgb_to_hex(((0.8*(math.ceil(packet_normalized[i] * 4095))),0,(4095 -(math.ceil(packet_normalized[i] * 4095)))))
         else:
            packet_normalized[i] = 0.0
            intensity[i] = rgb_to_hex(((0.8*(math.ceil(packet_normalized[i] * 4095))),0,(4095 -(math.ceil(packet_normalized[i] * 4095)))))

      canvas_vc.grid(row = 0,column = 4)
      x0_vc = 200
      y0_vc = 200
      x1_vc = 320
      y1_vc = 200
      for i in range(num_vcs):
         y0_vc = y1_vc
         y1_vc = y0_vc + 20
         if display == 0:
            vc_rect_ids[i] = canvas_vc.create_rectangle(x0_vc,y0_vc,x1_vc,y1_vc,fill=intensity[i])
    
            a = np.array([[0,1]])
            f = figure(figsize=(2.5, 8),facecolor='w')
            img = imshow(a, cmap="Blues")
            gca().set_visible(False)
            my_cmap = cm.get_cmap('Redblack')
            norm = matplotlib.colors.Normalize(min_vc_packet, max_vc_packet)
            cmmapable = cm.ScalarMappable(norm, my_cmap)
            cmmapable.set_array(range((int)(min_vc_packet), (int)(max_vc_packet)))
            cb = colorbar(cmmapable)
            cb.set_label('%s'%option_selected,fontsize=14,labelpad=-70)
	    cb.ax.yaxis.tick_left()
            for l in cb.ax.yaxis.get_ticklabels():
               l.set_size('large')
            dataplot1 = FigureCanvasTkAgg(f,master=frame3)
	    dataplot1.show()
            frame3.grid(row=0,column=3)
	    dataplot1.get_tk_widget().grid(row=0,column=2,sticky=tk.E)
            
         else:
            vc_rect_ids[i] = canvas_vc.create_rectangle(x0_vc,y0_vc,x1_vc,y1_vc)
            vc_packet_ids[i] = canvas_vc.create_text(x0_vc + 50,y0_vc + 10, text = '%d'%packets_in_vc[i])
         vc_txt_ids[i] = canvas_vc.create_text(x0_vc-30,(y0_vc+y1_vc)/2,text='vc = %d'%i)
    
      if link_clicked_dir == 0:
         direction = 'North'
      elif link_clicked_dir == 1:
         direction = 'East'
      elif link_clicked_dir == 2:
         direction = 'South'
      else:
         direction = 'West'
      vc_label = canvas_vc.create_text(260,160,text='router = %d, direction = %s'%(link_clicked_router,direction))

   if eval(event.type) == 5:
      if packet_op ==1:
         if (family_selected == "vc") | (family_selected == "link"):
            if link_clicked_dir == -1:
                  canvas.itemconfig(packet_info_txt,text="Router inflow traffic = %f"%router_info_acc[link_clicked_router])
            elif link_clicked_dir >= 0:
               if packet_op == 1:
                  canvas.itemconfig(packet_info_txt,text="Packet traffic = %f"%packet[link_clicked_router][link_clicked_dir])
               else:
                  canvas.itemconfig(packet_info_txt,text="Packet id = %f"%packet[link_clicked_router][link_clicked_dir])
         else:
               canvas.itemconfig(packet_info_txt,text="%s = %f"%(option_selected, router_info_acc[link_clicked_router]))
         
      else:
           canvas.itemconfig(packet_info_txt,text="Packet id = %f"%packet[link_clicked_router][link_clicked_dir])
