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
