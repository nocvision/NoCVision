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
