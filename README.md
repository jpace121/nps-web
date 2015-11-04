#NPS Penetrometer WebApp Code#

##Introduction##
This project contains the code needed to run the web app that controls
and records data from the penetrometer. 

The project is designed to run on a Beaglebone Black with a wifi and bluetooth
dongle.

At start up, the Beaglebone launches a web server running the web app. The user
then connects to the Beaglebone's Wifi network (called "Penetrometer"), and,
using a web browser, navigates to the web app (any URL should redirect to the
correct web page).

From there, the user should follow the directions on the page to control the 
penetrometer.

The rest of this document provides an overview of the software architecture
and layout of the project. This document's intent is to provide enough detail
about the project that a suitably skilled individual would know where to start
if they needed to add a new feature or fix a bug.

##Start Up##
To launch the web app, run the file './start-up.sh'. This file sets up the 
beaglebone for gpio and communication and lauanches the web server. 

'serve_tornado.py' launches a web server (provided by Tornado). Tornado is 
used purely as a web server, not for URL routing, etc. 
The web app itself is managed using Flask in the file './website.py'.

The web app API was designed to be RESTful. URLs that have an underscore as 
their first characters are API endpoints, talked to by the Javascript on the
web page, not the user themselves. The other URLs are navigatable by a web 
browser and etiher generate html or a specific file or image.

To communicate with the backend, the javascript on the front end sends AJAX
requests which include an option variable. Based on the value of the option 
variable, the back end does some action and calculates some response.

The code in 'website.py' doesn't contain the actual logic that communicates with
the sensors. This code is contained in individual other files.

The logic to communicate with the sensors is located in 'distanceSesnor.py'
and 'forceSensor.py' respectively. Both files should have their own 
documentation. Examples on how to use the classes contained in each file 
are given in the bottom of each file in the section after 'if __name__ == 
"__main__"'. 

'save_to_csv.' contains the logic the backend needs to allow for the saving
and downloading of the log files. 'makePlot.py' contains the logic needed to 
plot the streamed data.




