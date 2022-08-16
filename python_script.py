import requests
import json
import csv
import pandas as pd
from datetime import date, datetime


def vehicles_func(is_colored, *args):
    response = requests.get("https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active")
    data = response.text
    new_data = json.loads(data)
    fileinput_name = "output.csv"
    columns = ["rnr",
               "gruppe",
               "kurzname",
               "langtext",
               "info",
               "sort",
               "lagerort",
               "lteartikel",
               "businessUnit",
               "vondat",
               "bisdat",
               "hu",
               "asu",
               "createdOn",
               "editedOn",
               "fuelConsumption",
               "priceInformation",
               "safetyCheckDate",
               "tachographTestDate",
               "gb1",
               "ownerId",
               "userId",
               "externalId",
               "vin",
               "labelIds",
               "bleGroupEnum",
               "profilePictureUrl",
               "thumbPathUrl"]
    with open(fileinput_name, "w") as file:
        csv_file = csv.writer(file, lineterminator='\n')
        csv_file.writerow(columns)
        for item in list(new_data):
            csv_file.writerow(item.values())

    filename1 = r'C:\Users\penev\Documents\CV\Python task\vehicle.csv'
    filename2 = r'C:\Users\penev\Documents\CV\Python task\output.csv'
    df1 = pd.read_csv(open(filename1, 'r'), delimiter=',')
    df2 = pd.read_csv(open(filename2, 'r'), delimiter=',')
    df = df2.merge(df1, how='outer')
    rslt_df = df[df.hu.notnull()]
    sorted_df = rslt_df.sort_values(by='gruppe')
    sorted_df.to_excel("sorted.xlsx")
    columns_to_show = ['rnr', 'gruppe']
    columns_to_add= list(*args)
    columns_to_show.extend(columns_to_add)
    result_df = sorted_df[columns_to_show].set_index('rnr')

    def highlight_greaterthan(s):
        current_month= date.today().month
        if current_month- s['hu'].month <3:
            return ['background-color: green'] * 5
        elif current_month - s['hu'].month < 12:
            return ['background-color: orange'] * 5
        else:
            return ['background-color: red'] * 5
    if is_colored:
        result_df.style.apply(highlight_greaterthan, axis=1)

    iso_date = datetime.now().strftime("%Y%m%d-%H%M%S")

    output_file=f"vehicles_{iso_date}.xlsx"
    result_df.to_excel(output_file)

    print(result_df)


colored = input()
keys = input().split(', ')

#
vehicles_func(colored, keys)
