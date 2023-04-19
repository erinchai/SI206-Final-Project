import matplotlib.pyplot as plt
import numpy as np

week_list = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8']
nyc_aqi_list = [72, 50, 41, 41, 52, 57, 55, 46]
honolulu_aqi_list = [48, 38, 37, 35, 30, 39, 37, 38]
nyc_temp_list = [46, 38, 39, 40, 32, 41, 44, 39]



def compare_temp_graph():
    # Numbers of pairs of bars you want
    N = 8

    # Data on X-axis
    # Specify the values of blue bars (height) -- NYC
    blue_bar = (46, 38, 39, 40, 32, 41, 44, 39)
    # Specify the values of pink bars (height) -- Honolulu
    pink_bar = (74, 73, 77, 74, 73, 74, 73, 73)

    # Position of bars on x-axis
    ind = np.arange(N)

    # Figure size
    plt.figure(figsize=(10,5))

    # Width of a bar 
    width = 0.3       

    # Plotting
    plt.bar(ind, blue_bar , width, label='New York City')
    plt.bar(ind + width, pink_bar, width, color = "pink",label='Honolulu')

    plt.xlabel('Week in 01/01/2023-02/28/2023')
    plt.ylabel('Temperature (Farenheit)')
    plt.ylim(0, 90)
    plt.title('Comparing New York City and Honolulu Average Weekly Temperatures in Jan/Feb')

    # xticks()
    # First argument - A list of positions at which ticks should be placed
    # Second argument -  A list of labels to place at the given locations
    plt.xticks(ind + width / 2, ('Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'))

    # Finding the best position for legends and putting it
    plt.legend(loc='best')
    plt.savefig("compare_temp.png")
    plt.show()


def compare_aqi_graph():
    # Numbers of pairs of bars you want
    N = 8

    # Data on X-axis

    # Specify the values of blue bars (height)
    blue_bar = (72, 50, 41, 41, 52, 57, 55, 46)
    # Specify the values of orange bars (height)
    pink_bar = (48, 38, 37, 35, 30, 39, 37, 38)

    # Position of bars on x-axis
    ind = np.arange(N)

    # Figure size
    plt.figure(figsize=(10,5))

    # Width of a bar 
    width = 0.3       

    # Plotting
    plt.bar(ind, blue_bar , width, label='New York')
    plt.bar(ind + width, pink_bar, width, color = "pink",label='Honolulu')

    plt.xlabel('Week in 01/01/2023 - 02/28/2023')
    plt.ylabel('AQI Level')
    plt.title('Comparing New York City and Honolulu Average Weekly AQI in Jan/Feb')

    # xticks()
    # First argument - A list of positions at which ticks should be placed
    # Second argument -  A list of labels to place at the given locations
    plt.xticks(ind + width / 2, ('Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'))

    # Finding the best position for legends and putting it
    plt.legend(loc='best')
    plt.savefig("compare_aqi.png")
    plt.show()


def compare_humidity():
    # Numbers of pairs of bars you want
    N = 8

    # Data on X-axis

    # Specify the values of blue bars (height)
    blue_bar = (82, 67, 64, 68, 50, 67, 58, 68)
    # Specify the values of orange bars (height)
    pink_bar = (75, 71, 75, 74, 82, 77, 81, 81)

    # Position of bars on x-axis
    ind = np.arange(N)

    # Figure size
    plt.figure(figsize=(10,5))

    # Width of a bar 
    width = 0.3       

    # Plotting
    plt.bar(ind, blue_bar , width, label='New York')
    plt.bar(ind + width, pink_bar, width, color = "pink",label='Honolulu')

    plt.xlabel('Week in 01/01/2023 - 02/28/2023')
    plt.ylabel('Humidity Percentage')
    plt.title('Comparing New York City and Honolulu Average Weekly Humidity in Jan/Feb')

    # xticks()
    # First argument - A list of positions at which ticks should be placed
    # Second argument -  A list of labels to place at the given locations
    plt.xticks(ind + width / 2, ('Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'))

    # Finding the best position for legends and putting it
    plt.legend(loc='best')
    plt.savefig("compare_humidity.png")
    plt.show()

compare_temp_graph
compare_aqi_graph()
compare_humidity()


    