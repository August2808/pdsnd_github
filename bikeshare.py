import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_list = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Kindly specify the city for the analysis(Chicago, New York City, Washington):').lower()
        if city in city_list:
           break
    # get user input for month (all, january, february, ... , june)
    prompt1 = input('Would you want to limit your analysis to a specific month,[yes or no]? :')
    if prompt1 == 'yes':
        month = input('Kindly specify the month for the analysis(between January to June):').lower()
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt1 = input('Would you want to limit your analysis to a specific day,[yes or no]? :')
    if prompt1 == 'yes':
        day = input('Kindly enter day of the week :')
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def view_data(df):
    prompt2 = input('This is a huge data. Would you like to view some rows from the top of the data? [yes, no] :')
    if prompt2 == 'yes':
        num_of_rows = int(input('Kindly specify the number of rows of data you want to view: '))
        print('The first {} rows of data'.format(num_of_rows))
        data = df.head(num_of_rows)
        print(data)
    else:
        print("Let's proceed")

    prompt3 = input(' Would you like to view some rows from the bottom of the data? [yes, no] :')
    if prompt3 == 'yes':
        num_of_rows = int(input('Kindly specify the number of rows of data you want to view: '))
        print('The last {} rows of data'.format(num_of_rows))
        data = df.tail(num_of_rows)
        print(data)
    else:
        print("Let's proceed to the data analysis")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    most_common_month = df['month'].value_counts().idxmax()
    print('The most common month is {}.'.format(most_common_month))

    # display the most common day of week
    common_day_of_the_week = df['day_of_week'].mode()[0]
    print('The most common day of the week is {}.'.format(common_day_of_the_week))

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is {}.'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df.groupby('Start Station')['Start Station'].count()
    common_start_station_count = max(start_station_count)
    commonly_used_start_station = start_station_count[(start_station_count == common_start_station_count)].index[0]
    print('The most commonly used start station was {}. It was used {} times.'.format(commonly_used_start_station, common_start_station_count))

    # display most commonly used end station
    end_station_count = df.groupby('End Station')['End Station'].count()
    common_end_station_count = max(end_station_count)
    commonly_used_end_station = end_station_count[(end_station_count == common_end_station_count)].index[0]
    print('The most commonly used start station was {}. It was used {} times.'.format(commonly_used_end_station, common_end_station_count))


    # display most frequent combination of start station and end station trips
    most_frequent_start_end_station_trips = df[['Start Station', 'End Station']].mode().loc[0]
    print('The most frequently used start and end stations are {}, and {} respectively.'.format(most_frequent_start_end_station_trips[0], most_frequent_start_end_station_trips[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is {}.".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {}.".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types \n')
    user_type_counts = df.groupby('User Type')['User Type'].count()
    #Iteratively display ouput
    for index, user_type_count in enumerate(user_type_counts):
        print(' {}: {}'.format(user_type_counts.index[index], user_type_count))

    # Display counts of gender

    if 'Gender' in df.columns:
        print('Count of gender types \n')
        gender_type_counts = df.groupby('Gender')['Gender'].count()
        #Iteratively display output
        for index, gender_type_count in enumerate(gender_type_counts):
            print(' {}: {}'.format(gender_type_counts.index[index], gender_type_count))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        new_birth_col = df['Birth Year'].dropna().reset_index(drop=True)
        earliest_year_of_birth = new_birth_col.min()
        most_recent_year_of_birth = new_birth_col.max()
        most_common_year_of_birth = df['Birth Year'].mode().max()
        print('The earliest year of birth is {}.'.format(earliest_year_of_birth))
        print('The most recent year of birth is {}.'.format(most_recent_year_of_birth))
        print('The most common year of birth is {}.'.format(most_common_year_of_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
