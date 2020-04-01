# Canberra Dams
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

_Creates a sensor for Home Assistant with the ACT Dam level information_

## Installation

This app is best installed using
[HACS](https://github.com/custom-components/hacs), so that you can easily track
and download updates.

Alternatively, you can download the `canberradams` directory from inside the `apps` directory here to your
local `apps` directory, then add the configuration to enable the `canberradams` module.

You will also need to install Beautiful Soup / bs4 and then copy the bs4 directory into the apps directory in Appdaemon.

## How it works

The [Icon Water](https://www.iconwater.com.au/water-education/water-and-sewerage-system/dams/water-storage-levels.aspx) site provides this information, this just scrapes
the page and makes the information available as a sensor in HA.

As this is non time critical sensor, it does not get the information on a set time schedule, but watches a input_boolean that you 
specify for when to update the sensor. You can obviously automate when you want that input_boolean to turn on.

### To Run

You will need to create an input_boolean entity to watch for when to update the sensor. When this
`input_boolean` is turned on, whether manually or by another automation you
create, the scraping process will be run to create/update the sensor.

## App configuration

```yaml
canberra_dams:
  module: canberradams
  class: Get_ACT_Dams
  DAM_FLAG: "input_boolean.check_dams"
  DAM_SENSOR: "sensor.act_dam_levels"
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | `canberradams`
`class` | False | string | | `Get_ACT_Dams`
`DAM_FLAG` | False | string || The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_dams 
`DAM_SENSOR` | False | string || The name of the sensor to create/update

## Issues/Feature Requests

Please log any issues or feature requests in this GitHub repository for me to review.