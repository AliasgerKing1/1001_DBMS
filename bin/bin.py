
                            # else :
                            #     # print(data['actual_data'])
                            #     table = Table(title=f"Data Fetched")
                            #     # Define custom styles for each column
                            #     column_styles = [
                            #         Style(color="white"),
                            #         Style(color="green"),
                            #         Style(color="yellow"),
                            #         Style(color="cyan"),
                            #         Style(color="magenta"),
                            #         Style(color="purple"),
                            #     ]


                            #     # Add columns to the table with different column styles
                            #     for index, props_for_table in enumerate(data["property_lst"]):
                            #         column_style = column_styles[index % len(column_styles)]  # Use modulo to cycle through styles
                            #         prop_name = props_for_table["name"]
                            #         table.add_column(prop_name, style=column_style, justify="center")

                            #     # Iterate over each object in actual_data and add rows for each column
                            #     for actual_data_object in data["actual_data"]:
                            #         row_data = []  # Collect data for each row
                            #         for index, _ in enumerate(data["property_lst"]):
                            #             value = actual_data_object.get(f"prop{index}", "")
                            #             row_data.append(value)
                            #         table.add_row(*row_data)


                            #     # Print the table
                            #     console.print(table)
                            #     time.sleep(2)

                         


# else :
                            #     print("no")

                            #     row_to_delete_dict = {
                            #     "which_row_to_delete" : int(which_row_to_delete),
                            #     "from_which_table" : from_which_table
                            # }

                            #     json_data = json.dumps(row_to_delete_dict)
                            #     response = requests.post('http://localhost:4015/api/dbms/delete/row', data=json_data, headers={'Content-Type': 'application/json'})
                            #     # Convert the JSON string to a Python dictionary
                            #     json_dict = json.loads(response.text)
                            #     data = json_dict["data"][0]
                            #     property_array = data['property_lst']
                            #     actual_data = data['actual_data']
                            #     row_index = json_dict.get("row_index")

                            #     # Create a table
                            #     table = Table(title=f"Data inserted")

                            #     # Define custom styles for each column
                            #     column_styles = [
                            #         Style(color="white"),
                            #         Style(color="green"),
                            #         Style(color="yellow"),
                            #         Style(color="cyan"),
                            #         Style(color="magenta"),
                            #         Style(color="purple"),
                            #     ]

                            #     # Add columns to the table with different column styles
                            #     for index, prop_info in enumerate(property_array):
                            #         column_style = column_styles[index % len(column_styles)]  # Use modulo to cycle through styles
                            #         table.add_column(prop_info["name"], style=column_style, justify="center")

                            #     # Add rows to the table
                            #     for idx, row_data in enumerate(actual_data, start=1):
                            #         table.add_row(*[str(row_data[f"prop{index}"]) for index in range(len(property_array))])

                            #     # Convert row_index to ordinal number
                            #     ordinal_row_index = f"{row_index}th" if 10 <= row_index % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(row_index % 10, "th")

                            #     # Print the table
                            #     console.print(table)

                            #     # Print the message with the ordinal row index
                            #     console.print(f"[bold green]'{data['table_name']}' table {row_index}{ordinal_row_index} row deleted successfully[/bold green]")
                            #     time.sleep(1)



                            # .split(')', -1)[0].split(',')
                            # Find the last occurrence of ")"

                            # primary_string = components_of_input[1][::-1].replace(")", "", 1)[::-1].split(')')[1].strip()



                            # else:
                            #     print("The word 'primary' is not found in the string.")



                            # else:
                            #     result_string = after_last_parenthesis.strip()
                            #     primary_string = result_string