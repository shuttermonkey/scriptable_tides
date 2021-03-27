# scriptable_tides

![widget](https://github.com/shuttermonkey/scriptable_tides/blob/main/screenshots/widget.jpg)



iOS scriptable widget to show local tide status with python scripts to generate the relevant data

## About this project

This project generates a widget that displays local tide information on iPhone or iPad home screens. using the [Scriptable](https://scriptable.app) app by Simon Støvring.

The widget uses data from the [NOAA Tides and Currents site](https://tidesandcurrents.noaa.gov/noaatideannual.html?id=8468448) which is reformatted and updated via the two python scripts. 

## How to use this

To use this widget, make a new script inside Scriptable and paste in the contents of `scriptable_tides.js`. 

You can run the script from within the app, or add a new Small widget on your home screen, set it to Scriptable, and choose the script by tapping and holding on the widget, choosing Edit Widget, and choosing the script by tapping on the Script field. 

I have the pythonscripts installed on a raspberry pi which runs the tides2JASON.py script regularly via cron and uploads the info to a self-hosted site

The localTideData.py script only really needs to be run every three years to update the tide data which manually needs to be downloaded from the NOAA site. One txt file is downloaded for each year with the following parameters: MLLW Datum, 12H clock, GMT timezone, format TXT # scriptable_tides
