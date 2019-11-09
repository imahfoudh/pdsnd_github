import time
import pandas as pd
import numpy as np
#from PIL import Image



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities=["chicago","new york city", "washington"]
months=["january", "february","march","april","may","june","all"]
days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday","all"]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #Bike = Image.open('bike.png')
    #Bike.show()
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input("\nGive the name of city you want to analyze (Chicago, New York City, or Washington): ").lower()
    while(True):
        #if(city=="chicago" or city=="new york city" or city == "washington" or city == "all"):
        if(city in cities):
            break
        else:
            city=input("Please give an entry from city options: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month=input("\nGive the name of the specific month you want to analyze (from January to June, or All): ").lower()
    while(True):
        if(month in months):
            break
        else:
            month=input("Please give an entry from month options: ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input("\nGive the name of the specific day you want to analyze or (All) to analyze everything: ").lower()
    while(True):
        if(day in days):
            break
        else:
            day=input("Please give a valid day of the week entry: ").lower()



    input("\nClick ENTER to continue to next section \n")
    print('-*'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month_name'] = df['Start Time'].dt.month
    df['day_name'] = df['Start Time'].dt.weekday_name
    df['s_hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months=["january", "february","march","april","may","june","all"]
        month=months.index(month)+1
        df = df[df['month_name']==month]

    if day !='all':
        df = df[df['day_name']==day.title()]


    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month =="all":
        common_month= df['month_name'].value_counts().idxmax()-1
        months0=["January", "February","March","April","May","June","all"]
        print("\nThe most common month number is: ",months0[common_month])
#can consider name instead of a number


    # display the most common day of week
    if day =="all":
        common_day=df['day_name'].value_counts().idxmax()
        print("\nThe most common day is: ",common_day)


    # display the most common start hour
    common_hour=df['s_hour'].value_counts().idxmax()
    print("\nThe most common hour is: ", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\nClick ENTER to continue to next section \n")
    print('-*'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_s_station=df['Start Station'].value_counts().idxmax()
    print("\nMost commonly used starting station is: ",common_s_station)
    # display most commonly used end station
    common_e_station=df['End Station'].value_counts().idxmax()
    print("\nMost commonly used ending station is: ", common_e_station)
    # display most frequent combination of start station and end station trip
    df['station_combination']="from  "+df['Start Station']+"   to   "+df['End Station']
    common_combination=df['station_combination'].value_counts().idxmax()
    print("\nMost commonly used station combination is: ", common_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\nClick ENTER to continue to next section \n")
    print('-*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    total_travel = df['Trip Duration'].sum()
    total_in_minutes=total_travel/60
    total_in_days = total_in_minutes/1440
    print("Total time travelled in minutes is: ", total_travel, " minutes. Equals to ", int(total_in_days), "day(s) - rounded")


    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_travel_minutes=mean_travel/60
    print("\nAverage time travelled in minutes is: ", mean_travel_minutes.round(2), " minutes.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\nClick ENTER to continue to next section \n")
    print('-*'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types / Customers and Subscribers
    #user_count= df['User Type'].value_counts() #for testing
    subscribers_c=df['User Type'].str.count("Subscriber").sum()
    customers_c=df['User Type'].str.count("Customer").sum()


    print("{} trips were made in total: {} trips were made by Subscribers, and {} trips were made by one-off customers".format((subscribers_c+customers_c),subscribers_c,customers_c))


    # Display counts of gender / not available for DC
    if city != 'washington':
        male_count=df['Gender'].str.count("Male").sum()
        female_count=df['Gender'].str.count("Female").sum()
        null_count=df['Gender'].isnull().sum().sum()
        print("\nThe trips were made by {} male customers and {} female customer. {} data points are missing".format(int(male_count),int(female_count),null_count))


    # Display earliest, most recent, and most common year of birth / not available for DC
    if city != 'washington':
        earliest_yr= df['Birth Year'].min()
        most_recent_yr= df['Birth Year'].max()
        most_common_yr= df['Birth Year'].value_counts().idxmax()

        print("\nThe oldest customer was born in {}, while the youngest was born in {}. The most common birth year for our costumers is {}".format(int(earliest_yr),int(most_recent_yr),int(most_common_yr)))



    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-*'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        data_display=input("\nWould like to view a snapshot of the dataset? Enter yes or no:\n")
        if data_display.lower() =='yes':
            print("\n\n\nPrinting list of columns.....\n")
            print(df.iloc[5])
            print("\n\n\nPrinting the snapshot of the first 5 rows.....\n")
            print(df.head())
        else:
            print("\nData snapshot skipped\n")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nExiting program\n")
            break

main()
