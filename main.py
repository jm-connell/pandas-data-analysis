import pandas as pd
import calendar
from datetime import datetime


def get_input():
    """
    Function to get user input for data type and danger level.

    Returns:
        data_type (str): The type of data the user wants to see. Can be '1', '2', '3', '4', '5', or '6'.
        danger_level (str): The level of danger the user wants to see. Can be '1' or '2'.
    """

    while True:
        # Loop until valid input is received

        # Get desired data type from user
        while True:
            print("\nWhat data would you like to see?\n1. Day of Week\n2. Month\n3. Time\n4. Borough\n5. Zip Code\n6. Vehicle Type\n")
            data_type = input(">> ")

            # Check if input is valid
            if data_type in ['1', '2', '3', '4', '5', '6']:
                break
            else:  
                print("\nPlease enter a number between 1 and 6")

        # Get desired danger level from user
        while True:
            print("\nWould you like to see the most safe or most dangerous?\n1. Most Safe\n2. Dangerous\n")
            danger_level = input(">> ") 

            # Check if input is valid
            if danger_level in ['1', '2']:
                break
            else:
                print("\nPlease enter 1 or 2")

        # If both inputs are valid, break the outer loop
        break

    # Return the user input
    return data_type, danger_level

def get_data(data, data_type, danger_level):
    """
    Function to process the data based on user input and return the result.

    Parameters:
        data (DataFrame): The data to process.
        data_type (str): The type of data the user wants to see. Can be '1', '2', '3', '4', '5', or '6'.
        danger_level (str): The level of danger the user wants to see. Can be '1' or '2'.

    Returns:
        result (str): The result of the data processing.
    """

    # Convert danger_level to corresponding aggregation function
    agg_func = 'idxmin' if danger_level == '1' else 'idxmax'

    if data_type == '1':
        # If data type is 'Day of Week', group by day of week and count collisions
        day_of_week = data.groupby(data['CRASH DATE'].dt.dayofweek)['COLLISION_ID'].count().agg(agg_func)
        result = calendar.day_name[day_of_week]
    elif data_type == '2':
        # If data type is 'Month', group by month and count collisions
        month = data.groupby(data['CRASH DATE'].dt.month)['COLLISION_ID'].count().agg(agg_func)
        result = calendar.month_name[month]
    elif data_type == '3':
        # If data type is 'Time', group by time and count collisions
        time = data.groupby(data['CRASH TIME'])['COLLISION_ID'].count().agg(agg_func)
        result = (datetime.min + time).time().strftime('%H:%M')
    elif data_type == '4':
        # If data type is 'Borough', group by borough and count collisions
        result = data.groupby('BOROUGH')['COLLISION_ID'].count().agg(agg_func)
    elif data_type == '5':
        # If data type is 'Zip Code', clean the data, then group by zip code and count collisions
        data['ZIP CODE'] = pd.to_numeric(data['ZIP CODE'], errors='coerce').fillna(0).astype(int)
        result = data[data['ZIP CODE'] != 0].groupby('ZIP CODE')['COLLISION_ID'].count().agg(agg_func)
    elif data_type == '6':
        # If data type is 'Vehicle Type', filter the data, then group by vehicle type and count collisions
        vehicle_counts = data['VEHICLE TYPE CODE 1'].value_counts()
        common_vehicles = vehicle_counts[vehicle_counts >= 100].index
        result = data[data['VEHICLE TYPE CODE 1'].isin(common_vehicles)].groupby('VEHICLE TYPE CODE 1')['COLLISION_ID'].count().agg(agg_func)

    # Return the result
    return result

def main():
    """
    Main function to load the data, get user input, process the data, and print the result.
    """

    # Define dictionaries to map user input to data types and danger levels
    data_type_dict = {'1': 'Day of Week', '2': 'Month', '3': 'Time', '4': 'Borough', '5': 'Zip Code', '6': 'Vehicle Type'}
    danger_level_dict = {'1': 'Most Safe', '2': 'Most Dangerous'}

    try:
        # Load the CSV file into a pandas DataFrame
        data = pd.read_csv('collisions.csv')

        # Convert 'CRASH DATE' to datetime format
        data['CRASH DATE'] = pd.to_datetime(data['CRASH DATE'], infer_datetime_format=True)

        # Convert 'CRASH TIME' to timedelta format
        data['CRASH TIME'] = pd.to_timedelta(data['CRASH TIME'] + ':00')

        # Get user input for data type and danger level
        data_type, danger_level = get_input()

        # Process the data based on user input and get the result
        result = get_data(data, data_type, danger_level)

        # Print the result
        print(f'\nThe {danger_level_dict[danger_level].lower()} {data_type_dict[data_type].lower()} is {result}\n')
    except FileNotFoundError:
        # Handle the case where the CSV file is not found
        print("The file 'collisions.csv' was not found.")
    except pd.errors.EmptyDataError:
        # Handle the case where the CSV file is empty
        print("No data was found in the file.")
    except Exception as e:
        # Handle any other exceptions that might occur
        print(f"An error occurred: {e}")


main()