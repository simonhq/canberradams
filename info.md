
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
`DAM_FLAG` | False | string | | The name of the flag in HA for triggering this sensor update - e.g. input_boolean.check_dams 
`DAM_SENSOR` | False | string | | The name of the sensor to create/update
