############################################################
#
# This class aims to get the Canberra ACT dam levels from the elders weather website 
#
# written to be run from AppDaemon for a HASS or HASSIO install
#
# Written: 13/01/2020
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

    # run each step against the database
    def initialize(self):

        # get the values from the app.yaml that has the relevant personal settings
        self.DAM_FLAG = globals.get_arg(self.args, "DAM_FLAG")
        self.DAM_SENSOR = globals.get_arg(self.args, "DAM_SENSOR")
                
        # listen to HA for the flag to see if it is necessary to run this code against a new database
        self.listen_state(self.main, self.DAM_FLAG, new="on")

    # run the app
    def main(self, entity, attribute, old, new, kwargs):
        """ parse the elders weather ACT dam level website
            
        """
        
        #connect to the website and scrape the dam levels for the ACT
        url = 'https://www.eldersweather.com.au/dam-level/act/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        all_td = soup.findAll('td')

        # create the sensor with the dam information 
        self.create_sensor(self.DAM_SENSOR, all_td)
        
        # turn off the flag in HA to show completion
        self.turn_off(self.DAM_FLAG)


    def create_sensor(self, dam_sensor, dam_levels):
        """ pass the raw html string and input text to add it to 
        :param dam_sensor: the name of the sensor to create in home assistant
        :param dam_levels: the array of dam levels from the website
        :return: -
        """

        # percentage in the dams
        catch_cap = self.get_val(dam_levels, 1)
        catch_per = self.get_val(dam_levels, 2)
        googong_per = self.get_val(dam_levels, 5)
        cotter_per = self.get_val(dam_levels, 8)
        corin_per = self.get_val(dam_levels, 11)
        bendora_per = self.get_val(dam_levels, 14)

        
        self.set_state(dam_sensor, state=catch_per, replace=True, attributes= {"Catchment Capacity": catch_cap, "Googong": googong_per, "Cotter": cotter_per, "Corin": corin_per, "Bendora": bendora_per}) 

    def get_val(self, dam_levels, array_pos):
        """ pass the array of values and the position to return the string 
        :param dam_levels: the array of dam levels from the website
        :param array_pos: the position in the array to return
        :return: string from the array
        """
        tagged_str = dam_levels[array_pos]
        soupa = BeautifulSoup(str(tagged_str), "html.parser")
        return soupa.get_text()
