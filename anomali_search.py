
import argparse
import sys
import requests
import csv
import configparser
import os.path
VERSION = "0.1"


# Banner
def banner():
    banner = '''
                                    _ _                           _     
   __ _ _ __   ___  _ __ ___   __ _| (_)  ___  ___  __ _ _ __ ___| |__  
  / _` | '_ \ / _ \| '_ ` _ \ / _` | | | / __|/ _ \/ _` | '__/ __| '_ \ 
 | (_| | | | | (_) | | | | | | (_| | | | \__ \  __/ (_| | | | (__| | | |
  \__,_|_| |_|\___/|_| |_| |_|\__,_|_|_| |___/\___|\__,_|_|  \___|_| |_|  
'''
    print(banner)
    print("**********************Anomali Intel Search -v" + VERSION + "**************************")
    # Usage

def usage():
        usage = """
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
        """
        print(usage)
        sys.exit

# Start

#####################################
        # Anomali Search #
#####################################
def anomali_search():
    outfile = args.o
    infile = args.f
    limit = args.l
    status = args.s
    conf = args.c

    # Config file function call
    if os.path.exists(args.c):
        # Config file processing & analysis
        try:
            config = configparser.ConfigParser()
            config.read(conf)
            # config.sections()
            anomali_api = config.get('ANOMALI', 'api_key')
            anomali_user = config.get('ANOMALI', 'user')
            anomali_url = config.get('ANOMALI', 'api_url')
            proxy = config.get('PROXY', 'proxy')
            proxy_user = config.get('PROXY', 'username')
            proxy_password = config.get('PROXY', 'password')
            proxy_creds = proxy_user + ':' + proxy_password
        except:
            sys.exc_info()
    else:
        print("No such file '{}'".format(conf), file=sys.stderr)
        exit()

    if args.k:
        try:
            # If more than one search word
            if ',' in args.k:
                ioc_list = [args.k.strip(' ') for args.k in args.k.split(',')]
            else:
                ioc_list = [args.k]
        except:
            sys.exc_info()
    else:
        ioc_list = open(infile, "r")
        
    if os.path.exists(outfile):
        os.remove(outfile)

    with open(outfile, 'w', newline='', encoding="utf-8") as data_file:
        writer = csv.writer(data_file)
        ## Write headers
        header = 'value', 'confidence', 'itype', 'source', 'date_modified', 'status', 'tags'
        writer.writerow(header)

        for item in ioc_list:
            # Define search string based on type
            if args.w:
                search_string = "&value__regexp=.*." + item + "*"
            elif args.t:
                search_string = "&tag="
            else:
                search_string = "&value="
            try:
                url = requests.get(
                anomali_url + "api_key=" + anomali_api + "&username=" + anomali_user + search_string + item + "&limit=" + str(
                limit) + "&status=" + status)
                with url as result:
                    if result.status_code == 200:
                        data = result.json()
                        if not data['objects']:  # If no records located - print message, increment not found and add to not found list
                            print("\n" + "-" * 50)
                            print("[!] No Records Located for " + item)
                            print("-" * 50)
                            writer.writerow([item,'','','','','No Results'])
                        else:
                            for obj in data['objects']:
                                writer.writerow(
                                [obj['value'], obj['confidence'], obj['itype'], obj['source'], obj['modified_ts'],
                                obj['status'],obj['tags']])
                                item = item.replace("http", "hxxp")
                                print("\n" + "-" * 50)
                                print("[!] Records located for " + item)
                                print("-" * 50)
                    else:
                        print(
                            "-------------Failed to connect - check API config info or that site is up----------------")
            except SystemError:
                print("Failed to query.")
    print("-------------Results returned in " + outfile + "----------------")

if __name__ == '__main__':
    banner()
    usage()
    parser = argparse.ArgumentParser()
    group_creation = parser.add_argument_group('Arguments')

    group_creation.add_argument('-f', '--list', help='List file with values to search - defaults to input.txt',default='./input.txt', dest="f")
    group_creation.add_argument('-k', '--keyword', help='Keyword search if list is not used', nargs='?', dest="k")
    group_creation.add_argument('-c', '--config', help='Config File', nargs='?', const='./conf/example.conf', required=True, dest="c")
    group_creation.add_argument('-o', '--outfile', help='Output File - defaults to results.csv', nargs='?',default='./results.csv', dest="o")
    group_creation.add_argument('-w', '--w', help='Use wildcard search for a more comprehensive search.  If not specified the search will query for the exact value(s)', action='store_true', dest="w")
    group_creation.add_argument('-l', '--limit', help='Specify the max results you wish to return. Default is no limit.', default='0',dest="l", type=int)
    group_creation.add_argument('-s', '--status',help='Return only certain indicators. Options are active, inactive and falsepos. Default is all.',choices=['active', 'inactive', 'falsepos', ''], default='', dest="s")
    search_type = parser.add_mutually_exclusive_group(required=True)
    search_type.add_argument('-v', '--value', help='Search value specified', action='store_true', dest="v")
    search_type.add_argument('-t', '--tag', help='Search tags', action='store_true', dest="t")
    args = parser.parse_args()
    anomali_search()

