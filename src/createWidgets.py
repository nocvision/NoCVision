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
