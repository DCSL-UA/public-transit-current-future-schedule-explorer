#Usage, "Python schedule_explorer.py <INputFile> <OutputFileName> -off <FirstAPIKey> <SecondAPIKey> <ThirdAPIKey> <FourthAPIKey> <FifthAPIKey>"
#If you don't have a key present beyond 1, simply enter 0 for that key, so as not to screw up the reading in of args. 
#Input file Format: PointALat,PointALong,PointBLat,PointBLong,MinutesInFuturetoQuery
#A space is allowed between PointALong and PointBLat after the comma. "POintALong,<SPACE>POIntBLat" is valid.
#This script improves on last by now including a breakdown of all types of traveling, including waiting, with seconds and % time spent performing each type of moving during a trip.
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

def print_breakdown_types(total_time,total_dist,bus,sub,train,tram,walk,wait,output):
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
    return step['distance']['value']




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

def try_except(gmaps12,address,destination,time_to_leave,output,KEYS,a):
  global gmaps
  global x
  try:
    global directions11
    directions11 = gmaps.directions(address,destination,departure_time=leaving(time_to_leave),mode='transit',units="metric",alternatives="true")
  except googlemaps.exceptions.ApiError as e:
    print e
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,time_to_leave,output,KEYS,a)
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
      try_except(gmaps,address,destination,time_to_leave,output,KEYS,a)
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

  address = line.strip().split(",")[0]+ ","+line.strip().split(",")[1]
  time_to_leave = line.strip().split(",")[4]
  destination = check_dest_space(line)
  output.write(address+","+destination+",")
  output.write(time.strftime('%H:%M:%S', time.localtime(leaving(time_to_leave))))
  iterate_counter=0
  try_except(gmaps,address,destination,time_to_leave,output,KEYS,1)
  
  for route in directions11:
    Bus_totals = [0,0]
    Sub_totals = [0,0]
    Train_totals = [0,0]
    Tram_totals = [0,0]
    Walk_totals = [0,0]
    Wait_total = [0,0]
    total_dist = [0]
    total_time = [0]    
    timelist = [0]

    stepmsg = ""
    if(i<3):
          for step in route['legs'][0]['steps']:
            if step['travel_mode'] != "TRANSIT":
              Walk_totals[0] += step['duration']['value']
              Walk_totals[1] += step['distance']['value']
              total_dist[0] += step['distance']['value']
              timelist[0] += step['duration']['value']
              total_time[0] += step['duration']['value']
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters" + "|Dur:" + str(step['duration']['value']) + " seconds)"
            else:  #If transit of some kind
              adjust_totals(timelist,total_dist,Bus_totals,Sub_totals,Train_totals,Tram_totals,Walk_totals,step)
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters|Dur:" + str(step['duration']['value']) + " seconds|" + "[Transit_Type:" +  step['transit_details']['line']['vehicle']['type'] + "|Leaves:" + step['transit_details']['departure_time']['text'] + "|Arrives:" + step['transit_details']['arrival_time']['text'] + "|Name:" + short_or_full(step['transit_details']['line']) + "|Total_Stops:" +  str(step['transit_details']['num_stops']) + "])"
            if route['legs'][0]['steps'].index(step) != len(route['legs'][0]['steps'])-1:
              stepmsg += "_NEXT_"
          total_time[0] = int(correct_leave_time(directions11[i]['legs'][0]['duration']['value'],directions11[i]['legs'][0]['departure_time']['value'],leaving_adjust(time_to_leave)))
          Wait_total[0] = total_time[0] - timelist[0]
          output.write(",")
          output.write(str(correct_leave_time(directions11[i]['legs'][0]['duration']['value'],directions11[i]['legs'][0]['departure_time']['value'],leaving_adjust(time_to_leave))))
          output.write(",")
          output.write(str(timelist[0]))
          output.write(",")
          output.write(str(directions11[i]['legs'][0]['distance']['value']) + ",")
          output.write(stepmsg)
          print_breakdown_types(total_time,total_dist,Bus_totals,Sub_totals,Train_totals,Tram_totals,Walk_totals,Wait_total,output)
          i += 1
  output.write("\n")
  


