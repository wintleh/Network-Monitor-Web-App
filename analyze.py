import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.style.use('seaborn-whitegrid')

# TODO Fix the time and timeInterval portions
# time indicates the middle of the graph
# timeInterval indicated the total interval to be used, centered on time

class NetworkUsageGraph:
    # nic_Capacity
    # nicAddress
    # data
    # end
    # start
    # x_values

    def __init__(self, ipAddressNIC, data_file, start_time=0, \
        end_time=(-1), max_interval_x=300):

        def _adjust_start(start, end, max_interval_x):
            '''
            Adjusts the start value to the end value if
            the interval between them exceeds maxIntervalX.
            '''

            if(end - start > max_interval_x):
                potential_start = end - max_interval_x
                if(potential_start > 0):
                    return potential_start
                else:
                    return 0
            else:
                return start

        def _define_end(current_end):
            '''
            Defines the end value.
            If it was not set, then set it to the end of the data in the
            specified file.
            If it was set, then use that value.
            '''

            if((current_end == -1) or (current_end > self.data.shape[0])):
                return self.data.shape[0]
            else:
                return current_end

        self.nic_Capacity = 125000000       # TODO replace this
        self.nicAddress = ipAddressNIC

        # Holds the time of the recording
        # and how much data per second had passed through
        # the interface over the time interval
        self.data = pd.read_csv(data_file)

        # Convert time column to type datetime
        # This makes finding a difference in the time easier
        self.data['time'] = pd.to_datetime(self.data['time'])

        # By default these are set to the last 5 minutes in dataFile
        self.end = _define_end(end_time)
        self.start = _adjust_start(start_time, end_time, max_interval_x)

        # Define the x values for the graph
        self.x_values = self.data.loc[:, 'time'].dt.time

    def generatePlot(self, file_location=''):
        '''
        Generates a graph base on the parameters defined when the object was
        instantiated
        '''

        timeframe_data = self.data.loc[self.start:(self.end-1)]
        # Time data is held in the first column
        start_date = (timeframe_data.iloc[0, 0]).date()
        end_date = (timeframe_data.iloc[-1, 0]).date()

        # Set the label for the x-axis
        if(end_date == start_date):
            x_label = start_date
        # If the date spans more than one day, then show the start and end
        # date for the data
        else:
            x_label = start_date + " - " + end_date

        fig = plt.figure()
        ax = plt.axes(title=self.nicAddress, \
            xlabel=x_label, ylabel='Link usage (percentage)', ylim=(0, 1))

        ax.plot(self.x_values, \
            self.data.loc[self.start:(self.end-1), 'bytes/sec'] / self.nic_Capacity)

        if(file_location == ''):
            return fig
        else:
            fig.savefig(self.nicAddress + '_graph.png')


# file_name = 'networkData-2SpeedTest'
# myGraph = NetworkUsageGraph('10.12.40.163', './data/raw/' + file_name + '.csv')
# myGraph.generatePlot('./data/graph/')
