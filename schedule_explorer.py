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

def print_breakdown_types(total_time,total_dist,bus,sub,train,tram,walk,output):
  print "TIME" + str(total_time)
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
header = ("tt1time,t1time," + "t1dist," + "t1steps,Bus_AbsTime,Bus_%Time,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,tt2time,t2time," + "t2dist," + "t2steps,Bus_AbsTime,Bus_%TIme,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,tt3time,t3time," + "t3dist,t3steps,Bus_AbsTime,Bus_%TIme,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,")
output.write("Slat,Slong,Dlat,Dlong,time," + header)
output.write("\n")
for line in inputfile:
  output.write("\n")
  outputjson = open("google_outputtestold" + str(counter) +".json","w")
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
    Bus_totals = [0,0]
    Sub_totals = [0,0]
    Train_totals = [0,0]
    Tram_totals = [0,0]
    Walk_totals = [0,0]
    total_dist = [0]
    total_time = [0]
    stepmsg = ""
    if(i<3):
          for step in route['legs'][0]['steps']:
            if step['travel_mode'] != "TRANSIT":
              print "HERE2"
              Walk_totals[0] += step['duration']['value']
              Walk_totals[1] += step['distance']['value']
              total_dist[0] += step['distance']['value']
              total_time[0] += step['duration']['value']
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters" + "|Dur:" + str(step['duration']['value']) + " seconds)"
            else:  #If transit of some kind
              adjust_totals(total_time,total_dist,Bus_totals,Sub_totals,Train_totals,Tram_totals,Walk_totals,step)
              stepmsg += "(" + step['travel_mode'][0] + "|Dist:" + str(step['distance']['value']) + " meters|Dur:" + str(step['duration']['value']) + " seconds|" + "[Transit_Type:" +  step['transit_details']['line']['vehicle']['type'] + "|Leaves:" + step['transit_details']['departure_time']['text'] + "|Arrives:" + step['transit_details']['arrival_time']['text'] + "|Name:" + short_or_full(step['transit_details']['line']) + "|Total_Stops:" +  str(step['transit_details']['num_stops']) + "])"
            if route['legs'][0]['steps'].index(step) != len(route['legs'][0]['steps'])-1:
              stepmsg += "_NEXT_"
          output.write(",")
          output.write(str(correct_leave_time(directions[i]['legs'][0]['duration']['value'],directions[i]['legs'][0]['departure_time']['value'],leaving_adjust(time_to_leave))))
          output.write(",")
          output.write(str(total_time[0]))
          output.write(",")
          output.write(str(directions[i]['legs'][0]['distance']['value']) + ",")
          output.write(stepmsg)
          print_breakdown_types(total_time,total_dist,Bus_totals,Sub_totals,Train_totals,Tram_totals,Walk_totals,output)
          i += 1
