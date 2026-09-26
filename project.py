import csv
import re
import json
from tabulate import tabulate
import argparse

def read_flight_data(log_file):

    with open(log_file) as file:
        reader=csv.DictReader(file)
        for row in reader:
            yield row

def is_valid(timestamp):
    if re.search(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",timestamp):
        return True
    return False

def detect_anomalies(data_generator,max_speed,min_altitude):
    anomalies=[]
    for row in data_generator:
        if not is_valid(row["timestamp"]):
            row["error_type"]="Invalid timestamp"
            anomalies.append(row)
            continue
        try:
            speed=int(row["speed"])
            altitude=int(row["altitude"])
            if speed>max_speed or altitude<min_altitude:
                row["error_type"]="Rule Violation"
                anomalies.append(row)
        except ValueError:
            row["error_type"]="Invalid sensor data"
            anomalies.append(row)
    return anomalies


def generate_report(anomalies):
    print("\nSECURITY REPORT")
    if len(anomalies)==0:
        print("All values are nominal.")
    else:
        print(f"WARNING! {len(anomalies)} rule violations detected.")
        data=[]
        for anomaly in anomalies:
            data.append([anomaly.get("timestamp","N/A"),anomaly.get("speed","N/A"),anomaly.get("altitude","N/A"),anomaly.get("error_type","N/A")])
        headers=["Time","Speed","Altitude","Error Type"]
        print(tabulate(data,headers,tablefmt="grid"))

def convert_json(anomalies,output_file):
    if len(anomalies)>0:
           with open(output_file,"w") as file:
               json.dump(anomalies,file,indent=4)
           print(f"Detailed anomaly report:{output_file}")



def main():
    parser=argparse.ArgumentParser(description="Detects anomalies in flight logs.")
    parser.add_argument("-f","--file",default="flight_data.csv",help="for read to Flight log CSV file.")
    parser.add_argument("-s","--speed",type=int,default=200,help="Max speed limit.")
    parser.add_argument("-a","--altitude",type=int,default=1000,help="Min altitude limit")
    parser.add_argument("-o","--output",default="anomalies_report.json",help="JSON output file.")
    args=parser.parse_args()
    flight_data=read_flight_data(args.file)
    anomalies=detect_anomalies(flight_data,max_speed=args.speed,min_altitude=args.altitude)
    generate_report(anomalies)
    convert_json(anomalies, args.output)


if __name__=="__main__":
    main()
