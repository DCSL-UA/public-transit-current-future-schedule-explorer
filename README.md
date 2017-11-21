# Google_DirectionsAPI_DataExport
An intuitive interface for interacting with and pulling valuable transit data from Google's Direction API.
# Idea
This repository contains an HTML web interface used to interact with a python script that queries the Google Directions API for directions going from Point A to Point B using strictly public transportation (transit). The exact specifications of this script are in line with those outlined on the [Directions API Developer's Guide](https://developers.google.com/maps/documentation/directions/intro "Directions API Developer's Guide")

The python script itself can be executed alone, using the parameter options outlined in the comments of the file, but the HTML web interface ensures that no silly errors are done, and also ensures a number of conditions are met. 

# Input and Output Files
All input files sent via the HTML Interface are saved into the `uploads_transit` directory. All output files are saved in the `output_transit` directory. The file that was produced as a result of running the python script is then presented for download via the webpage. Should something go wrong, the file can then be accessed in the outputs directory, along with its corresponding upload file, to determine what went wrong. 

## Input File Format
The python script is supplied an input file which is read. Each line contains a point A and Point B lat and long in the following format:
`POINTALat,POINTALong,POINTBLat,POINTBLong,Minutes_in_Future`
The above represents one single line of the file. A space is allowed **after the comma** following `POINTALong`.
### Minutes in Future Explained
The Google Directions API allows you to query for times in the future. In the case where the mode is transit, it allows us to see into the future schedule of possible routes from point A to point B. By querying for minutes into the future, we can see those routes now, rather than waiting. Providing a "0" here will run that line of input right now, no minutes in the future. Providing a "120" will run that line of input right now, but will ask google to provide route information as if it were exactly 2 hours in the future.

## Output Files
The HTML Interface saves all the output files using the current time and date so as not to repeat any filenames, overwriting old data or causing file errors, and to ensure that it is easy to match up corresponding input and output files. The time the input file was uploaded will match the name of the output file. 

The python script has the same header for each file, it is as follows: 
```Slat,Slong,Dlat,Dlong,time,tt1time,t1time,t1dist,t1steps,Bus_AbsTime,Bus_%Time,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,Wait_AbsTime,Wait_%Time,tt2time,t2time,t2dist,t2steps,Bus_AbsTime,Bus_%TIme,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,Wait_AbsTime,Wait_%Time,tt3time,t3time,t3dist,t3steps,Bus_AbsTime,Bus_%TIme,Sub_AbsTime,Sub%Time,Tr_AbsTime,Tr_%Time,Tram_AbsTime,Tram_%Time,Walk_AbsTime,Walk_%Time,Wait_AbsTime,Wait_%Time```
Slat = Point A latitude<br />
Slong = Point A longitude<br />
Dlat = Point B latitude<br />
Dlong = Point B longitude<br />
time = Time that the query for this was sent to google's API (If we were provided a "Minutes_in_Future" of "1", then the time here will be 1 minute in the future of the current time that this execution was performed)
tt1time = Total travel time, including time spent waiting for a form of transit
t1time = Time that google says this trip will take for Route 1 of potentially 3 (in seconds), not including wait time
t1dist = Distance in meters for route 1 of potentially 3.
t1steps = Steps for traveling Point A to Point B according to google, includes exact transit information and time spent on each step. Varys greatly, format is explained below.
Bus_AbsTime = Absolute number of seconds spent on a bus
Bus_%Time = % Time spent on bus relative to total trip time including wait time. 
This format follows for each possible type of travel, all the way through wait time and wait %.
Obviously t2* and t3* is the same as above for Routes 2 and 3, including the breakdown of each travel type.

### Explanation of Multiple Routes
For any given point A and point B there is potentially 4 routes that google sends back (Can be obtained by using parameter `alternatives="True"` as shown in Developer's Guide. We are returning at most 3 of those routes. However, there does not always have to be 3 routes, there does not always have to be even 1 route (I.e bad input or maybe the two points don't have roads that connect them according to google). In the case that there is less than 3 routes, the python script dynamically fills the remaining space with `NULL` values. 
### Explanation of Step Information
Under t1steps, t2steps, and t3steps contains each and every step that google says is to be completed in order to get from point A to point B. Delineation between each step is shown as `__NEXT__`. For every "(" there is a single letter that follows. That is the first letter of the type of travel occuring. W = Walk, T = Transit. We list the duration and distance of that step as google provides. When we have Transit, we provide a breakdown on the specific transit occuring. it starts with "\[". Inside, is the breakdown of the type of transit specifically, the name of the transit (F train, for example), when it leaves, arrives, and the number of stops to travel. 
### Explanation of Wait Time
Google's Direction API returns the route when we query. The way google does this is by specifying the departure time of the route to some given time. For any given time that we have queried for, the departure time can be, in some cases, 15 minutes in the future. Google's trip duration time is calculated for that departure time to the stated arrival time. However, if we have asked google to provide route information at 10:00:00 AM CST, and the stated departure time that we get back is 10:05:00 AM CST, there is a 5 minute time period here. Now this time would normally be spent at the transit station, waiting for the bus to arrive. Google sets the departure time to 10:05 so that you spend exactly as little time as needed waiting. However, if we truly start our trip at 10:00:00 AM CST, then we will be spending 5 minutes waiting at the transit station. Thus, we can get the total amount of time spent waiting by adding the difference of 10:05:00 AM CST and 10:00:00 AM CST to the total trip time. 
### Explanation of Setting Preferences of Mode of Travel
Google's Direction API lets us set preferred transit modes (Bus,Subway,Train, and Tram). If we set our preference to Bus, then google will return routes with busses over those with other forms if they exist. The HTML interface limits the options of selection for you to conform to the Direction API limitations. "Rail" is equivalent to the setting of "train|tram|subway" in that order. You can specify a different order of train, tram, and subway, by selecting them individually, as the HTML interface allows you to do. 
#### Explaining HTML Interface selection of Preferred Travel Mode
The HTML interface will not allow you to select the term "Rail" and then select any of the Train, Tram, or Subway options, as those have already been specified by selecting Rail. If you select Subway, you can not select Subway later on in the preferences. Same goes for all other options. This ensures that we always conform to Google's Direction API limitations as outlined in their Developer's Guide.


