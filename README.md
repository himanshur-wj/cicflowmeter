# Python CICFlowMeter

> This project is not maintained actively by me. If you found something wrong (bugs, incorrect results) feel free to create issues or pull requests.

### Installation

```sh
git clone https://github.com/hieulw/cicflowmeter
cd cicflowmeter
poetry install
```

### Usage

```sh
usage: cicflowmeter [-h] (-i INPUT_INTERFACE | -f INPUT_FILE) [-c] [-v] output

positional arguments:
  output                output file name (in flow mode) or directory (in sequence mode)

options:
  -h, --help            show this help message and exit
  -i INPUT_INTERFACE    capture online data from INPUT_INTERFACE
  -f INPUT_FILE         capture offline data from INPUT_FILE
  -c, --csv             output flows as csv
  -v, --verbose         more verbosity
  -t INPUT_NTERVAL      time in seconds
  -fn FILE_NAME         pass this argument if you want to save the file name  as datatime.csv
```


Convert pcap file to flow csv:

#### The below command will convert the given pcap file into /path/flow.csv
```
cicflowmeter -f example.pcap -c flows.csv 
```

#### The below command will convert the given pcap file into /path/`datatime.csv` irrespective of the given filename
```
cicflowmeter -f example.pcap -c flows.csv -fn
```

Sniff packets real-time from interface to flow csv: (**need root permission**)

#### The below command will capture the real-time traffic and saves in specified path
```
cicflowmeter -i eth0 -c flows.csv
```

#### Example: If you wnat to capture the network traffic for 1 minites (60 seconds)
```
cicflowmeter -i eth0 -c flows.csv -t 60
```

### References:

1. https://www.unb.ca/cic/research/applications.html#CICFlowMeter
2. https://github.com/ahlashkari/CICFlowMeter
