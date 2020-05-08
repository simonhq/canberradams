# Canberra Dams
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Creates sensors for Home Assistant with the ACT Dam level information_

## Lovelace Example

![Example of the entities in Lovelace](https://github.com/simonhq/canberradams/blob/master/canberra_dams_entities.PNG)

![An Entity has capacity and current volume](https://github.com/simonhq/canberradams/blob/master/canberra_dams_entity.PNG)

## Installation

This app is best installed using
[HACS](https://github.com/custom-components/hacs), so that you can easily track
and download updates.

Alternatively, you can download the `canberradams` directory from inside the `apps` directory here to your
local `apps` directory, then add the configuration to enable the `canberradams` module.

You will also need to install Beautiful Soup / bs4 and then copy the bs4 directory into the apps directory in Appdaemon.

## How it works

The [Icon Water](https://www.iconwater.com.au/layouts/ACTEW/charts/GetCurrentDamLevelsExtended.aspx) site provides this information, this just scrapes
the page and makes the information available as sensors in HA.

As this is non time critical sensor, it does not get the information on a set time schedule, but watches a input_boolean that you 
specify for when to update the sensor. You can obviously automate when you want that input_boolean to turn on.

### To Run

You will need to create an input_boolean entity to watch for when to update the sensor. When this
`input_boolean` is turned on, whether manually or by another automation you
create, the scraping process will be run to create/update the sensor.

## AppDaemon Libraries

Please add the following packages to your appdaemon 4 configuration on the supervisor page of the add-on.

``` yaml
system_packages: []
python_packages:
  - xmltodict
init_commands: []
```

_Note: bs4 (beautiful soup) is no longer required for this app_

## App configuration

In the apps.yaml file in the appdaemon/apps directory - 

```yaml
canberra_dams:
  module: canberradams
  class: Get_ACT_Dams
  DAM_FLAG: "input_boolean.check_dams"
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | `canberradams`
`class` | False | string | | `Get_ACT_Dams`
`DAM_FLAG` | False | string || The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_dams 

## Sensors Created

This version will create 6 sensors

* sensor.act_dam_last_updated
* sensor.act_dam_bendora_dam
* sensor.act_dam_combined_volume
* sensor.act_dam_corin_dam
* sensor.act_dam_cotter_dam
* sensor.act_dam_googong_dam

## Issues/Feature Requests

Please log any issues or feature requests in this GitHub repository for me to review.