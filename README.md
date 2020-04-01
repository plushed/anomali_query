# Anomali Query

Query Anomali data for values and indicators.

## Requirements

This script is coded for Python 3

The config file default is ./conf/example.conf and must contain the username and API key for the Anomali query.  If a proxy is present, the proxy information and credentials can be appended to the config file as well.

The tool is broken into 3 sections currently

## Search Methods
  a. The search methods are broken apart into values and tags.  Values are an API call that queries against the value field of the keyworks presented either using the --keyword argument or the default of querying against the --infile or -f. 
  
  b. Tags can be queried against a list of keywords as well but instead of pulling results of values they pull results of tags. The tags allow for a wider breath of search if indicators are being tagged to a particular attribute such as campaigns, bulletins or malware

## Input / Output

  a. Input defaults to a list ./inputs.txt but keywords can also be used using a comma seperated list in the command line. 
  Example: python anomali_search.py -c -v -k example.com
  
  b. Outputs default to ./results.csv and will be overwritten each time the command is executed. Specific outputs can be specified using the -o or --outfile command. 

## Filtering

  a. The limit of results returned can be specified using the -l --limit argument. This defaults to no limit. 
  
  b. The indicator status defaults to "all" but can be filtered for the types, active, inactive, and falsepos. 
  
## Usage

```
                                   _ _                           _     
   __ _ _ __   ___  _ __ ___   __ _| (_)  ___  ___  __ _ _ __ ___| |__  
  / _` | '_ \ / _ \| '_ ` _ \ / _` | | | / __|/ _ \/ _` | '__/ __| '_ \ 
 | (_| | | | | (_) | | | | | | (_| | | | \__ \  __/ (_| | | | (__| | | |
  \__,_|_| |_|\___/|_| |_| |_|\__,_|_|_| |___/\___|\__,_|_|  \___|_| |_|  

**********************Anomali Intel Search -v0.1**************************

        -h --help       Prints this help
        -c --config     Required parameter. Specify config, otherwise uses example.conf
        
        --------------------------Input Output----------------------------
        -f --infile     Search a list of keywords or IOCs in a file
        -k --keyword    Specify the keyword you wish to search if a list is not used
        -o --outfile    Specify the output file, otherwise output to results.csv
        
        --------------------------Search Methods----------------------------
        -v --value      Search specific keywords or IOCs     
        -t --tag        Search tags instead of specific values
        -w --w          Searches values as wildcards rather than an exact search
        
        --------------------------Filtering----------------------------
        -l --limit      Specify the max results you wish to return. Default is no limit
        -s --status     Options are active, inactive and falsepos. Default is all
        
        Example: python anomali_search.py -c -k example.com -s active -w -l 10000 -o results.csv
        Example: python anomali_search.py -c -v -w
        
usage: anomali_search.py [-h] [-f F] [-k [K]] -c [C] [-o [O]] [-w] [-l L]
                         [-s {active,inactive,falsepos,}] (-v | -t)
```
