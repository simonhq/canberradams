
## AppDaemon Libraries

Please add the following packages to your appdaemon configuration

``` yaml
system_packages: []
python_packages:
  - xmltodict
init_commands: []
```

_Note: bs4 (beautiful soup) is no longer required for this app_

## App configuration

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