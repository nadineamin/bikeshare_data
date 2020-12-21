import time
import pandas as pd
import numpy as np
from calendar import month_name

#important notes!! in chicago, gender and birth year data have NaN values. Make sure to check for NaN



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york, washington)
    cities = ['chicago', 'new york', 'washington']

    city = str(input("Would you like to see data for Chicago, New York, or Washington?\n")).lower()
    
    while city not in cities:
        city = str(input("Invalid input! Please try again: Would you like to see data for Chicago, New York, or Washington?\n")).lower()
        
    print("\nGathering data for " + str(city.title()) + "...")
    
    # filters to be applied to the data
    data_filters = ['month', 'day', 'both', 'neither']

    data_fil = str(input("Would you like to filter the data by month, day, both, or neither?\n")).lower()
    while data_fil not in data_filters:
        data_fil = str(input("Invalid input! Please try again: Would you like to filter the data by month, day, both, or neither?\n")).lower()
    
    if data_fil == 'neither':
        print("\nNo filters will be applied...")
    elif data_fil == 'both':
        print("\nFiltering by both Month and Day...")
    else:
        print("\nFiltering by " + str(data_fil.title()) + "...")
    
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    if data_fil == 'month' or data_fil == 'both':
        month = str(input("Which month - January, February, March, April, May, or June?\n")).lower()
        while (month not in months) or (month == 'all'):
            month = str(input("Invalid input! Please try again: Which month - January, February, March, April, May, or June?\n")).lower()
        print("\nFiltering month by " + month.title() + "...")

    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    
    if data_fil == 'day' or data_fil == 'both':
        day = str(input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")).lower()
        while (day not in days) or (day == 'all'):
            day = str(input("Invalid output! Please try again: Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")).lower()
        print("\nFiltering day by " + day.title() + "...")
    
    else:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: " + str(month_name[df['month'].mode()[0]]))

    # display the most common day of week
    print("The most common day of week is: " + str(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("The most common start hour is: " + str(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: " + str(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is: " + str(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Comb Station'] = [str(x) + " and " + str(y) for x, y in zip(df['Start Station'], df['End Station'])]
    print("The most commonly used combination of start and end stations is: " + str(df['Comb Station'].mode()[0]))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Time Diff'] = df['End Time'] - df['Start Time']
    print("The total travel time is: " + str(df['Time Diff'].sum()))

    # display mean travel time
    print("The mean travel time is: " + str(df['Time Diff'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of user types are:\n" + str(df['User Type'].value_counts()))

    if 'Gender' not in df.columns and 'Birth Year' not in df.columns:
        print("The gender and birth year data are not available for Washington\n")
    
    else:
        # Display counts of gender
        print("\nThe counts of gender are:\n" + str(df['Gender'].value_counts()))
    
        # Display earliest, most recent, and most common year of birth
        print("\nThe earliest birth year is: " + str(int(df['Birth Year'].min())))
        print("The most recent birth year is: " + str(int(df['Birth Year'].max())))
        print("The most common birth year is: " + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(city):
    """Displays a multiple of five rows of raw data based on the user's input."""

    raw_check = str(input("\nWould you like 5 rows of raw data to be displayed? Enter 'yes' or 'no'\n")).lower()
    while raw_check != 'yes' and raw_check != 'no':
        raw_check = str(input("Invalid input! Please try again: Would you like 5 rows of raw data to be displayed? Enter 'yes' or 'no'\n")).lower()
    
    if raw_check == 'no':
        print("No raw data will be displayed\n")
        
    else:
        while raw_check == 'yes':
            for row in pd.read_csv(CITY_DATA[city], iterator = True, chunksize = 5):
                print(row)
                
                raw_check = str(input("\nWould you like 5 more rows of raw data to be displayed? Enter 'yes' or 'no'\n")).lower()
                while raw_check != 'yes' and raw_check != 'no':
                    raw_check = str(input("Invalid input! Please try again: Would you like 5 more rows of raw data to be displayed? Enter 'yes' or 'no'\n")).lower()
                if raw_check == 'no':
                    break
                
        print("No more raw data will be displayed\n")
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        message = str(input("\nWould you like to see cool statistics of the data with the filters you chose? Enter 'yes' or 'no'\n")).lower()
        while message != 'yes' and message != 'no':
            message = str(input("Invalid input! Please try again: Would you like to see cool statistics of the data with the filters you chose? (Type 'yes' or 'no')\n")).lower()
        
        if message == 'yes':
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            
            
        else:
            print("\nNo statistics will be displayed")
            print('-'*40)
        
        raw_data(city)
        restart = input("Would you like to restart? Enter 'yes' or 'no'\n").lower()
        if restart != 'yes':
            print("\nThank you for running this code. I hope you gathered all the data you needed!")
            break

if __name__ == "__main__":
	main()
