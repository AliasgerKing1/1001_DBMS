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


outer_loop_flag = True  # Flag to control the outer loop
while outer_loop_flag :
        console = Console()
        console.print("[bold purple]1001 DBMS Login[/bold purple]")
        username = get_non_empty_input("Enter Username: ")
        
        if username_not_exists(username):
            console.print("[bold red]Username not exists.[/bold red]")
            time.sleep(2)
            continue

        password = get_non_empty_input("Enter Password: ")
        if not password_is_correct(username, password):
            console.print("[bold red]Incorrect password.[/bold red]")
            time.sleep(2)
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
                command_name = command_and_object[0].lower()
                if command_name == 'create' :
                    what_to_create = command_and_object[1].lower()
                    if what_to_create == 'table' :
                        table_name = command_and_object[2]
                        values_with_type = components_of_input[1][::-1].replace(")", "", 1)[::-1].split(',')
                        property_lst = []  # Initialize property_lst before the loop
                        for eachProperty in values_with_type:
                            new_each_property = eachProperty.split()
                            if len(new_each_property) == 2:
                                property_dict = {
                                    "name": new_each_property[0], 
                                    "type": new_each_property[1].split('(')[0].lower(),
                                    "count": new_each_property[1].split('(')[1].replace(')', "")
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

                        # Extract the 'data' property
                        returned_data = json_dict['data']
                        table = Table(title= f"Table '{returned_data['table_name']}' created")
                        table.add_column("name", style="white", justify="center")
                        table.add_column("type", style="magenta")
                        table.add_column("max length", style="yellow", justify="center")

                        for returned_property in returned_data['property_lst'] :
                            table.add_row(returned_property['name'], returned_property['type'], str(returned_property['count']))
                        # Print the table
                        console.print(table)
                        # print(response.text)
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
                            time.sleep(2)
                        elif json_dict['status'] == 200:
                            success_msg = json_dict['msg']
                            insetedData = json_dict['insetedData']
                            propertiesArray = json_dict['propertiesArray']

                            # Convert properties with data type 'number' to strings
                            converted_dict = {key: str(value) if isinstance(value, (int, float)) else value for key, value in insetedData.items()}

                            # Print the result
                            print(converted_dict)
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
                            time.sleep(2)
                elif command_name == 'select' :
                    what_to_select = command_and_object[1]
                    if command_and_object[2].lower() == 'from' :
                        table_name_select = command_and_object[3].lower()
                        select_data_dict = {
                            "table_name" : table_name_select,
                            
                        }


