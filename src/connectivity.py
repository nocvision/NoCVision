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

import re
import math


def connectivity(topology='mesh',k=3):

   xnodes = k
   nodes = k * k
   links = [[-1 for i in range(4)] for i in range(nodes)]
   north = 0
   west = 0
   south = 0
   east = 0
   value_regex = re.compile('^(\D*)(:)(.*)\n$')

   for i in range(nodes):
      for j in range(4):
         row = (int)(math.floor(i/xnodes))
         col = i%xnodes
         if topology == 'mesh':
            if j == 0:
	       if row != 0:
	          links[i][j] = i - xnodes
	       else:
	          links[i][j] = -1
	    elif j == 1:
	       if col != xnodes-1:
	          links[i][j] = i + 1
	       else:
	          links[i][j] = -1
            elif j == 2:
	       if row != xnodes-1:
	          links[i][j] = i + xnodes
	       else:
	          links[i][j] = -1
	    else:
	       if col != 0:
	          links[i][j] = i - 1
	       else:
	          links[i][j] = -1
         elif topology == 'torus':
            if j == 0:
	       if row != 0:
	          links[i][j] = i - xnodes
	       else:
	          links[i][j] = nodes - xnodes + i
	    elif j == 1:
	       if col != xnodes-1:
	          links[i][j] = i + 1
	       else:
	          links[i][j] = i - xnodes + 1
            elif j == 2:
	       if row != xnodes-1:
	          links[i][j] = i + xnodes
	       else:
	          links[i][j] = i%xnodes
	    else:
	       if col != 0:
	          links[i][j] = i - 1
	       else:
	          links[i][j] = i + xnodes - 1
         elif topology == 'psuedo_heroic':
            if j == 0:
	       if row != 0:
	          links[i][j] = i - xnodes + 1
	       else:
	          links[i][j] = (int)(math.floor(xnodes/2)) + i
	    elif j == 1:
	       if col != xnodes-1:
	          links[i][j] = i + xnodes + 1
	       else:
	          links[i][j] = i + xnodes*2 
            elif j == 2:
	       if row != xnodes-1:
	          links[i][j] = i + xnodes - 1
	       else:
	          links[i][j] = i - (int)(math.floor(xnodes/2))
	    else:
	       if col != 0:
	          links[i][j] = i - xnodes - 1
	       else:
	          links[i][j] = i - xnodes*2
         elif topology == 'irregular':
            with open(conf_file_name,'r') as init_file:
               for line in init_file:
                  if 'connectivity:' in line:
                     link_temp = eval(value_regex.search(line).groups()[2])
		     for i in range(nodes):
		      row_src = (int)(math.floor(i/xnodes))
		      col_src = (int)(i%xnodes)
		      for k in range(4):
		        for j in range(4):
			   dest = link_temp[i][j]
			   row_dest = (int)(math.floor(dest/xnodes))
			   col_dest = (int)(dest%xnodes)
			   if (row_dest == row_src-1):
			      links[i][0] = link_temp[i][j]
			   elif(row_dest == row_src+1):
			      links[i][2] = link_temp[i][j]
			   elif (col_dest == col_src-1):
			      links[i][3] = link_temp[i][j]
			   elif (col_dest == col_src + 1):
			      links[i][1] = link_temp[i][j]

			   elif ((col_src == 0) & (col_dest == xnodes-1)):
			      links[i][3] = link_temp[i][j]
			   elif ((col_src == xnodes-1) & (col_dest == 0)):
			      links[i][1] = link_temp[i][j]
			   elif ((row_src == 0) & (row_dest == xnodes-1)):
			      links[i][0] = link_temp[i][j]
			   elif ((row_src == xnodes-1) & (row_dest == 0)):
			      links[i][2] = link_temp[i][j]

			   elif ((row_src == row_dest)):
			      if links[i][0] == -1:
			         links[i][0] = link_temp[i][j]
		              else:
			         links[i][2] = link_temp[i][j]
			   elif ((col_src == col_dest)):
			      if links[i][3] == -1:
			         links[i][3] = link_temp[i][j]
			      else:
			         links[i][1] = link_temp[i][j]
			   
		     return links

	       print "connectivity parameter not found for irregular topology"
	       exit_sys()
         elif topology == 'irregular1':
            with open(conf_file_name,'r') as init_file:
               for line in init_file:
                  if 'connectivity:' in line:
                     links = eval(value_regex.search(line).groups()[2])
		     return links

	       print "connectivity parameter not found for irregular topology"
	       exit_sys()

	    
         else:
	    print "%s Topology unknown"%topology
	    exit_sys()

   return links
