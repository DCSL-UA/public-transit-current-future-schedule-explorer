import json, urllib
import googlemaps
import time
from datetime import datetime
import sys
import datetime
x=1
gmaps = ""
global directions11
directions11 = ""
#Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)
Types_of_Bus = ["BUS","INTERCITY_BUS","TROLLEYBUS"]
Types_of_Rail = ["RAIL","METRO_RAIL","MONORAIL","COMMUTER_TRAIN","HEAVY_RAIL","HIGH_SPEED_TRAIN"]
Types_of_Tram = ["TRAM"]
Types_of_Subway = ["SUBWAY"]
def short_or_full(directions):
  if "short_name" in directions.keys():
    return directions['short_name']
  else:
    return directions['name']
def leaving(time_to_leave):
  return (time.time()+ (int(time_to_leave)*60))

def google_leaving(time_to_leave):
    if (time_to_leave == "0"):
      return "now"
    else:
      return (int(time.time())+ (int(time_to_leave)*60))

def print_breakdown_types(total_time,total_dist,bus,sub,train,tram,walk,wait,output,query_time):
  output.write(",")
  output.write(str(bus[0]))
  output.write(",")
  output.write(str(float(100* (float(bus[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(sub[0]))
  output.write(",")
  output.write(str(float(100* (float(sub[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(train[0]))
  output.write(",")
  output.write(str(float(100* (float(train[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(tram[0]))
  output.write(",")
  output.write(str(float(100* (float(tram[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(walk[0]))
  output.write(",")
  output.write(str(float(100* (float(walk[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(wait[0]))
  output.write(",")
  output.write(str(float(100* (float(wait[0])/float(total_time[0])))))

def get_waittime(step,query_time,timelist,wait_total):
  if (step['transit_details']['departure_time']['value'] != (timelist[0] + query_time)):
   # print "Transit arrives: " + str(step['transit_details']['arrival_time']['value'])
   # print "adding: " + str(step['transit_details']['departure_time']['value'] - (timelist[0] + query_time))
    return step['transit_details']['departure_time']['value'] - (timelist[0] + wait_total[0] + query_time)
  else:
    return 0
def adjust_totals(total_time,total_dist,bus,sub,train,tram,walk,step):
    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Bus):
      bus[0] += step['duration']['value']
      bus[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']

    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Subway):
      sub[0] += step['duration']['value'] 
      sub[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']
    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Rail):
      train[0] += step['duration']['value']
      train[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']
    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Tram):
      tram[0] += step['duration']['value']
      tram[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']
    




def leaving_adjust(time_to_leave):
    return (int(time.time())+ (int(time_to_leave)*60))
def correct_leave_time(duration,departure_epoch,leavetime):
  time1 = departure_epoch - leavetime
  time2 = duration + time1
  return time2
def client(API_KEY_INPUT):
  global x
  try:
    global gmaps
    gmaps = googlemaps.Client(key = str(API_KEY_INPUT))
  except:
    print "API Key " + str(x-1) + " Was Full or invalid.<br>"
    x += 1
    if (got_more_keys(KEYS,x) != False):      
      client(got_more_keys(KEYS,x))
    else:
      print "No More keys to run on. None of the keys provided worked."
      exit()
def finish_line(array_size,array_index,output):
  while(array_index != array_size):
    output.write(",transit,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL")
    array_index += 1
def format_orderlist(list):
  message = ""
  for item in list:
    if item.lower() == "rail":
      message += "train|tram|subway"
    else:
      if item != "0":
        message += item.lower()
    if list.index(item) != len(list)-1:
      if list[list.index(item)+1] != "0":
        message += "|"
  return message
def try_except(gmaps12,address,destination,time_to_leave,output,KEYS,a,Order_list):
  global gmaps
  global x
  try:
    global directions11
    directions11 = gmaps.directions(address,destination,departure_time=leaving(time_to_leave),mode='transit',units="metric",transit_mode=Order_list,alternatives="true")
  except googlemaps.exceptions.ApiError as e:
    print e
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,time_to_leave,output,KEYS,a,Order_list)
    else:
      print "Key Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(1,0,output)
      exit()
  except Exception as e:
    print e
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,time_to_leave,output,KEYS,a,Order_list)
    else:
      print "Key " + str(x-1) + " Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(1,0,output)
      exit()
def get_mode(count):
  if(count == 0):
    return "driving"
  if(count == 1):
    return "walking"
  if(count == 2):
    return "bicycling"
  if(count == 3):
    return "transit"

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
def get_seconds(t1,t2,Entry_count,mode_count):
  h1, m1, s1 = t1.hour, t1.minute, t1.second
  h2, m2, s2 = t2.hour, t2.minute, t2.second
  t1_secs = s1 + 60 * (m1 + 60*h1)
  t2_secs = s2 + 60 * (m2 + 60*h2)
  return((t2_secs/Entry_count)/mode_count)

def got_more_keys(KEYS,count):
  global x
  if(KEYS[count-1] == str("0") or x > len(KEYS)-1):
    return False
  return KEYS[count-1]

def check_timetoleave(line):
  if(len(line) > 4):
    return line[4]
  else:
 #   print "ELSE"
    return "0"

def get_departuretime(directions):
  if "departure_time" in directions.keys():
    if "value" in directions['departure_time'].keys():
      return directions['departure_time']['value']
  else:
    return int(time.time())
def check_dest_space(line):
  if(line.strip().split(',')[2][0] == ' '):
    return line.strip().split(",")[2][1:] + "," +line.strip().split(",")[3]
  else:
    return line.strip().split(",")[2] + "," +line.strip().split(",")[3]

if (sys.argv[1]=="-help"):
   print "To Run, execute as  such: \"python gmaps.py <input_file_name> <output_file_name>\""
   print "\n"
   print "Output File defaults to stdout if not specified.\n"
   print "Input File Format = <lat,long,lat,long NEWLINE>No spaces until end of second pair"
   exit(-1)

output = open(sys.argv[2],"w")
output_stepbystep = open( sys.argv[2][:-4] + "step_by_step.csv","w")
output_stepbystep.write("Trip,Option,Step,Mode,Tstart,Tend,Duration (Seconds) ,Distance (Meters),Details,Stops,\n")
#print sys.argv[1]
inputfile = open(sys.argv[1],"r")
#Path to output file created
modes_to_run = []
#-off and -on
Toggle_traffic_models = sys.argv[3]
#API KEY STORAGE
API_KEY_INPUT = sys.argv[4]
KEY2 = sys.argv[5]
KEY3 = sys.argv[6]
KEY4 = sys.argv[7]
KEY5 = sys.argv[8]
Order_list = [sys.argv[9],sys.argv[10],sys.argv[11],sys.argv[12]]

key_count = 0
KEYS=[API_KEY_INPUT,KEY2,KEY3,KEY4,KEY5]
for key in KEYS:
  if(key != "0"):
    key_count += 1
#Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)

address = ""
traffic_models_list = []
destination = ""
#print "<br>LINE COUNT: " + str(file_len(str(sys.argv[1])))

counter=0
y=0
client(API_KEY_INPUT)
header = ("tt1time,t1time," + "t1dist," + "t1steps,Bus_AbsTime,Bus_%Time,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,Wait_AbsTime,Wait_%Time,tt2time,t2time," + "t2dist," + "t2steps,Bus_AbsTime,Bus_%TIme,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,Wait_AbsTime,Wait_%Time,tt3time,t3time," + "t3dist,t3steps,Bus_AbsTime,Bus_%TIme,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,Wait_AbsTime,Wait_%Time,")
output.write("Slat,Slong,Dlat,Dlong,time," + header)
output.write("\n")
formated_list = format_orderlist(Order_list)
for line in inputfile:
  i=0
  counter += 1
  if(counter>=2490):
      print "Key #" + str(y) + " Reached its limit.<br>"
      counter=0
      y += 1
      if(KEYS[x] == '0'):
        print "END of Keys. Partial data download is available below.\n"
        exit()
      API_KEY_INPUT = KEYS[x]
      x+=1
 # print "LINE WAS: " + str(line.strip().split(","))
  address = line.strip().split(",")[0]+ ","+line.strip().split(",")[1]
  time_to_leave = check_timetoleave(line.strip().split(","))
  destination = check_dest_space(line)
  output.write(address+","+destination+",")
  query_time = leaving(time_to_leave)
  output.write(time.strftime('%H:%M:%S', time.localtime(query_time)))
  iterate_counter=0
  try_except(gmaps,address,destination,time_to_leave,output,KEYS,1,formated_list)
  for route in directions11:
  #  print "NEW ROUTE<br><br>"
    Bus_totals = [0,0]
    Sub_totals = [0,0]
    Train_totals = [0,0]
    Tram_totals = [0,0]
    Walk_totals = [0,0]
    Wait_total = [0,0]
    total_dist = [0]
    total_time = [0]    
    timelist = [0]
    wait_step_count = 0
    stepmsg = ""
    if(i<3):
      #    print "Route started at " + str(query_time)
      #    print "ARRIVAL : " + str(route['legs'][0]['arrival_time']['value'])
          for step in route['legs'][0]['steps']:
            if (route['legs'][0]['steps'].index(step) != 0):
              output_stepbystep.write("\n")
            if step['travel_mode'] != "TRANSIT":
       #       print "Current steps make the time " + str(timelist[0])
              output_stepbystep.write(str(counter) + "," + str(i+1) + "," + str(route['legs'][0]['steps'].index(step) + 1 + wait_step_count) + "," + str(step['travel_mode']))
              output_stepbystep.write("," + time.strftime('%H:%M:%S', time.localtime(query_time+ int(timelist[0]))) + "," + time.strftime('%H:%M:%S', time.localtime((query_time +timelist[0] + int(step['duration']['value'])))))
              output_stepbystep.write("," + str(step['duration']['value']) + "," + str(step['distance']['value']))
              Walk_totals[0] += step['duration']['value']
              total_dist[0] += step['distance']['value']
              timelist[0] += step['duration']['value']
              total_time[0] += step['duration']['value']
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters" + "|Dur:" + str(step['duration']['value']) + " seconds)"
            else:  #If transit of some kind
       #       print "Transit"
        #      print "Current steps make the time " + str(timelist[0])
              
              if int(get_waittime(step,query_time,timelist,Wait_total)) > 0:
                output_stepbystep.write(str(counter) + "," + str(i+1) + "," + str(route['legs'][0]['steps'].index(step) + 1) + ",")
                output_stepbystep.write("Wait" + ",")
                output_stepbystep.write(time.strftime('%H:%M:%S', time.localtime((query_time + int(timelist[0])))) + "," + time.strftime('%H:%M:%S', time.localtime((query_time + timelist[0]+ int(get_waittime(step,query_time,timelist,Wait_total))))))
                output_stepbystep.write("," + str((query_time + timelist[0] + int(get_waittime(step,query_time,timelist,Wait_total))) - (query_time + int(timelist[0]))) + "\n")
                wait_step_count += 1
                Wait_total[0] += int(get_waittime(step,query_time,timelist,Wait_total))
                timelist[0] += int(get_waittime(step,query_time,timelist,Wait_total))
              output_stepbystep.write(str(counter) + "," + str(i+1) + "," + str(route['legs'][0]['steps'].index(step) + 1 + wait_step_count) + ",")
              output_stepbystep.write(str(step['travel_mode']) + ",")
              output_stepbystep.write(time.strftime('%H:%M:%S', time.localtime((query_time + int(timelist[0])))) + "," + time.strftime('%H:%M:%S', time.localtime((query_time + timelist[0]+ step['duration']['value']))))
              output_stepbystep.write("," + str(step['duration']['value']) + "," + str(step['distance']['value']))
              output_stepbystep.write("," + str(step['transit_details']['line']['vehicle']['type']) + " " + short_or_full(step['transit_details']['line']))
              output_stepbystep.write("," + str(step['transit_details']['num_stops']))
              adjust_totals(timelist,total_dist,Bus_totals,Sub_totals,Train_totals,Tram_totals,Walk_totals,step)
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters|Dur:" + str(step['duration']['value']) + " seconds|" + "[Transit_Type:" +  step['transit_details']['line']['vehicle']['type'] + "|Leaves:" + step['transit_details']['departure_time']['text'] + "|Arrives:" + step['transit_details']['arrival_time']['text'] + "|Name:" + short_or_full(step['transit_details']['line']) + "|Total_Stops:" +  str(step['transit_details']['num_stops']) + "])"
            if route['legs'][0]['steps'].index(step) != len(route['legs'][0]['steps'])-1:
              stepmsg += "_NEXT_"
          output_stepbystep.write("\n")
          total_time[0] = int(correct_leave_time(directions11[i]['legs'][0]['duration']['value'],get_departuretime(directions11[i]['legs'][0]),leaving_adjust(time_to_leave)))
          output.write(",")
          output.write(str(int(timelist[0] + Wait_total[0])))
          output.write(",")
          output.write(str(timelist[0]))
          output.write(",")
          output.write(str(directions11[i]['legs'][0]['distance']['value']) + ",")
          output.write(stepmsg)
          print_breakdown_types(total_time,total_dist,Bus_totals,Sub_totals,Train_totals,Tram_totals,Walk_totals,Wait_total,output,query_time)
          i += 1
  
  while(i<3):
    output.write(",NULL,NULL,NULL,NULL")
    output.write(","+"0,0,0,0,0,0,0,0,0,0,0,0")
    i+=1
  output.write("\n")
  
output.close()
inputfile.close()

