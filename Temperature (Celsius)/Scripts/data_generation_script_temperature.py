"""Data Generation Script."""
# Import relevant libraries
import datetime as dt
import numpy as np
import pandas as pd
import random


def shift_value_generator(discrete_shift_values, shift_values_distribution):
    """Generate values for a shift such as day or night shift.

    Parameters
    ----------
    discrete_shift_values : list
        The values that can be taken on during the shift.
    shift_values_distribution : list
        The probability distribution of the discrete shift values.

    Returns
    -------
    shift_values : list
        The list of random values for the custom-defined shift.

    """
    # Create an empty list to store the generated values
    shift_values = []

    # The choices() method returns a list with the randomly selected element
    # from the specified sequence. You can weigh the possibility of each
    # result with the weights parameter. k is the size of list generated.
    shift_values = (random.choices(discrete_shift_values,
                                   weights = (shift_values_distribution),
                                   k = 4464))

    return shift_values


def min_num_repeat(night_shift_list, n_repeats_choice):
    """Ensure "26" is repeated 6-12 times (30-60 mins) to simulate "off" asset.

    Parameters
    ----------
    night_shift_list : list
        The list of original night shift values.
    n_repeats_choice : list
        The range of values that "26" can be repeated for.

    Returns
    -------
    night_shift_list : list
        The list of adjusted night shift values with minimum repeated "26".

    """
    # Create an empty list to store each row's repeat value
    n_times_repeat = []

    # Loop through each row to decide whether it should be repeated
    for i in night_shift_list:
        if i == 26:
            n_times_repeat.append(random.choice(n_repeats_choice))
        else:
            n_times_repeat.append(1)

    # Use repeat() method to repeat "26" by the randomly selected number
    night_shift_list = np.repeat(night_shift_list, n_times_repeat)
    night_shift_list = night_shift_list[0:4464]

    return night_shift_list


def shift_df_generator(empty_df, day_lower_hr_lim, day_upper_hr_lim):
    """Generate day and night dataframe.

    Parameters
    ----------
    empty_df : DataFrame
        A DataFrame with timestamp and 'Temperature (Celsius)' with all zeros.
    day_lower_hr_lim : int
        The lower hour limit that constitutes the start of the day shift.
    day_upper_hr_lim : int
        The upper hour limit that constitutes the end of the day shift.

    Returns
    -------
    day_df : DataFrame
        A DataFrame containing only dayshift values.
    night_df : DataFrame
        A DataFrame containing only nightshift values.

    """
    # Create 2 temporary dataframes (1 for dayshift, 1 for nightshift)
    day_df = empty_df.loc[(empty_df['Timestamp'].dt.hour >= day_lower_hr_lim) &
                          (empty_df['Timestamp'].dt.hour < day_upper_hr_lim)]
    # Night dataframe will consist of rows with indices not taken by day_df
    night_df = empty_df[~empty_df.index.isin(day_df.index)]

    return day_df, night_df


def main():

    # Generate lists of day shift values for 10 datasets
    day_shift_values_1 = [44, 48, 51, 54, 57, 61, 65, 70, 79, 81, 84]
    day_shift_values_2 = [44, 48, 51, 53, 57, 60, 64, 69, 79, 80, 82]
    day_shift_values_3 = [43, 47, 49, 53, 57, 61, 65, 70, 78, 80, 82]
    day_shift_values_4 = [43, 47, 49, 52, 56, 60, 64, 69, 78, 79]
    day_shift_values_5 = [42, 46, 49, 53, 56, 60, 63, 67, 78, 79]
    day_shift_values_6 = [42, 46, 49, 51, 55, 59, 63, 68, 77, 78]
    day_shift_values_7 = [41, 45, 48, 51, 54, 58, 62, 67, 77, 78]
    day_shift_values_8 = [41, 45, 48, 52, 53, 57, 61, 67, 77, 78]
    day_shift_values_9 = [40, 44, 48, 51, 55, 59, 63, 68, 77, 78]
    day_shift_values_10 = [40, 44, 48, 51, 54, 58, 62, 67, 76, 77]

    # Define day shift values distribution
    day_shift_values_distribution_1 = [8, 8, 15, 16, 16, 16, 8, 5, 3, 3, 2]
    day_shift_values_distribution_2 = [9, 9, 15, 16, 16, 16, 10, 7, 1, 1]

    # Generate the 10 day shift datasets
    for i in range(1, 4):
        exec(f'day_shift_{i} = shift_value_generator(day_shift_values_{i}, day_shift_values_distribution_1)')
    for i in range(4, 11):
        exec(f'day_shift_{i} = shift_value_generator(day_shift_values_{i}, day_shift_values_distribution_2)')

    # Generate list of night shift values
    night_shift_values = [26, 31, 35, 37, 40, 45, 49, 51, 53]
    night_shift_values_distribution = [5, 9, 9, 16, 16, 16, 16, 8, 5]
    night_shift = shift_value_generator(night_shift_values,
                                        night_shift_values_distribution)

    # Define the range of values that "26" can be repeated for
    n_repeats_choice = [6, 7, 8, 9, 10, 11, 12]
    for i in range(1, 11):
        exec(f'night_shift_{i} = min_num_repeat(night_shift, n_repeats_choice)')

    # Generate timestamp for 31 days (January) in intervals of 5 minutes
    # 1 day = 60mins/h * 24h = 1440mins
    # No. of 5mins interval per day = 1440mins/5mins = 288
    # No. of 5mins interval in 31 days = 288 * 31 = 8928
    timestamp_list = [(dt.datetime(2021, 1, 1, 0, 0, 0) +
                       dt.timedelta(minutes = 5 * x))
                      for x in range(8928)]

    # Create a dataframe with a timestamp column and an empty temperature column
    # Fill up the temperature column with all 0 values first
    temperature_values = np.zeros(8928)
    temperature_dataset = pd.DataFrame.from_dict({
        'Timestamp': timestamp_list,
        'Temperature (Celsius)': temperature_values
        })

    # Create day and night dataframes with defined range of hours for day shift
    for i in range(1, 11):
        exec(f'day_df_{i}, night_df_{i} = shift_df_generator(temperature_dataset, 8, 20)')

    # Fill up each dataframe with respective distribution of values
    for i in range(1, 11):
        exec(f'day_df_{i}.loc[:, "Temperature (Celsius)"] = day_shift_{i}')
        exec(f'night_df_{i}.loc[:, "Temperature (Celsius)"] = night_shift_{i}')

    # Combine both dataframes and sort back according to index (aka timestamp)
    for i in range(1, 11):
        exec(f'combined_dataset_{i} = pd.concat([day_df_{i}, night_df_{i}])')
        exec(f'combined_dataset_{i}.sort_index(inplace = True)')

        # Save the combined dataframe to an excel file
        exec(f'combined_dataset_{i}.to_excel("Temperature_Dataset_{i}.xlsx", header = True, index = False)')


if __name__ == '__main__':
    main()
