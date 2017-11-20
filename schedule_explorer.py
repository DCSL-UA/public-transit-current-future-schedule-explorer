#Usage, "Python schedule_explorer.py <INputFile> <OutputFileName> -off <FirstAPIKey> <SecondAPIKey> <ThirdAPIKey> <FourthAPIKey> <FifthAPIKey>"
#If you don't have a key present beyond 1, simply enter 0 for that key, so as not to screw up the reading in of args. 
#Input file Format: PointALat,PointALong,PointBLat,PointBLong,MinutesInFuturetoQuery
#A space is allowed between PointALong and PointBLat after the comma. "POintALong,<SPACE>POIntBLat" is valid.
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

counter=0
y=0
client(API_KEY_INPUT)
header = ("t1time," + "t1dist," + "t1steps,t2time," + "t2dist," + "t2steps,t3time," + "t3dist,t3steps")
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
    stepmsg = ""
    if(i<3):
          for step in route['legs'][0]['steps']:
            if step['travel_mode'] != "TRANSIT":
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters" + "|Dur:" + str(step['duration']['value']) + " seconds)"
            else:  #If transit of some kind
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters|Dur:" + str(step['duration']['value']) + " seconds|" + "[Transit_Type:" +  step['transit_details']['line']['vehicle']['type'] + "|Leaves:" + step['transit_details']['departure_time']['text'] + "|Arrives:" + step['transit_details']['arrival_time']['text'] + "|Name:" + short_or_full(step['transit_details']['line']) + "|Total_Stops:" +  str(step['transit_details']['num_stops']) + "])"
            if route['legs'][0]['steps'].index(step) != len(route['legs'][0]['steps'])-1:
              stepmsg += "_NEXT_"
          output.write(",")
          output.write(str(correct_leave_time(directions11[i]['legs'][0]['duration']['value'],directions11[i]['legs'][0]['departure_time']['value'],leaving_adjust(time_to_leave))))
          output.write(",")
          output.write(str(directions11[i]['legs'][0]['distance']['value']) + ",")
          output.write(stepmsg)
          i += 1
  output.write("\n")
  


