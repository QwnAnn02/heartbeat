import pandas as pd
from jinja2 import Template
from functions import check_input_file_existence,validate_field_names, check_mandatory_fields , fix_trailing_spaces, validate_ip_addresses
from yaml_template import yaml_template
from datetime import datetime
import os

def main():
    # Read Excel data into a Pandas DataFrame
    input_excel = 'config_generator/heartbeat_config_INPUT_template.xlsx' 
    # Check if the input file exists
    check_input_file_existence(input_excel)
    df = pd.read_excel(input_excel, engine='openpyxl', index_col=None)
    
    # Validate field names
    validate_field_names(df)

    # Check for mandatory fields
    check_mandatory_fields(df)


    # Fix trailing spaces
    df = fix_trailing_spaces(df)

    # Validate IP address format
    validate_ip_addresses(df)

    now = datetime.now()

    # Create Jinja2 template object
    template = Template(yaml_template)

    # Render YAML data
    yaml_data = template.render(data=df)

    # Save YAML data to a file
    yaml_file = 'heartbeat yaml config file.yaml'
    with open(yaml_file, 'w') as f:
       f.write(yaml_data)

    print(f"YAML data has been successfully written to {yaml_file}.")

    # Append data to Master Excel sheet
    master_excel_file = 'heartbeat_gen_master_data.xlsx'
    if os.path.exists(master_excel_file):
        master_df = pd.read_excel(master_excel_file, engine='openpyxl', index_col=None) 
        # Append the new data to the master data
        master_df = pd.concat([master_df, df], ignore_index=True)
    else:
        # If master Excel file doesn't exist, create a new one
        master_df = df.copy()

    # Add a date column with the current date
    master_df['date'] = now.strftime('%d-%m-%y')
    master_df['time'] = now.strftime('%H:%M:%S')

    # Save the updated master data
    master_df.to_excel(master_excel_file, index=False, engine='openpyxl')

    # Delete the input Excel file
    #os.remove(input_excel)
    


     
    print(f"Data has been successfully appended to {master_excel_file} and input Excel sheet has been cleared.")

if __name__ == "__main__":
    main()