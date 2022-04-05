import numpy as np
import pandas as pd
import time

while True:
    #Greeting message:

    print("\nHello! let me help you to explore US Bikeshare Data")

    city_index = pd.Series(data=["chicago", "washington", "new_york_city"], index=["Chicago", "Washington", "Newyork"])

    #Here is a check to avoid errors during reading the csv files:

    while True:
        try:
            city_ans = input("\nPlz choose the city you want to explore (chicago/newyork/washington): ")
            city_ans = city_ans.title()
            chosen_city = city_index[city_ans]
            city_data = pd.read_csv("{}.csv".format(chosen_city))
            break
        except KeyError:
            print("\nSorry! plz type the city name correctly from the names within the brackets")

    #Preparing our DataFrame and adding some new columns to help us get
    #the required statistics:-

    city_data["Start Time"] = pd.to_datetime(city_data["Start Time"])

    city_data.insert(2, "Start Hour", city_data["Start Time"].dt.hour)

    city_data.insert(2, "Month", city_data["Start Time"].dt.month)

    city_data.insert(3, "Day", city_data["Start Time"].dt.day_name())

    city_data["Trip"] = city_data["Start Station"] + " To " + city_data["End Station"]

    #Getting the filtered DataFrames (city_data_1 & city_data_2) according
    #to the required filters avoiding KeyError exceptions:-

    #Note that city_data_2 is the final DataFrame after applying filters.

    month_index = pd.Series(data=[1, 2, 3, 4, 5, 6], index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"])

    day_index = pd.Series(data=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], index=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

    filters = ""

    while True:
        filter_month_ans = input("\nDo you want to filter by month? (y/n): ")
        filter_month_ans = filter_month_ans.lower()
        if filter_month_ans == "y":
            while True:
                try:
                    month_ans = input("\nChoose the specified month, plz (jan/feb/mar/apr/may/jun): ")
                    month_ans = month_ans.title()
                    chosen_month = month_index[month_ans]
                    city_data_1 = city_data.loc[city_data["Month"] == chosen_month]
                    filters += month_ans
                    break
                except KeyError:
                    print("\nSorry! wrong month...plz try again and choose the month from those within the brackets")
            break
        elif filter_month_ans == "n":
            city_data_1 = city_data
            filters += "all months"
            break
        else:
            print("\nSorry! plz try again..hint: y for yes and n for no")
    while True:
        filter_day_ans = input("\nDo you want to filter by day? (y/n): ")
        filter_day_ans = filter_day_ans.lower()
        if filter_day_ans == "y":
            while True:
                try:
                    day_ans = input("\nChoose the specified day, plz (sun/mon/tue/wed/thu/fri/sat): ")
                    day_ans = day_ans.title()
                    chosen_day = day_index[day_ans]
                    city_data_2 = city_data_1.loc[city_data_1["Day"] == chosen_day]
                    filters += "-{}".format(chosen_day)
                    break
                except KeyError:
                    print("\nSorry! wrong day...plz try again and choose the day from those within the brackets")
            break
        elif filter_day_ans == "n":
            city_data_2 = city_data_1
            filters += "-all days"
            break
        else:
            print("\nSorry! plz try again..hint: y for yes and n for no")

    #Getting most common month and day of the week:-

    print("\nCalculating the 1st statistic...")

    start = time.time()

    month_names = pd.Series(data=["January", "February", "March", "April", "May", "June"], index=[1, 2, 3, 4, 5, 6])

    most_month = month_names[city_data_1["Month"].mode()[0]]

    most_day = city_data["Day"].mode()[0]

    print("\nMost common month and day in the whole data are {} and {}".format(most_month, most_day))

    print("\nThis took {} seconds".format(time.time() - start))

    #Getting the most common hour:-

    print("\nCalculating the next statistic...")

    start = time.time()

    most_hour = city_data_2["Start Hour"].mode()[0]

    count_most_hour = (city_data_2["Start Hour"] == most_hour).sum()

    print("\nMost common traveling hour of the day is {}, it occured {} times.".format(most_hour, count_most_hour))

    print("\nThe filters are {}, and this took {} seconds".format(filters, time.time() - start))

    #Getting the most common start station, end station and trip:-

    print("\nCalculating the next statistic...")

    start = time.time()

    most_start = city_data_2["Start Station"].mode()[0]

    count_most_start = (city_data_2["Start Station"] == most_start).sum()

    most_end = city_data_2["End Station"].mode()[0]

    count_most_end = (city_data_2["End Station"] == most_end).sum()

    most_trip = city_data_2["Trip"].mode()[0]

    count_most_trip = (city_data_2["Trip"] == most_trip).sum()

    print("\nMost common start station is {}, it occured {} times.".format(most_start, count_most_start))

    print("\nMost common end station is {}, it occured {} times.".format(most_end, count_most_end))

    print("\nMost common trip is '{}', it occured {} times.".format(most_trip, count_most_trip))

    print("\nThe filters are {}, and this took {} seconds".format(filters, time.time() - start))

    #Getting total and average travel times:-

    print("\nCalculating the next statistic...")

    start = time.time()

    total_duration = (city_data_2["Trip Duration"].sum()) / 3600

    avg_duration = city_data_2["Trip Duration"].mean()

    print("\nTotal duration is {} hours, the average duration is {} seconds".format(total_duration, avg_duration))

    print("\nThe filters are {}, and this took {} seconds".format(filters, time.time() - start))

    #Getting user type count, gender count and birth year stats:-

    print("\nCalculating the next statistic...")

    start = time.time()

    def type_counts(column):
        '''Calculate the value caounts of a column and iterately print a string
        containing both the index and its value'''
        user_type_counts = city_data_2[column].value_counts()
        user_types = user_type_counts.index
        type_counts = user_type_counts.values
        for i in range(len(user_type_counts)):
            print("\nNumber of {}s is {}".format(user_types[i], type_counts[i]))

    type_counts("User Type")

    if chosen_city != "washington":
        type_counts("Gender")
        min_year = int(city_data_2["Birth Year"].min())
        min_year_count = (city_data_2["Birth Year"] == min_year).sum()
        max_year = int(city_data_2["Birth Year"].max())
        max_year_count = (city_data_2["Birth Year"] == max_year).sum()
        most_year = int(city_data_2["Birth Year"].mode()[0])
        most_year_count = (city_data_2["Birth Year"] == most_year).sum()
        print("\nEarliest year of birth is {}, it occured {} times.".format(min_year, min_year_count))
        print("\nMost recent year of birth is {}, it occured {} times".format(max_year, max_year_count))
        print("\nMost common year of birth is {}, it occured {} times".format(most_year, most_year_count))

    print("\nThe filters are {}, and this took {} seconds".format(filters, time.time() - start))

    #Displaying 5 rows of the DataFrame:-

    i = 0

    disp_data = pd.read_csv("{}.csv".format(chosen_city))

    while True:
        disp_answer = input("\nDo you want to see 5 rows of the given data? (y/n): ")
        disp_answer = disp_answer.lower()
        if disp_answer == "y":
            print(disp_data.iloc[(i*5):(i+1)*5])
            i += 1
        elif disp_answer == "n":
            break
        else:
            print("\nplz type y for YES or n for NO")

    again_ans = input("\nDo you want to start all over again? (y/n): ")
    again_ans = again_ans.lower()
    if again_ans != "y":
        print("\nThank you...See you later...Bye")
        break
