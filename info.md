
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
`DAM_FLAG` | False | string | | The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_dams 

## Sensors Created

This version will create 6 sensors

* sensor.act_dam_last_updated
* sensor.act_dam_bendora_dam
* sensor.act_dam_combined_volume
* sensor.act_dam_corin_dam
* sensor.act_dam_cotter_dam
* sensor.act_dam_googong_dam