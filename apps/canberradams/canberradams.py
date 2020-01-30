############################################################
#
# This class aims to get the Canberra ACT dam levels from Icon Water
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# Written: 30/01/2020
# on windows use py -m pip install beautifulsoup4
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
#   DAM_SENSOR: "sensor.act_dam_levels"
#   global_dependencies:
#     - globals
#     - secrets
#
############################################################

# import the function libraries for beautiful soup
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import appdaemon.plugins.hass.hassapi as hass
import globals

class Get_ACT_Dams(hass.Hass):

    # the name of the flag in HA (input_boolean.xxx) that will be watched/turned off
    DAM_FLAG = ""
    DAM_SENSOR = ""
    URL = "https://www.iconwater.com.au/water-education/water-and-sewerage-system/dams/water-storage-levels.aspx"

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        self.DAM_FLAG = globals.get_arg(self.args, "DAM_FLAG")
        self.DAM_SENSOR = globals.get_arg(self.args, "DAM_SENSOR")

        # create the original sensor
        self.load(self.DAM_SENSOR)

        # listen to HA for the flag to update the sensor
        self.listen_state(self.main, self.DAM_FLAG, new="on")

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """ create the sensor and turn off the flag
            
        """
        # create the sensor with the dam information 
        self.load(self.DAM_SENSOR)
        
        # turn off the flag in HA to show completion
        self.turn_off(self.DAM_FLAG)

    def load(self, dam_sensor):
        """ parse the elders weather ACT dam level website
        """

        #connect to the website and scrape the dam levels for the ACT
        url = self.URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        all_tags = soup.findAll('span')

        # create the sensor with the dam information 
        self.create_sensor(dam_sensor, all_tags)

    def create_sensor(self, dam_sensor, dam_levels):
        """ pass the raw html string and input text to add it to 
        :param dam_sensor: the name of the sensor to create in home assistant
        :param dam_levels: the array of dam levels from the website
        :return: -
        """

        # percentage in the dams
        catch_per = self.get_val(dam_levels, 2)
        
        self.set_state(dam_sensor, state=catch_per, replace=True, attributes= {"icon": "mdi:cup-water", "friendly_name": "ACT Dam Levels"})

    def get_val(self, dam_levels, array_pos):
        """ pass the array of values and the position to return the string 
        :param dam_levels: the array of dam levels from the website
        :param array_pos: the position in the array to return
        :return: string from the array
        """
        tagged_str = dam_levels[array_pos]
        soupa = BeautifulSoup(str(tagged_str), "html.parser")
        return soupa.get_text()
