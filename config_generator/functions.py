import pandas as pd
import os
import re
import sys 

#check if the input file exists.
def check_input_file_existence(input_excel):
    if not os.path.exists(input_excel):
        raise FileNotFoundError(f"Input file '{input_excel}' not found. Please provide a valid input file.")

#validate the input field names.
def validate_field_names(df):
    expected_columns = ['type', 'id', 'name','hosts', 'ipv4', 'ipv6',
                         'city name', 'country iso code', 'country name',
                         'latitude', 'longitude', 'geo.name',
                         'location id', 'site id', 'site name',
                         'site uid', 'site category', 'cmbd ci name',
                         'cmdb ci uid', 'cmdb ci parent name', 'cmdb ci parent uid',
                         'cmdb event category','mode', 'timeout', 'wait', 'tags'
                         ]
    try:

        for column in expected_columns:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' is missing!.")   

        unexpected_columns = set(df.columns) - set(expected_columns)
        if unexpected_columns:
            raise ValueError(f"Unexpected columns present: {', '.join(unexpected_columns)}") #re-direct for input correction?
    except ValueError as ve:
        print(f"Error in field names: {ve}")
        sys.exit(1)

#check if mandatory fields are present
def check_mandatory_fields(df):
    mandatory_fields = ['type', 'id', 'name','hosts']
    try:

        for field in mandatory_fields:
            if df[field].isnull().any():
                raise ValueError(f"Mandatory field '{field}' contains null values.") #re-direct for input correction and append it in the excel sheet or should the user go back to the excel sheet?
    except ValueError as ve:
        print(f"Mandatory field(s) missing : {ve}")
        sys.exit(1)

#strip any trailing spaces
def fix_trailing_spaces(df):
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return df

#validate IP address and check for duplicates
def validate_ip_addresses(df, master_df=None):
    ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    ipv6_pattern = re.compile(r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$')

    # a set to keep track of unique IP addresses in the current sheet
    unique_ips = set()

    try:
        for _, row in df.iterrows():
            for host in row['hosts'].split(', '):
                if not ipv4_pattern.match(host) and not ipv6_pattern.match(host):
                    raise ValueError(f"Invalid IP address format for host '{host}' in row {row.name}")

                # Check for duplicate IP addresses in the current sheet
                if host in unique_ips:
                    raise ValueError(f"Duplicate IP address '{host}' found in row {row.name}")

                # Add the IP address to the set
                unique_ips.add(host)

                # Check for duplicate IP addresses in the master sheet
                if master_df is not None and host in master_df['hosts'].str.split(', ').sum(): #concatenates a list of all IPs
                    raise ValueError(f"Duplicate IP address '{host}' found in the master sheet")

    except ValueError as ve:
        print(f"Error in IP address format or duplicate entries: {ve}")
        sys.exit(1)