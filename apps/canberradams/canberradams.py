############################################################
#
# This class aims to get the Canberra ACT dam levels from Icon Water
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# Written: 30/01/2020
# updated: 03/05/2020
# 
############################################################

############################################################
# 
# In the apps.yaml file you will need the following
# updated for your database path, stop ids and name of your flag
#
# canberra_dams:
#   module: canberradams
#   class: Get_ACT_Dams
#   DAM_FLAG: "input_boolean.check_dams"
#
############################################################

# import the function libraries
import requests
import datetime
import json
import xmltodict
import appdaemon.plugins.hass.hassapi as hass

class Get_ACT_Dams(hass.Hass):

    # the name of the flag in HA (input_boolean.xxx) that will be watched/turned off
    DAM_FLAG = ""
    URL = "https://www.iconwater.com.au/layouts/ACTEW/charts/GetCurrentDamLevelsExtended.aspx"

    up_sensor = "sensor.act_dam_last_updated"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        self.DAM_FLAG = self.args["DAM_FLAG"]

        # create the original sensor
        self.load()

        # listen to HA for the flag to update the sensor
        self.listen_state(self.main, self.DAM_FLAG, new="on")

        # set to run each morning at 5.23am
        runtime = datatime.time(5,23,0)
        self.run_daily(self.load, runtime)

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """ create the sensor and turn off the flag
            
        """
        # create the sensor with the dam information 
        self.load()
        
        # turn off the flag in HA to show completion
        self.turn_off(self.DAM_FLAG)

    def load(self):
        """ parse the ICON Water ACT dam level website
        """

        #connect to the website and scrape the dam levels for the ACT
        url = self.URL
        response = requests.request("GET", url, headers=self.headers, data = self.payload)
        
        #create a sensor to keep track last time this was run
        tim = datetime.datetime.now()
        date_time = tim.strftime("%d/%m/%Y, %H:%M:%S")
        self.set_state(self.up_sensor, state=date_time, replace=True, attributes= {"icon": "mdi:timeline-clock-outline", "friendly_name": "ACT Dam Levels Data last sourced"})
        
        page = xmltodict.parse(response.text)
        dtags = json.loads(json.dumps(page))
        
        #get the second series - with percentages and remaining volumes
        dams = dtags['data']['series'][1]
        #self.log(readings)
        #get the values for each dam
        for x in range(5):
            #dam name
            dname = dams['reading'][x]['dam']
            #dam percentage full
            dper = dams['reading'][x]['percentageFull']
            #dam remaining capacity
            drcap = dams['reading'][x]['amount']
            #total capacity is rcap/(100-dper)*100
            dcap = float(drcap) / (100 - float(dper)) * 100
            #current available
            davail = dcap - float(drcap)
            #sensor name
            sensor_name = 'sensor.act_dam_' + dname.replace(" ","_")

            #create the sensors for each of the dams and the combined volumes
            self.set_state(sensor_name, state=dper, replace=True, attributes= {"icon": "mdi:cup-water", "friendly_name": "ACT Dam Level - " + dname, "unit_of_measurement": "%", "Current Available": "{:12.2f}".format(davail), "Total Capacity": "{:12.2f}".format(dcap) })
