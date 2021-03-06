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
  
def select_mode():  
  if  (len(event_epoch_list) > 0) & (len(epoch_asc) > 0) :
    Rad_op_3 = tk.Radiobutton(frame1,text="Event based parsing",variable=packet_trace,value=2)
    Rad_op_3.grid(row=2,column=0)
    Rad_op_2 = tk.Radiobutton(frame1,text="Display traffic",variable=packet_trace,value=1)
    Rad_op_2.grid(row=1,column=0)
    optionenterbutton = tk.Button(frame1, text = "Enter", command = exit_gui)
    optionenterbutton.grid(row=3,column=0)
    optionexitbutton = tk.Button(frame1, text = "Exit", command = exit_sys)
    optionexitbutton.grid(row=4,column=0)
    frame1.mainloop()
    packet_op = packet_trace.get()
    Rad_op_2.grid_remove()
    Rad_op_3.grid_remove()
    optionenterbutton.grid_remove()
    optionexitbutton.grid_remove()
  elif (len(event_epoch_list) > 0):
    packet_op = 2;
  elif (len(epoch_asc) > 0):
    packet_op = 1;
  else:
    print "Error: Interval/event info not provided"
    exit_sys()
  
     
  
  if packet_op != 2:
    par_opt_sel = tk.OptionMenu(frame1,option_sel,*parameter_options)
    option_sel.set("%s"%parameter_options[0])
  
    option_prop_menu = tk.OptionMenu(frame1,op_prop_sel,*option_prop)
    op_prop_sel.set("%s"%option_prop[0])
    option_prop_menu.grid(row=2,column = 2)
  
    par_opt_sel.grid(row=2,column=1)
    paroptlabel = tk.Label(frame1, text='Choose parameter to \n plot')
    paroptlabel.grid(row=1,column=1)
    parproplabel = tk.Label(frame1, text='Choose property of \n parameter')
    parproplabel.grid(row=1,column=2)
    optionenterbutton = tk.Button(frame1, text = "Enter", command = exit_gui)
    optionenterbutton.grid(row=3,column=2)
    optionexitbutton = tk.Button(frame1, text = "Exit", command = exit_sys)
    optionexitbutton.grid(row=3,column=3)
    epochstartlabel = tk.Label(frame1, text='Epoch start \n (epoch size = %d cycles\n execution time = %d cycles)'%(epoch_asc[0],epoch_asc[len(epoch_asc)-1]))
    epochstartlabel.grid(row=1,column=3)
    epochstartentry = tk.Entry(frame1, bd = 3)
    epochstartentry.grid(row=2,column=3)
    epochsizelabel = tk.Label(frame1, text='Epoch step size \n (min step width = %d)'%epoch_smallest_step)
    epochsizelabel.grid(row=1,column=4)
    epochsizeentry = tk.Entry(frame1, bd = 3)
    epochsizeentry.grid(row=2,column=4)
    frame1.mainloop()
  
    option_selected = option_sel.get()
  
    option_prop_selected = op_prop_sel.get()
    try:
      epoch_jump_usr_def = epoch_smallest_step * (int)(math.floor(eval(epochsizeentry.get())))
    except:
      epoch_jump_usr_def = epoch_smallest_step
    try:
      epoch_start_usr_def = epoch_asc[0] * (int)(math.floor(eval(epochstartentry.get())))
    except:
      epoch_start_usr_def = epoch_asc[0]
  
    par_opt_sel.grid_remove()
    paroptlabel.grid_remove()
    option_prop_menu.grid_remove()
    paroptlabel.grid_remove()
    parproplabel.grid_remove()
    optionenterbutton.grid_remove()
    optionexitbutton.grid_remove()
    epochsizeentry.grid_remove()
    epochsizelabel.grid_remove()
    epochstartentry.grid_remove()
    epochstartlabel.grid_remove()
  
    family_selected = get_family(nodes,num_vcs,eval(config.get('clock = %d'%epoch_asc[0],option_selected)))
    epoch_skip_steps = (int)(math.floor(epoch_jump_usr_def/(epoch_asc[1] - epoch_asc[0])))
  
  else:
    evententerbutton = tk.Button(frame1, text = "Enter", command = exit_gui)
    evententerbutton.grid(row=3,column=0)
    eventexitbutton = tk.Button(frame1, text = "Exit", command = exit_sys)
    eventexitbutton.grid(row=3,column=1)
    epochstartlabel = tk.Label(frame1, text='Epoch start (min = %d, max = %d)'%(event_epoch_asc[0],event_epoch_asc[len(event_epoch_asc)-1]))
    epochstartlabel.grid(row=1,column=0)
    event_start_ip = tk.Entry(frame1, bd = 3)
    event_start_ip.grid(row=2,column = 0)
    frame1.mainloop()
  
    for items in event_epoch_asc:
      if (eval(event_start_ip.get()) <= items):
        event_start_usr_def = items 
        break;
      else:
        event_start_usr_def = event_epoch_asc[len(event_epoch_asc)-1]
    evententerbutton.grid_remove()
    eventexitbutton.grid_remove()
    epochstartlabel.grid_remove()
    event_start_ip.grid_remove()
