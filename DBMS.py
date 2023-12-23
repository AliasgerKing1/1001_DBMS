import os
import pyautogui
import subprocess
import time
import re

import requests
import json


import random
import string

import csv
import keyboard
import shutil

from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.style import Style

def username_not_exists(username):
    with open(r'C:\Users\Aliasger B\1001_ai\1001_ai_python\Ai\DBMS\UserData.csv', "r") as userData:
        reader = csv.reader(userData)
        next(reader)  # Skip the header
        for row in reader:
            if row[0] == username:
                return False
    return True

def login_animation(console):
    with Progress() as progress:
        task = progress.add_task("[cyan]Logging in ...", total=100)

        for i in range(100):
            time.sleep(0.05)  # Simulate some work
            progress.update(task, advance=1)
        
        progress.stop()

    # Display Markdown-formatted text after the progress bar
    print("[bold green]Login SuccessFul.[/bold green]")

def get_non_empty_input(prompt):
                while True:
                    user_input = input(prompt)
                    if user_input.strip():  # Check if input is not empty after stripping whitespace
                        return user_input
                    else:
                        console.print("[bold red]Input cannot be empty. Please try again.[/bold red]")

def password_is_correct(username, password):
    with open(r'C:\Users\Aliasger B\1001_ai\1001_ai_python\Ai\DBMS\UserData.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        for row in reader:
            if username == row[0] and password == row[1]:  # Check if the username and password match
                return True
    return False

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(characters) for i in range(length))
    return result_str


def remove_extra_commas(input_string):
    # Replace consecutive commas and spaces with a single comma
    cleaned_string = re.sub(r',\s*,', ',', input_string)
    # Remove leading and trailing commas
    cleaned_string = cleaned_string.strip(',')
    return cleaned_string

def remove_extra_spaces(input_string):
    # Use a regular expression to replace multiple spaces with a single space
    cleaned_string = re.sub(r'\s+', ' ', input_string)
    return cleaned_string.strip()



outer_loop_flag = True  # Flag to control the outer loop
while outer_loop_flag :
        console = Console()
        console.print("[bold purple]1001 DBMS Login[/bold purple]")
        username = get_non_empty_input("Enter Username: ")
        
        if username_not_exists(username):
            console.print("[bold red]Username not exists.[/bold red]")
            time.sleep(1)
            continue

        password = get_non_empty_input("Enter Password: ")
        if not password_is_correct(username, password):
            console.print("[bold red]Incorrect password.[/bold red]")
            time.sleep(1)
            continue
        # login_animation(console)

        # time.sleep(3)

        os.system('cls' if os.name == 'nt' else 'clear')
        login_loop_flag = True # Flag to control the login loop
        console.rule("[bold yellow]Welcome to 1001![/bold yellow]", characters="=")
        while login_loop_flag :
            user_input = input('')
            if user_input == 'exit':
                console.print("[bold yellow]Exiting...[/bold yellow]")
                time.sleep(1)
                outer_loop_flag = False
                login_loop_flag = False
                os.system('cls' if os.name == 'nt' else 'clear')
            else :
                components_of_input = user_input.split('(', 1)
                command_and_object = components_of_input[0].split()
                if len(command_and_object) > 2 :
                    if command_and_object[0] == "select" and command_and_object[2].lower() == "from" :
                        # Find the indices of "select" and "from" in the list
                        select_index = command_and_object.index("select")
                        from_index = command_and_object.index("from")

                        # Extract the text between "select" and "from"
                        selected_text = command_and_object[select_index + 1:from_index]

                        # Remove commas from the string in the selected_text
                        selected_text = [word.replace(',', '') for word in selected_text]

                        # Append the modified selected_text as a list to result_list
                        result_list = [selected_text]

                        # Replace the text between "select" and "from" with the result_list
                        command_and_object[select_index + 1:from_index] = result_list
                if len(command_and_object) > 2 :
                    if command_and_object[0] == "delete" and command_and_object[1] == "row" :
                                            
                        # Find the indices of "row" and "from" in the list
                        row_index = command_and_object.index("row")
                        from_index = command_and_object.index("from")

                                        
                        # Extract the text between "row" and "from"
                        selected_text = command_and_object[row_index + 1:from_index]

                        # Remove commas after numbers in each string
                        modified_text = [re.sub(r'\b(\d+),\s*', r'\1', item) for item in selected_text]

                        # Initialize an empty list to store the final result
                        result_list = []

                        # Check if the number of digits is more than 2 in each modified string
                        for mod_item in modified_text:
                            check_length = len(re.findall(r'\d', mod_item))
                            if check_length > 1:
                                # Split each digit into a separate string
                                digit_strings = [digit for digit in re.findall(r'\d', mod_item)]
                                # Concatenate the arrays
                                result_list += digit_strings
                            else:
                                # If fewer than 2 digits, keep the original string
                                result_list.append(mod_item)

                        # Replace the text between "row" and "from" with the result_list
                        # print(result_list)
                        # Assuming result_list is a list of strings
                        modified_result_list = [item.replace(',', '') for item in result_list]

                        # Replace the text between "row" and "from" with the modified_result_list
                        command_and_object[row_index + 1:from_index] = [modified_result_list]

                        # Remove empty strings from the list
                        command_and_object = [item for item in command_and_object if item]

                        # print(command_and_object)

                
                command_name = command_and_object[0].lower()
                if command_name == 'create' :
                    what_to_create = command_and_object[1].lower()
                    if what_to_create == 'table' :
                        table_name = command_and_object[2]
                        primary_string = ''
                        foreign_string = ''

                        if "yramirp sa" and not "ngierof sa" in components_of_input[1][::-1] :
                            values_with_type = components_of_input[1][::-1].replace(")", "", 1)[::-1]

                            # Find the last occurrence of ")"
                            last_parenthesis_index = values_with_type.rfind(')')

                            # Split the string based on the last parenthesis
                            before_last_parenthesis = values_with_type[:last_parenthesis_index]
                            after_last_parenthesis = values_with_type[last_parenthesis_index + 1:]

                            # Append a closing parenthesis at the end
                            before_last_parenthesis += ')'
                            # print("Before last parenthesis:", before_last_parenthesis)
                            # print("After last parenthesis:", after_last_parenthesis)
                            values_with_type = before_last_parenthesis.split(',')
                            primary_string = after_last_parenthesis.replace("as", '').replace("primary", '').strip()
                            tempArray = []
                            for each_string_of_value_with_type in values_with_type :
                                cleaned_string_of_value_with_type = remove_extra_spaces(each_string_of_value_with_type)
                                # print("Original string:", each_string_of_value_with_type)
                                # print("String with single spaces:", cleaned_string_of_value_with_type)
                                tempArray.append(cleaned_string_of_value_with_type)
                            values_with_type = tempArray

                        elif "ngierof sa" and "yramirp sa" in components_of_input[1][::-1] :
                            values_with_type = components_of_input[1][::-1].replace(")", "", 1)[::-1]

                            # Find the last occurrence of ")"
                            last_parenthesis_index = values_with_type.rfind(')')

                            # Split the string based on the last parenthesis
                            before_last_parenthesis = values_with_type[:last_parenthesis_index]
                            after_last_parenthesis = values_with_type[last_parenthesis_index + 1:]

                            # Append a closing parenthesis at the end
                            before_last_parenthesis += ')'
                            # print("Before last parenthesis:", before_last_parenthesis)
                            # print("After last parenthesis:", after_last_parenthesis)

                            # Find the index of "primary" in the string
                            index_of_primary = after_last_parenthesis.find("primary")  
                            #  If "primary" is found, remove the text before and including "primary"
                            if index_of_primary != -1:
                                result_string = after_last_parenthesis[index_of_primary + len("primary"):].strip()

                                values_with_type = before_last_parenthesis.split(',')
                                foreign_string = result_string.replace("foreign", "").replace("as", "").strip()
                                tempArray = []
                                for each_string_of_value_with_type in values_with_type :
                                    cleaned_string_of_value_with_type = remove_extra_spaces(each_string_of_value_with_type)
                                    tempArray.append(cleaned_string_of_value_with_type)
                                values_with_type = tempArray
                                # Find the index of "primary" in the string
                            
                            index_of_primary = after_last_parenthesis.find("primary")

                            # If "primary" is found, remove everything after and including "primary"
                            if index_of_primary != -1:
                                result_string = after_last_parenthesis[:index_of_primary + len("primary")].strip()
                                
                                primary_string = result_string.replace("primary", "").replace("as", "").strip()


                            print(primary_string)

                        elif not "ngierof sa" and not "yramirp sa" in components_of_input[1][::-1] :
                            values_with_type = components_of_input[1][::-1].replace(")", "", 1)[::-1].split(',')
                            tempArray = []
                            for each_string_of_value_with_type in values_with_type :
                                cleaned_string_of_value_with_type = remove_extra_spaces(each_string_of_value_with_type)
                                # print("Original string:", each_string_of_value_with_type)
                                # print("String with single spaces:", cleaned_string_of_value_with_type)
                                tempArray.append(cleaned_string_of_value_with_type)
                            values_with_type = tempArray
                        elif "ngierof sa" and not "yramirp sa" in components_of_input[1] :
                            console.print(f"[bold red]Before adding foreign key, must have primary key[/bold red]")
                        else :
                            console.print(f"[bold cyan]Invalid syntax[/bold cyan]")
                        property_lst = []  # Initialize property_lst before the loop
                        for eachProperty in values_with_type:
                            new_each_property = eachProperty.split()
                            if len(new_each_property) == 2:
                                property_dict = {
                                    "name": new_each_property[0], 
                                    "type": new_each_property[1].split('(')[0].lower(),
                                    "count": new_each_property[1].split('(')[1].replace(')', ""),
                                    "PK:FK" : primary_string + ":" + foreign_string
                                }
                                property_lst.append(property_dict)  # Append property_dict to property_lst

                        json_object = {
                            "table_name": table_name,
                            "property_lst": property_lst,
                            "actual_data": []
                        }

                        json_data = json.dumps(json_object)
                        
                        response = requests.post('http://localhost:4015/api/dbms', data=json_data, headers={'Content-Type': 'application/json'})
                        # Convert the JSON string to a Python dictionary
                        json_dict = json.loads(response.text)
                        data = json_dict["data"]
                        if json_dict['status'] == 400 :
                                console.print(f"[bold red]Already a item made with name '{data}'[/bold red]")
                        else :
                            # Extract the 'data' property
                            returned_data = json_dict['data']
                            table = Table(title= f"Table '{returned_data['table_name']}' created")
                            table.add_column("name", style="white", justify="center")
                            table.add_column("type", style="magenta")
                            table.add_column("max length", style="yellow")
                            table.add_column("P/F key", style="cyan", justify="center")

                            for returned_property in returned_data['property_lst']:
                                pk_fk_value = returned_property['PK:FK']
                                name = returned_property['name']

                                if pk_fk_value == "":
                                    pk_fk_result = "-"
                                elif name == pk_fk_value.split(":")[0] and name != pk_fk_value.split(":")[1]:
                                    pk_fk_result = "PK"
                                elif name == pk_fk_value.split(":")[1] and name != pk_fk_value.split(":")[0]:
                                    pk_fk_result = "FK"
                                else:
                                    pk_fk_result = "-"

                                table.add_row(name, returned_property['type'], str(returned_property['count']), pk_fk_result)

                            # Print the table
                            console.print(table)
                elif command_name == 'insert' :
                    if command_and_object[1].lower() == 'into' :
                        insert_table_name = command_and_object[2]
                        insert_values = components_of_input[1][::-1].replace(")", "", 1)[::-1].split(',')
                        property_dict = {
                            "table_name": insert_table_name
                        }  # Initialize property_dict before the loop

                        for index, striped_insert_value in enumerate(insert_values):
                            striped_insert_value = striped_insert_value.strip()

                            # Check if the value can be converted to a number
                            try:
                                numeric_value = float(striped_insert_value)
                                property_dict[f"prop{index}"] = numeric_value
                            except ValueError:
                                # If conversion to float fails, treat it as a string
                                property_dict[f"prop{index}"] = striped_insert_value

                        json_data = json.dumps(property_dict)
                        # print(json_data)

                        response = requests.put('http://localhost:4015/api/dbms', data=json_data, headers={'Content-Type': 'application/json'})
                        # Convert the JSON string to a Python dictionary
                        json_dict = json.loads(response.text)
                        if json_dict['status'] == 400 :
                            error_msg = json_dict['msg']
                            console.print(f"[bold red]{error_msg}.[/bold red]")
                            time.sleep(1)
                        elif json_dict['status'] == 200:
                            success_msg = json_dict['msg']
                            insetedData = json_dict['insetedData']
                            propertiesArray = json_dict['propertiesArray']

                            # Convert properties with data type 'number' to strings
                            converted_dict = {key: str(value) if isinstance(value, (int, float)) else value for key, value in insetedData.items()}

                            # Print the result
                            # print(converted_dict)
                            console.print(f"[bold cyan]{success_msg}.[/bold cyan]")
                            table = Table(title=f"Data inserted")
                            # Define custom styles for each column
                            column_styles = [
                                Style(color="white"),
                                Style(color="green"),
                                Style(color="yellow"),
                                Style(color="cyan"),
                                Style(color="magenta"),
                                Style(color="purple"),
                            ]


                            # Add columns to the table with different column styles
                            for index, props_for_table in enumerate(propertiesArray):
                                column_style = column_styles[index % len(column_styles)]  # Use modulo to cycle through styles
                                table.add_column(props_for_table["name"], style=column_style, justify="center")

                            # Add rows to the table
                            for index in range(len(propertiesArray)):
                                row_data = [str(converted_dict[f"prop{index}"]) for index in range(len(propertiesArray))]
                                table.add_row(*row_data)

                            # Print the table
                            console.print(table)
                    else :
                        console.print(f"[bold cyan]Unknown identifier '{command_and_object[1].lower()}'[/bold cyan]")
                        console.print("[bold magenta]are you mean 'into'?[/bold magenta]")
                elif command_name == 'select' :
                    what_to_select = command_and_object[1]
                    if (what_to_select == "from" and not len(command_and_object) > 2) or (what_to_select == "from" and len(command_and_object) > 2) :
                        console.print(f"[bold cyan]Give valid column name[/bold cyan]")
                        console.print(f"[bold magenta]not clear which column to select[/bold magenta]")
                    else :
                        if len(command_and_object) > 2 and command_and_object[2].lower() == 'from' :
                            table_name_select = command_and_object[3].lower()
                            if what_to_select[0] == '*' :
                                what_to_select = "*"
                            select_data_dict = {
                                "table_name" : table_name_select,
                                "what_to_select" : what_to_select
                            }
                        
                            json_data = json.dumps(select_data_dict)

                            if type(what_to_select) == list and what_to_select != '*' :
                                response = requests.post('http://localhost:4015/api/dbms/data/lst', data=json_data, headers={'Content-Type': 'application/json'})
                                # Convert the JSON string to a Python dictionary
                                json_dict = json.loads(response.text)
                                # print(json_dict)
                                
                                data = json_dict['data']

                                # Create a single table
                                table = Table()

                                # Extract column names and add columns to the table
                                column_names = [dt['data']['matchedPropertyName'] for dt in data if isinstance(dt['data']['matchedPropertyName'], str)]
                                for column_name in column_names:
                                    table.add_column(column_name, style='white', justify="center")

                                # Add rows for each column in selectedData
                                max_rows = max(len(dt['data']['selectedData']) for dt in data)
                                for row_index in range(max_rows):
                                    row_data = []
                                    for dt in data:
                                        if row_index < len(dt['data']['selectedData']):
                                            row_data.append(str(dt['data']['selectedData'][row_index]))
                                        else:
                                            row_data.append("")  # Padding for rows with fewer items

                                    table.add_row(*row_data)

                                # Set the title dynamically based on the column names
                                table.title = f"Data Fetched from {', '.join(column_names)} column"

                                # Print the table
                                console.print(table)
                            else :
                                # print(json_data)
                                response = requests.post('http://localhost:4015/api/dbms/data', data=json_data, headers={'Content-Type': 'application/json'})
                                # Convert the JSON string to a Python dictionary
                                json_dict = json.loads(response.text)
                                data = json_dict['data']
                                if type(data) == str :
                                    console.print(f"[bold red]No table made with name '{data['table_name']}'[/bold red]")
                                else :
                                    if len(data['actual_data']) == 0 :
                                        console.print(f"[bold cyan]No data in '{data['table_name']}' table[/bold cyan]")
                                    else :
                                        if json_dict['status'] == 400 :
                                            console.print(f"[bold red]No item found with name '{data}'[/bold red]")
                                        else :
                                            # print(data['actual_data'])
                                            table = Table(title=f"Data Fetched")
                                            # Define custom styles for each column
                                            column_styles = [
                                                Style(color="white"),
                                                Style(color="green"),
                                                Style(color="yellow"),
                                                Style(color="cyan"),
                                                Style(color="magenta"),
                                                Style(color="purple"),
                                            ]


                                            # Add columns to the table with different column styles
                                            for index, props_for_table in enumerate(data["property_lst"]):
                                                column_style = column_styles[index % len(column_styles)]  # Use modulo to cycle through styles
                                                prop_name = props_for_table["name"]
                                                table.add_column(prop_name, style=column_style, justify="center")

                                            # Iterate over each object in actual_data and add rows for each column
                                            for actual_data_object in data["actual_data"]:
                                                row_data = []  # Collect data for each row
                                                for index, _ in enumerate(data["property_lst"]):
                                                    value = actual_data_object.get(f"prop{index}", "")
                                                    row_data.append(str(value))
                                                table.add_row(*row_data)


                                            # Print the table
                                            console.print(table)
                            
                        else :
                            if len(command_and_object) > 2 :
                                console.print(f"[bold cyan]Unknown identifier '{command_and_object[2].lower()}'[/bold cyan]")
                                console.print("[bold magenta]are you mean 'from'?[/bold magenta]")
                
                elif command_name == 'delete' :
                    what_to_delete = command_and_object[1]
                    if what_to_delete.lower().strip() == "table" :
                        which_table_to_delete = command_and_object[2]

                        table_to_delete_dict = {
                            "which_table_to_delete" : which_table_to_delete
                        }

                        json_data = json.dumps(table_to_delete_dict)
                        response = requests.post('http://localhost:4015/api/dbms/delete/table', data=json_data, headers={'Content-Type': 'application/json'})
                        # Convert the JSON string to a Python dictionary
                        json_dict = json.loads(response.text)
                        data = json_dict["data"]
                        console.print(f"[bold green]{data} table deleted successfully[/bold green]")
                    elif what_to_delete.lower().strip() == "row" :
                        which_row_to_delete = command_and_object[2]
                        if command_and_object[3] == 'from' :
                            from_which_table = command_and_object[4]
                            row_to_delete_dict = {
                            "which_row_to_delete" : which_row_to_delete,
                            "from_which_table" : from_which_table
                        }

                            json_data = json.dumps(row_to_delete_dict)
                            response = requests.post('http://localhost:4015/api/dbms/delete/row', data=json_data, headers={'Content-Type': 'application/json'})
                            # Convert the JSON string to a Python dictionary
                            json_dict = json.loads(response.text)
                            data = json_dict["data"][0]
                            property_array = data['property_lst']
                            actual_data = data['actual_data']
                            row_index = json_dict.get("row_index")
                            # Convert the list to a single string without brackets and quotes
                            result_string = ', '.join(row_index)
                                                        
                            # Remove square brackets and quotes from the string
                            row_index = result_string.replace('[', '').replace(']', '').replace('"', '')
                            result = remove_extra_commas(row_index)


                            # Create a table
                            table = Table(title=f"Row deleted")

                            # Define custom styles for each column
                            column_styles = [
                                Style(color="white"),
                                Style(color="green"),
                                Style(color="yellow"),
                                Style(color="cyan"),
                                Style(color="magenta"),
                                Style(color="purple"),
                            ]

                            # Add columns to the table with different column styles
                            for index, prop_info in enumerate(property_array):
                                column_style = column_styles[index % len(column_styles)]  # Use modulo to cycle through styles
                                table.add_column(prop_info["name"], style=column_style, justify="center")

                            # Add rows to the table
                            for idx, row_data in enumerate(actual_data, start=1):
                                table.add_row(*[str(row_data[f"prop{index}"]) for index in range(len(property_array))])

                            # # Convert row_index to ordinal number
                            # ordinal_row_index = f"{row_index}th" if 10 <= row_index % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(row_index % 10, "th")

                            # Print the table
                            console.print(table)

                            # Print the message with the ordinal row index
                            console.print(f"[bold green]'{data['table_name']}' table {result} row deleted successfully[/bold green]")
                            time.sleep(1)

                elif command_name == 'clear' :
                    what_to_clear = command_and_object[1]
                    if what_to_clear.lower().strip() == "table" :
                        which_table_to_clear = command_and_object[2]

                        table_to_clear_dict = {
                            "which_table_to_clear" : which_table_to_clear
                        }

                        json_data = json.dumps(table_to_clear_dict)
                        response = requests.post('http://localhost:4015/api/dbms/clear', data=json_data, headers={'Content-Type': 'application/json'})
                        # Convert the JSON string to a Python dictionary
                        json_dict = json.loads(response.text)
                        data = json_dict["data"]
                        console.print(f"[bold green]'{data}' table cleared successfully[/bold green]")
                else :
                    console.print(f"[bold cyan]Unknown command '{command_name}'[/bold cyan]")


