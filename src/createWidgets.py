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

from nocvision_config import *
from draw_links import *

def createWidgets():
      for i in range(xnodes):
         for j in range(xnodes):
            router_id[i][j] = canvas.create_oval(300 + (node_width+node_spacing)*j, 200 + (node_width+node_spacing)*i, 300+node_width + (node_width+node_spacing)*j, 200+node_width + (node_width+node_spacing)*i, fill = 'white')
	    x_centre = (int)(math.floor(((300 + (node_width+node_spacing)*j) + (300+node_width + (node_width+node_spacing)*j))/2))
	    y_centre = (int)(math.floor(((200 + (node_width+node_spacing)*i) + (200+node_width + (node_width+node_spacing)*i))/2))
	    router_id_txt[i][j] = canvas.create_text(x_centre,y_centre,text='%d'%(i*xnodes + j),anchor=tk.CENTER)
      for i in range(nodes):
         for j in range(4):
	    if (link[i][j] >= 0) & (link[i][j] <= (nodes-1)):
               link_id[i][j] = draw_links(i , j)
	    else:
	       link_id[i][j] = 0
      canvas.grid(column=1,row=0)
      hbar.grid(row=1,column=1,sticky='ew')
      vbar.grid(row=0,column=2,sticky='ns')
