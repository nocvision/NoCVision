from __future__ import division
import Tkinter as tk
import math
from nocvision_config import *

def draw_links(src_node,direction,col="black"):
   dest_node = link[src_node][direction]

   row_dest = (int)(math.floor(dest_node/xnodes))
   col_dest = dest_node%xnodes

   row_src = (int)(math.floor(src_node/xnodes))
   col_src = src_node%xnodes
   north_edge_node_src = (row_src == 0)
   east_edge_node_src = (col_src == xnodes-1)
   south_edge_node_src = (row_src == xnodes-1)
   west_edge_node_src = (col_src == 0)

   north_edge_node_dest = (row_dest == 0)
   east_edge_node_dest = (col_dest == xnodes-1)
   south_edge_node_dest = (row_dest == xnodes-1)
   west_edge_node_dest = (col_dest == 0)

   x_centre_node_src = 300 + col_src*(node_width+node_spacing) + (node_width/2)
   y_centre_node_src = 200 + row_src*(node_width+node_spacing) + (node_width/2)
   x_centre_node_dest = 300 + col_dest*(node_width+node_spacing) + (node_width/2)
   y_centre_node_dest = 200 + row_dest*(node_width+node_spacing) + (node_width/2)

   if direction == 0:
      x_src = x_centre_node_src-10
      y_src = y_centre_node_src - (node_width/2)

      if ((row_src == row_dest + 1) & (col_src == col_dest)):
         x_dest = x_centre_node_dest - 10
         y_dest = y_centre_node_dest + (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif (north_edge_node_src & south_edge_node_dest):
         x_dest = x_centre_node_dest - 10
         y_dest = y_centre_node_dest + (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src - (node_spacing/2) - 10, x_src - (node_spacing/2), y_src - (node_spacing/2) - 10, x_dest - (node_spacing/2),y_dest + (node_spacing/2) + 10, x_dest,y_dest + (node_spacing/2) + 10, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif (north_edge_node_src & north_edge_node_dest):
         x_dest = x_centre_node_dest + 10
         y_dest = y_centre_node_dest - (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src - (node_spacing/2) - 10 - 8*col_src, x_dest,y_dest - (node_spacing/2) - 10 - 8*col_src, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif ((row_src == row_dest + 1) & (col_src == col_dest + 1)):
         x_src = x_centre_node_src - (node_width/(2*math.sqrt(2))) + 5
         y_src = y_centre_node_src - (node_width/(2*math.sqrt(2))) - 5
         x_dest = x_centre_node_dest + (node_width/(2*math.sqrt(2))) + 5
         y_dest = y_centre_node_dest + (node_width/(2*math.sqrt(2))) - 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif ((row_src == row_dest + 1) & (col_src == col_dest - 1)):
         x_src = x_centre_node_src + (node_width/(2*math.sqrt(2))) + 5
         y_src = y_centre_node_src - (node_width/(2*math.sqrt(2))) + 5
         x_dest = x_centre_node_dest - (node_width/(2*math.sqrt(2))) + 5
         y_dest = y_centre_node_dest + (node_width/(2*math.sqrt(2))) + 5 
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif (row_src == row_dest) & (col_dest > col_src):
         x_src = x_centre_node_src-10
         y_src = y_centre_node_src - (node_width/2)
         x_dest = x_centre_node_dest - 10
         y_dest = y_centre_node_dest - (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src - (node_spacing/2) - 5 - 2*col_src, x_dest,y_dest - (node_spacing/2) - 5 - 2*col_src, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif (row_src == row_dest) & (col_dest < col_src):
         x_src = x_centre_node_src+10
         y_src = y_centre_node_src - (node_width/2)
         x_dest = x_centre_node_dest + 10
         y_dest = y_centre_node_dest - (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src - (node_spacing/2) + 5 - 2*col_src, x_dest,y_dest - (node_spacing/2) + 5 - 2*col_src, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))

   elif direction == 1:
      x_src = x_centre_node_src + (node_width/2)
      y_src = y_centre_node_src - 10
      if ((row_src == row_dest) & (col_dest == col_src+1)):
         x_dest = x_centre_node_dest - (node_width/2)
         y_dest = y_centre_node_dest - 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
   
      elif (west_edge_node_src & east_edge_node_dest):
         x_dest = x_centre_node_dest - (node_width/2)
         y_dest = y_centre_node_dest - 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src + (node_spacing/2) + 10, y_src,x_src + (node_spacing/2) + 10, y_src - (node_spacing/2), x_dest - (node_spacing/2) - 10,y_dest - (node_spacing/2), x_dest  - (node_spacing/2) - 10,y_dest, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif (west_edge_node_src & west_edge_node_dest):
         x_dest = x_centre_node_dest + (node_width/2)
         y_dest = y_centre_node_dest + 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src + (node_spacing/2) + 10 + 8*row_src, y_src, x_dest  + (node_spacing/2) + 10 + 8*row_src,y_dest, x_dest,y_dest,arrow=tk.LAST,fill = col, dash = (5,3), width = 4)
      elif ((row_src == row_dest + 1) & (col_src == col_dest - 1)):
         x_src = x_centre_node_src + (node_width/(2*math.sqrt(2))) + 5 
         y_src = y_centre_node_src - (node_width/(2*math.sqrt(2))) + 5
         x_dest = x_centre_node_dest - (node_width/(2*math.sqrt(2))) + 5
         y_dest = y_centre_node_dest + (node_width/(2*math.sqrt(2))) + 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif ((row_src == row_dest - 1) & (col_src == col_dest - 1)):
         x_src = x_centre_node_src + (node_width/(2*math.sqrt(2))) - 5
         y_src = y_centre_node_src + (node_width/(2*math.sqrt(2))) + 5
         x_dest = x_centre_node_dest - (node_width/(2*math.sqrt(2))) - 5 
         y_dest = y_centre_node_dest - (node_width/(2*math.sqrt(2))) + 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif (col_src == col_dest) & (row_dest > row_src):
         x_src = x_centre_node_src + (node_width/2)
         y_src = y_centre_node_src + 10
         x_dest = x_centre_node_dest + (node_width/2)
         y_dest = y_centre_node_dest + 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src + (node_spacing/2)+5+2*row_src, y_src, x_dest+(node_spacing/2)+5+2*row_src, y_dest, x_dest,y_dest,arrow=tk.LAST, fill = col, width = 4, dash = (5,3))
      elif (col_src == col_dest) & (row_dest < row_src):
         x_dest = x_centre_node_dest + (node_width/2)
         y_dest = y_centre_node_dest - 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src + (node_spacing/2)+5+2*row_src, y_src, x_dest+(node_spacing/2)+5+2*row_src, y_dest, x_dest,y_dest,arrow=tk.LAST, fill = col, width = 4, dash = (5,3))



   elif direction == 2:
      x_src = x_centre_node_src + 10
      y_src = y_centre_node_src + (node_width/2)

      if ((row_src == row_dest - 1) & (col_src == col_dest)):
         x_dest = x_centre_node_dest + 10
         y_dest = y_centre_node_dest  - (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)

      elif (south_edge_node_src & north_edge_node_dest):
         x_dest = x_centre_node_dest + 10
         y_dest = y_centre_node_dest  - (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src + (node_spacing/2), x_src - (node_spacing/2), y_src + (node_spacing/2), x_dest - (node_spacing/2),y_dest - (node_spacing/2), x_dest,y_dest - (node_spacing/2), x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif (south_edge_node_src & south_edge_node_dest):
         x_dest = x_centre_node_dest - 10
         y_dest = y_centre_node_dest  + (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src + (node_spacing/2) + 8*col_src, x_dest, y_dest + (node_spacing/2) + 8*col_src, x_dest,y_dest,arrow=tk.LAST,fill = col, dash = (5,3), width = 4)
      elif ((row_src == row_dest - 1) & (col_src == col_dest - 1)):
         x_src = x_centre_node_src + (node_width/(2*math.sqrt(2))) - 5
         y_src = y_centre_node_src + (node_width/(2*math.sqrt(2))) + 5
         x_dest = x_centre_node_dest - (node_width/(2*math.sqrt(2))) - 5
         y_dest = y_centre_node_dest - (node_width/(2*math.sqrt(2))) + 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif ((row_src == row_dest - 1) & (col_src == col_dest + 1)):
         x_src = x_centre_node_src - (node_width/(2*math.sqrt(2))) - 5
         y_src = y_centre_node_src + (node_width/(2*math.sqrt(2))) - 5
         x_dest = x_centre_node_dest + (node_width/(2*math.sqrt(2))) - 5
         y_dest = y_centre_node_dest - (node_width/(2*math.sqrt(2))) - 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif (row_src == row_dest) & (col_dest > col_src):
         x_dest = x_centre_node_dest + 10
         y_dest = y_centre_node_dest + (node_width/2)
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src + (node_spacing/2) + 10 + 8*col_src, x_dest,y_dest + (node_spacing/2) + 10 + 8*col_src, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif (col_src == col_dest) & (row_dest < row_src):
         x_dest = x_centre_node_dest + (node_width/2)
         y_dest = y_centre_node_dest - 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src, y_src + (node_spacing/2) + 10 - 8*col_src, x_dest,y_dest + (node_spacing/2) + 10 - 8*col_src, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))



   else:
      x_src = x_centre_node_src - (node_width/2)
      y_src = y_centre_node_src + 10
      if ((row_src == row_dest) & (col_dest == col_src-1)):
         x_dest = x_centre_node_dest + (node_width/2)
         y_dest = y_centre_node_dest + 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif (east_edge_node_src & west_edge_node_dest):
         x_dest = x_centre_node_dest + (node_width/2)
         y_dest = y_centre_node_dest + 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src - (node_spacing/2), y_src,x_src - (node_spacing/2), y_src - (node_spacing/2), x_dest + (node_spacing/2),y_dest - (node_spacing/2), x_dest  + (node_spacing/2),y_dest, x_dest,y_dest, width = 4, arrow=tk.LAST, fill = col, dash = (5,3))
      elif (east_edge_node_src & east_edge_node_dest):
         if (src_node == 7):
	    print "entered"
         x_dest = x_centre_node_dest - (node_width/2)
         y_dest = y_centre_node_dest - 10
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_src - (node_spacing/2) - 8*row_src, y_src, x_dest - (node_spacing/2) - 8*row_src, y_dest, x_dest,y_dest,arrow=tk.LAST, fill = col, dash = (5,3), width = 4)
      elif ((row_src == row_dest - 1) & (col_src == col_dest - 1)):
         x_src = x_centre_node_src + (node_width/(2*math.sqrt(2))) - 5
         y_src = y_centre_node_src + (node_width/(2*math.sqrt(2))) - 5
         x_dest = x_centre_node_dest - (node_width/(2*math.sqrt(2))) - 5
         y_dest = y_centre_node_dest - (node_width/(2*math.sqrt(2))) - 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
      elif ((row_src == row_dest + 1) & (col_src == col_dest + 1)):
         x_src = x_centre_node_src - (node_width/(2*math.sqrt(2))) + 5
         y_src = y_centre_node_src - (node_width/(2*math.sqrt(2))) - 5 
         x_dest = x_centre_node_dest + (node_width/(2*math.sqrt(2))) + 5
         y_dest = y_centre_node_dest + (node_width/(2*math.sqrt(2))) - 5
         link_id[src_node][direction] = canvas.create_line(x_src,y_src,x_dest,y_dest,arrow=tk.LAST, fill = col, width = 8)
   return link_id[src_node][direction]

