import pandas as pd
from pandas.errors import EmptyDataError
import re

# TODO Deal with duplicates

class GraphList:
    '''
    A list used to hold the locations to all of the graphs
    along with other data about the graphs.
    '''

    def __init__(self, reportfile):
        self.list = pd.DataFrame(columns=['nic', 'location', 'time', 'timeInterval'])
        self.reportfile = reportfile

    def _empty_df(self):
        return pd.DataFrame(columns=['nic', 'location', 'time', 'timeInterval'])

    def get_next_file_index(self, nic):
        '''
        Returns the index number for the filename the next graph should be assigned
        '''
        # Get a dataframe of the locations of graphs associated with the nic
        nic_locations = self.list[self.list.loc[:, 'nic'] == nic]\
            .drop(['nic', 'time', 'timeInterval'], axis=1)

        # Sort (descending) by location
        # Get the first element in location
        # Get the index of that file
        try:
            high_index_location = nic_locations.sort_values('location', \
                ascending=False).iloc[0, 0]

        # If there is an index error, then there was no graph for that nic
        # The next index will be 0 (the first)
        except IndexError:
            return '0'

        # Don't need to worry about the first 15 chars in the regex,
            # they will always be the same
        # Get the index from the filename, then increment it to get the next
            # file index for this nic
        return str(int(\
            re.sub(r'\w+.*\(|\).png', '', high_index_location[15:])) + 1)

    def add(self, nic, location, time, timeInterval):
        '''
        Add a new entry to the list
        '''
        # Create a temporary dataframe with one row
        # Then combine it with the full dataframe
        new_graph = pd.DataFrame({'nic':nic, 'location':location, 'time':time,\
            'timeInterval':timeInterval}, index=[self.list.shape[0]])

        self.list = self.list.append(new_graph, sort=True)

        # Write all the data to the csv
        self.list.to_csv(self.reportfile, index=False)

    def clear(self):
        self.list = _empty_df()

#     def delete(self):
        # TODO implement this: figure out how deleting graphs will work

    def load_data(self):
        '''
        Returns True if there was data to load,
        False if there was no data to load.
        '''
        try:
            self.list = pd.read_csv(self.reportfile)
            # print(self.list.to_string())
            return True
        # If there is no data, do nothing
        except EmptyDataError:
            return False

    def location_list(self):
        return self.list['location'].tolist()

    def is_empty(self):
        return self.list.shape[0] == 0

    def __str__(self):
        return self.list.to_string()
