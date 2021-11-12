import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

#First function to grab filters from raw user input. While loops handle user input error.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
 
# Ask user to input which city they would like to explore.      
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?: ").title()
        if city not in ("Chicago", "New York City", "Washington"):
            print ("You have entered an invalid city. Please try again.")
            continue
        else: 
            break
 # Ask user to input how they would like to filter the data. Loop through the options.       
    x = True
    while x == True: 
        filters = input("Would you like to filter the data by month, day, both, or none?: ").lower()
        if filters == "month":
            day = "All"
            while True: 
                month = input("Which month? (January, February, March, April, May, or June): ").title()
                if month not in ("January", "February", "March", "April", "May", "June"):
                    print ("You have entered an invalid month. Please try again.")
                    continue
                else: 
                    x = False
                    break
        elif filters == "day":
            month = "All"
            while True:
                day = input("Which day? (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday): ").title()
                if day not in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
                    print ("You have entered an invalid choice. Please try again.")
                    continue
                else:
                    x = False
                    break
        elif filters == "both":
            while True: 
                month = input("Which month? (January, February, March, April, May, or June): ").title()
                if month not in ("January", "February", "March", "April", "May", "June"):
                    print ("You have entered an invalid month. Please try again.")
                    continue
                else: 
                    break
            while True:
                day = input("Which day? (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday): ").title()
                if day not in ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"):
                    print ("You have entered an invalid choice. Please try again.")
                    continue
                else: 
                    x = False
                    break
        elif filters == "none":
            month = "All"
            day = "All"
            x = False
        elif filters not in ("both", "month", "day", "none"): 
            print("You have entered an invalid choice. Please try again.")
            continue
        else:
            if x == False:
                break
            break

       
    print('-'*40)
    return city, month, day

#Function that applies filters chosen in the def get_filters function. 
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        df = df[df['month'] == month]

    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

#Calculate and display the statistics for most common month, days, and hours traveled. 
    
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month_name = months[common_month -1]
    print('The most common month is: ',common_month_name)
    
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day)

    
    common_hour = df['hour'].mode()[0]

#Convert hour as integer into readable time format. 

    if common_hour > 12:
        common_hour_time = str(common_hour - 12) + ":00 PM"
    elif common_hour == 12:
        common_hour_time = str(common_hour) + ":00 PM"
    else:
        common_hour_time = str(common_hour) + ":00 AM"

    print('The most common start hour is: {}.'.format(common_hour_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Caclulate and display most commonly used start station.
    common_start = df['Start Station'].mode()[0]
    print('The most common start station is: ', common_start)
    
    # Calculate and display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station is: ', common_end)

    # Calculate and display most frequent combination of start station and end station trip
    frequent_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most frequent combination of start station and end station tripsyes is: ', frequent_combo)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate and display total travel time. Change seconds into days, take the remainder and change into hours, etc. Display final output       # as readable time. 
    
    seconds_passed = df['Trip Duration'].sum()
    day = int(seconds_passed//86400)
    hour = int((seconds_passed -(day*86400))//3600)
    minute = int((seconds_passed -((day*86400) + (hour*3600)))//60)
    seconds = int(seconds_passed - ((day*86400) + (hour*3600) + (minute*60)))
    total_travel = datetime.time(hour, minute, seconds)
    

    print ('The total time traveling done through June was {} days {}'.format(day,total_travel))


    # Calculate and display mean travel time. Same method as above to caclulate time as days, hours, minutes passed. 
    
    avg_travel = int(df['Trip Duration'].mean())
    avg_day = avg_travel//86400
    avg_hour = (avg_travel-(avg_day*86400))//3600
    avg_min = (avg_travel-((avg_day*86400) + (avg_hour*3600)))//60
    avg_sec = avg_travel-((avg_day*86400) + (avg_hour*3600) + (avg_min*60))
    avg_time = datetime.time(avg_hour, avg_min, avg_sec)
    
    print('The average time spent on each trip was {} days {}'.format(avg_day, avg_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate and display counts of user types
    user_types = df['User Type'].value_counts()
    print('The count of each user type is: ')
    print(user_types)
    
    # Calculate and display counts of gender
    try:
        gender_count = df['Gender'].value_counts(dropna=True)
        print('The count of each gender is: ')
        print(gender_count)
    except KeyError:
        print('Gender data not available for this city.')
    
    # Calculate and display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])

        print('The earliest year of birth is {}'.format(earliest))
        print('The most recent year of birth is {}'.format(recent))
        print('The most common year of birth is {}'.format(common_birth))
    except KeyError:
        print('Birth year data not available for this city.')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        while True:
            rawdata = input('\nWould you like to see the raw data? Enter yes or no.\n')
            if rawdata.lower() not in ('yes', 'no'):
                print("You have entered an invalid input. Please try again.")
                continue
            elif rawdata.lower() == 'no':
                break
            elif rawdata.lower() == 'yes':
                n = 0
                x = n + 5
                print(df.iloc[n:x])
                while True:
                    next_line = input("\nWould you like to see the next five entries? Enter yes or no. \n").lower()
                    if next_line == 'yes':
                        n = n + 5
                        x = x + 5
                        print(df.iloc[n:x])
                        continue
                    else:
                        break
            break
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            n = 0
            x = n + 5
            break


if __name__ == "__main__":
	main()
