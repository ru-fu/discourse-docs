> **RESTRUCTURE**: Should the table be split out into reference?

# Configure geographical location

Anbox Cloud allows specifying a static geographical location which is provided to the Android container.  The location is configured in the file `/var/lib/anbox/static_gps_position` within the Anbox container.

The location data is constructed in the following format:

```
<Latitude>,<Latitude in hemisphere>,<Longitude>,<Longitude in hemisphere>
```

For example:

    4807.038,N,1131.001,E

You can find details about the different parts of the location in the following table.

Field                   | Value type | Description
------------------------|------------|-------------------------------------------------------------------
Latitude                | float      | In the format of ddmm.mm (d refers to degrees, m refers to minutes). For example: 4807.038 = 48 degrees 7.038 minutes
Latitude in hemisphere  | char       | Latitude hemisphere `N` (northern hemisphere) or `S` (southern hemisphere)
Longitude               | float      | In the format of ddmm.mm (d refers to degrees, m refers to minutes). For example: 1131.001 = 11 degrees 31.001 minutes
Longitude in hemisphere | char       | hemisphere `E` (east longitude) or `W` (west longitude)

To make the file `/var/lib/anbox/static_gps_position` available to Android container, you can create a file that contains GPS data with the above format and move that file from `ADDON_DIR` to `/var/lib/anbox/static_gps_position` via an [addon install hook](https://discourse.ubuntu.com/t/managing-addons/17759#heading--build-your-own-addon) during its installation time. Then when Android container gets started and an application requests the current location information through Android framework, the GPS data will be forwarded from Anbox session to the application.


