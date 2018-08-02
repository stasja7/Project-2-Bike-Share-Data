import time
import pandas as pd

city_data = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['all','january','february','march','april','may','june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday','friday','saturday','sunday']

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
    city = input ('Please select New York City, Chicago, or Washington: ').lower()
    while city not in city_data:
        print ('Please try again.')
        break
   
    # get user input for month (all, january, february, ... , june)
    month = input ('Now I need you to tell me the month (ex. All, January, February, March, April, May, or June): ').lower()
    while month not in months:
        print ('Please try again.')
        break
  
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input ('Enter a day (ex. All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ').lower()
    while day not in days:
        print ('Please try again')
        break
    
    print('-'*40)
    print('Here is your selection: ', '{}, {}, {}'.format(city, month, day).title())
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
    df = pd.read_csv(city_data[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    import datetime
    common_month = df['month'].mode()[0]
    month_str = datetime.date(1900, common_month, 1).strftime('%B') #converted month number to month name
    print('Most Common Month: ', month_str)
    
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day: ', common_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = str(df['hour'].mode()[0])
    popular_hour_st = datetime.datetime.strptime(popular_hour, '%H').strftime('%#I %p') #in standard time and removed leading zero
    print('Most Popular Start Hour:', popular_hour_st) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_combination = df.groupby(['Start Station', 'End Station']).size().reset_index(name='start_end_count').sort_values(['start_end_count'], ascending=[0])
    print('Most Frequent Combination: ', frequent_combination['Start Station'].iloc[0], '-', frequent_combination['End Station'].iloc[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    day_s = total_travel_time // (24 * 3600)
    total_travel_time = total_travel_time % (24 * 3600)
    hour_s = total_travel_time // 3600
    total_travel_time %= 3600
    minutes_s = total_travel_time // 60
    total_travel_time %= 60
    seconds_s = total_travel_time
       
    print('Total Travel Time \nDays: {} \nHours: {} \nMinutes: {} \nSeconds: {}'.format(day_s, hour_s, minutes_s, seconds_s))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    day_m = mean_travel_time // (24 * 3600)
    mean_travel_time = mean_travel_time % (24 * 3600)
    hour_m = mean_travel_time // 3600
    mean_travel_time %= 3600
    minutes_m = mean_travel_time // 60
    mean_travel_time %= 60
    seconds_m = mean_travel_time
    
    print('\nMean Travel Time \nDays: {} \nHours: {} \nMinutes: {} \nSeconds: {}'.format(day_m, hour_m, minutes_m, seconds_m))
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
       
    user_type = df['User Type'].value_counts()
    print('Count of User Type:\n', user_type)
    
    # Display counts of gender
    city = input
    if city != 'washington':
        try:
            gender_count = df['Gender'].value_counts()
            print('Gender Count:\n', gender_count)
        except KeyError:
            print('Gender count data is not available for Washington.')
            
    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        try:
            min_year_of_birth = int(df['Birth Year'].min())
            max_year_of_birth = int(df['Birth Year'].max())
            common_year_of_birth = int(df['Birth Year'].mode()[0])
            print('Earliest year of birth: {}\nMost recent year of birth: {}\nMost common year of birth: {}'.format(min_year_of_birth, max_year_of_birth, common_year_of_birth))
        except KeyError:
            print('Year of birth data is not available for Washington.')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():  
    while True:
        #Display raw data at user request
        city, month, day = get_filters()
        df = load_data(city, month, day)
        x = 0
        y = x + 5             
        five_rows = input('Would you like to see the first five rows of data? Enter yes or no.\n')
        if five_rows == 'yes':
            print(df.iloc[x:y])
            while x < len(df.index):
                next_five_rows = input('Would you like to see five more rows? Enter yes or no.\n')
                if next_five_rows == 'yes':
                    x += 5
                    y += 5
                    print(df.iloc[x:y])
                else:
                    break
              
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
