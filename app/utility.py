import pandas as pd
from pandas.errors import EmptyDataError
from analyze import RankIP
import re

# TODO Deal with duplicates

class NICDataList:
    '''
    Used to hold all the NIC data that corresponds to the graphs. Should be
    used in conjunction with a GraphList. The ith element from this list should
    match the ith element from the corresponding GraphList. The reportfile holds
    the file location for the raw data file, this is used when the server starts
    and there is data still saved.
    '''

    def __init__(self, reportfile):
        self.list = self._empty_list_df()
        self.datafiles = self._empty_list_file()
        self.reportfile = reportfile

    def _empty_list_df(self):
        '''
        Used with self.list
        '''
        return pd.DataFrame(columns=['destIP', 'packets'])

    def _empty_list_file(self):
        '''
        Used with self.datafiles
        '''
        return pd.DataFrame(columns=['file'])


    def get_data(self):
        return self.list

    def add(self, df, file):
        '''
        Add a new entry to the list
        '''

        new_f = pd.DataFrame({'file':file}, index=[self.datafiles.shape[0]])
        new_df = pd.DataFrame({'destIP':[df.loc[:,'destIP'].tolist()], \
            'packets':[df.loc[:,'packets'].tolist()]},\
            index=[self.list.shape[0]])

        self.datafiles = self.datafiles.append(new_f)
        self.list = self.list.append(new_df, sort=True)
        # print(self.list)

        # Write all the data to the csv
        self.datafiles.to_csv(self.reportfile, index=False)

    def clear(self):
        '''
        Clears the list. Returns a list of the locations to the .png files
        for the graphs that were in the list
        '''
        # Overwrite self.list with an empty df, update the reportfile
        self.list = self._empty_list_df()
        self.datafiles = self._empty_list_file()
        self.datafiles.to_csv(self.reportfile, index=False)

    def load_data(self, top_n_dest):
        '''
        Returns True if there was data to load,
        False if there was no data to load.
        '''
        try:
            generated = pd.read_csv(self.reportfile)['file'].tolist()
            for file in generated:
                # Read the file, then re-rank and add to list
                ranked = RankIP(file)
                self.add(ranked.get_top(top_n_dest), file)

            # print(self.list.to_string())
            return True
        # If there is no data, do nothing
        except EmptyDataError:
            return False

    def is_empty(self):
        return self.list.shape[0] == 0

    def __str__(self):
        return self.list.to_string()

class GraphList:
    '''
    A list used to hold the locations to all of the graphs
    along with other data about the graphs.
    '''

    def __init__(self, reportfile):
        self.list = self._empty_df()
        self.reportfile = reportfile

    def _empty_df(self):
        return pd.DataFrame(columns=['nic', 'location', 'date']) # , 'timeInterval' TODO implement

    def get_next_file_index(self, nic):
        '''
        Returns the index number for the filename the next graph should be assigned
        '''
        # Get a dataframe of the locations of graphs associated with the nic
        nic_locations = self.list[self.list.loc[:, 'nic'] == nic]\
            .drop(['nic', 'date'], axis=1) # , 'timeInterval' TODO implement

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

    def add(self, nic, location, date): #, timeInterval): TODO implement
        '''
        Add a new entry to the list
        '''
        # Create a temporary dataframe with one row
        # Then combine it with the full dataframe
        new_graph = pd.DataFrame({'nic':nic, 'location':location, 'date':date},\
            index=[self.list.shape[0]])
            #'timeInterval':timeInterval},


        self.list = self.list.append(new_graph, sort=True)

        # Write all the data to the csv
        self.list.to_csv(self.reportfile, index=False)

    def clear(self):
        '''
        Clears the list. Returns a list of the locations to the .png files
        for the graphs that were in the list
        '''
        # Gets a list of all the locations listed int he location column
        location_list = self.list['location'].tolist()

        # Overwrite self.list with an empty df, update the reportfile
        self.list = self._empty_df()
        self.list.to_csv(self.reportfile, index=False)

        return location_list

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
