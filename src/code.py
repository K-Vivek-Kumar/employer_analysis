# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Import custom functions from src.funcs
from src.funcs import worked_for_7_days, less_than_10_hours_between_shifts, more_than_14_hours_in_a_shift
from src.funcs import convert_to_timedelta

# Define input, output, and image paths
input_path = '../Assignment_Timecard.xlsx - Sheet1.csv'
output_path = '../output.txt'
output_image_path = '../output_graph.png'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_path)

# Convert 'Time' and 'Time Out' columns to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M %p')
df['Time Out'] = pd.to_datetime(df['Time Out'], format='%m/%d/%Y %I:%M %p')

# Convert 'Timecard Hours (as Time)' to timedelta format
df['Timecard Hours (as Time)'] = df['Timecard Hours (as Time)'].apply(convert_to_timedelta)

# Group data by 'Employee Name'
grouped_data = df.groupby('Employee Name')

# Write analysis results to the output file
with open(output_path, 'w') as output_file:
    output_file.write("Has Worked for 7 consecutive days:\n")
    for name, group in grouped_data:
        if worked_for_7_days(group):
            output_file.write(f"\t{name}\n")

    output_file.write("\nHas Less Than 10 hours but greater than 1 hour between shifts:\n")
    for name, group in grouped_data:
        if less_than_10_hours_between_shifts(group):
            output_file.write(f"\t{name}\n")

    output_file.write("\nHas worked for more than 14 hours in a single shift:\n")
    for name, group in grouped_data:
        if more_than_14_hours_in_a_shift(group):
            output_file.write(f"\t{name}\n")

# Resetting index before plotting the bar chart
total_hours = df.groupby('Employee Name')['Timecard Hours (as Time)'].sum()
total_hours = total_hours.reset_index()

# Plot a bar chart of total hours worked by each employee
plt.figure(figsize=(10, 6))
plt.bar(total_hours['Employee Name'], total_hours['Timecard Hours (as Time)'], color='green')
plt.title('Total Hours Worked by Each Employee')
plt.ylabel('Total Hours Worked')
plt.xticks(rotation=45, ha='right', fontsize=4)
plt.savefig(output_image_path, bbox_inches='tight')
