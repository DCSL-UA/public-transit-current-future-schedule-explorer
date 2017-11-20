#Usage, "Python schedule_explorer.py <Input_File> <Output_File_name> <APIKEY>"
#Input file format is as follows: PointALat,PointALong,PointBLat,PointBLong,MinutesinFuturetoQuery new line for each pair

import json, urllib
import googlemaps
import time
from datetime import datetime
import sys
import datetime
import time
counter = 0
output = open(sys.argv[2],"w")
#print sys.argv[1]
inputfile = open(sys.argv[1],"r")
#Path to output file created
API_KEY_INPUT = sys.argv[3]
modes_to_run = []
#-off and -on
key_count = 0

#Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)

def short_or_full(directions):
  if "short_name" in directions.keys():
    return directions['short_name']
  else:
    return directions['name']
def leaving(time_to_leave):
    return float(time.time()+ float(int(time_to_leave)*60))

def leaving_adjust(time_to_leave):
    return int(time.time()+ float(int(time_to_leave)*60))
header = ("t1departure_time,t1time," + "t1dist," + "t1steps,t2departure_time,t2time," + "t2dist," + "t2steps,t3departure_time,t3time," + "t3dist,t3steps")
output.write("Slat,Slong,Dlat,Dlong,query_time," + header)
output.write("\n")

def correct_leave_time(duration,departure_epoch,leavetime):
  time1 = departure_epoch - leavetime
  time2 = duration + time1
  return int(time2)
for line in inputfile:
  output.write("\n")
  outputjson = open("google_outputtest" + str(counter) +".json","w")
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
  if(line.strip().split(',')[2][0] == ' '):
    destination = line.strip().split(",")[2][1:] + "," +line.strip().split(",")[3]
  else:
    destination = line.strip().split(",")[2] + "," +line.strip().split(",")[3]
  output.write(address+","+destination+",")
  output.write(time.strftime('%H:%M:%S', time.localtime(leaving(time_to_leave))))
  traffic_models_list = []
  try:
    gmaps = googlemaps.Client(key = str(API_KEY_INPUT))
  except ValueError:
    print "API Key was invalid or we ran out of keys to use. Please try again. Partial data may be available in link below.\n"
  iterate_counter=0
  try:
    directions = gmaps.directions(address,destination,departure_time=leaving(time_to_leave),mode='transit',units="metric",alternatives="true")
  except googlemaps.exceptions.ApiError:
    print "API Key is either no longer active or has filled up. Please try with a different key.\n"
    exit()
  except Exception as e:
    print "Error: " + str(e)
    exit()
  i=0
  stepmsg = ""
  outputjson.write(json.dumps(directions, sort_keys=True,indent=4))
  for route in directions:
    stepmsg = ""
    if(i<3):
          output.write(",")
          output.write(str(directions[i]['legs'][0]['departure_time']['text']))
          output.write(",")
          output.write(str(correct_leave_time(directions[i]['legs'][0]['duration']['value'],directions[i]['legs'][0]['departure_time']['value'],leaving_adjust(time_to_leave))))
          output.write(",")
          output.write(str(directions[i]['legs'][0]['distance']['value']) + ",")
          for step in route['legs'][0]['steps']:
            if step['travel_mode'] != "TRANSIT":
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters" + "|Dur:" + str(step['duration']['value']) + " seconds)"
            else: 
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters|Dur:" + str(step['duration']['value']) + " seconds|" + "[Transit_Type:" +  step['transit_details']['line']['vehicle']['type'] + "|Arrives:" + step['transit_details']['arrival_time']['text'] + "|Leaves:" + step['transit_details']['departure_time']['text'] + "|Name:" + short_or_full(step['transit_details']['line']) + "|Total_Stops:" +  str(step['transit_details']['num_stops']) + "])"
            if route['legs'][0]['steps'].index(step) != len(route['legs'][0]['steps'])-1:
              stepmsg += "_NEXT_"
          output.write(stepmsg)
          i += 1
