# yalngg
yet-another-lldp-network-graph-generator


Set your switch password (SONiC basic Auth in this code):

```sh
export SW_ADMIN=admin
export SW_PASS=adminP@ss
```

Create your input switch document, switches.csv

```csv
hostname,swithcip
leaf1,10.1.1.100
leaf2,10.1.1.101
spine1,10.1.2.100
spine2,10.1.2.101
storleaf1,10.1.3.100
storleaf2,10.1.3.101
```
