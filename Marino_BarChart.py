"""
Kimberly Stochaj - stochaj.k@northeastern.edu
2023 IISE Technical Project
Makes a chart of foercasted business at Marino based on historical data - 
hopefully for eventual website implementation
April 2023
Marino_BarChart.py
"""

# import libraries and intialize constants
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from collections import defaultdict

ARRIVAL_DATA = "MarinoAccessLog.csv"
# The number of days to consider in making the forcast - False if all historical data should be used
HISTORYRANGE_DAYS = 50
DOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
       "Sunday"]
DESIRED_DOW = ["Monday"]

def str_to_datetime(date_str):
    """ convert strings in the format M/D/YYYY H:MM:SS AM/PM to datetime objects
        
        Args: 
            date_str (str): the string to convert to a datetime object
        
        Returns: 
            my_datetime (datetime): the datetime object that 
    """
    # seperate the string containing the date into its parts and convert type
    dt_lst = date_str.split()
    
    day_info = dt_lst[0].split("/")
    day_info = [int(i) for i in day_info]
    
    time_info = dt_lst[1].split(":")
    time_info = [int(i) for i in time_info]
    
    # converts 12 hour to 24 hour time
    if dt_lst[2] == "PM" and time_info[0] != 12:
        time_info[0] += 12
    
    # create datetime object
    my_datetime = datetime(day_info[2], day_info[0], day_info[1], time_info[0],
                           time_info[1], time_info[2])
    return my_datetime


def plot_hist(hour_lst, day_of_week, scale):
    """ create a histogram from a list of ints
        
        Args:
            hour_lst (lst of ints): hours representing histogram bins
            day_of_week (str): weekday that the data coresponds to - used in 
                the plot title
            scale (int): the number of a given day of the week included by the data
            
        Returns:
            none
    """
    counts, bins = np.histogram(hour_lst, bins = np.unique(hour_lst))
    counts = np.divide(counts, scale)
    bins = bins[0 : -1]
    
    if day_of_week in DESIRED_DOW:
        plt.bar(bins, counts)
    
        plt.xlabel("check-in hour (24 hour time)")
        plt.ylabel("# check-ins per hour")
        plt.xticks(bins)
        plt.ylim(0, 350)
    
        if HISTORYRANGE_DAYS == False:
            plt.title(f"Forcasted Marino useage for {day_of_week}")
        else:
            plt.title(f"Forcasted Marino useage for {day_of_week} (based on {HISTORYRANGE_DAYS} past days)")
    
    plt.show()


def main():
    df_arrivals = pd.read_csv(ARRIVAL_DATA)
    
    # add column for datetime object
    df_arrivals["datetime"] = ''
    for idx, row in df_arrivals.iterrows():
        row["datetime"] = str_to_datetime(row["Date Time"])
    
    if HISTORYRANGE_DAYS != False: 
        # get the time of the earliest entry for calculations (HISTORYRANGE_DAYS days ago)
        now = datetime.now()
        beginning = now - timedelta(days = HISTORYRANGE_DAYS)
        
        # keep only the data that falls within the desired period
        df_arrivals = df_arrivals[df_arrivals["datetime"] >= beginning]
    
    # build a list of lists for the arrival hours, sorted by day of the week and a dictionary to 
    # count how many of each weeekday have occured (for scaling)
    hst_lst = [[],[],[],[],[],[],[]]
    dow_count = defaultdict(lambda : 0)
    current_dow = -1
    
    # iterate through dataframe, filling the above data structures
    for idx, row in df_arrivals.iterrows():
         hst_lst[row["datetime"].weekday()].append(row["datetime"].hour)
         if row["datetime"].weekday() != current_dow:
             current_dow = row["datetime"].weekday()
             dow_count[DOW[current_dow]] += 1
    
    # create a histogram for each day of the week
    sns.set()
    for i in range(len(hst_lst)):
        plot_hist(hst_lst[i], DOW[i], dow_count[DOW[i]])
    
    
main()
