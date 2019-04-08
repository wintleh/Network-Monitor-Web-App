from flask import render_template, flash, redirect, url_for, make_response
from app import app
from app.forms import GraphForm, LibraryForm
from app.utility import GraphList, NICDataList
from analyze import NetworkUsageGraph, RankIP
import os

# TODO Clean up the file paths
dir_path = os.path.dirname(os.path.realpath(__file__))

# Holds a list of all graphs and related data
graphs_reportfile = './app/static/images/imagedata.csv'
nic_reportfile = './app/static/images/nicdata.csv'
graphs = GraphList(graphs_reportfile)
nic_data = NICDataList(nic_reportfile)

# Defines how many top destination ip addresses to show
top_n_dest = 5

# Load the data, initially
nic_data.load_data(top_n_dest)
graphs.load_data()

################################################################################

@app.after_request
def nocache(response):
    '''
    Used to make the server not cache the page. Makes images display correctly.
    '''
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

################################################################################
# Handles showing content on each page
################################################################################
@app.route('/')
@app.route('/index')
def index():
    # Use library as the main page
    return redirect(url_for('library'))

################################################################################

@app.route('/library', methods=['GET', 'POST'])
def library():

    form = LibraryForm()

    if form.validate_on_submit():
        # Clear images dir except for imagedata.csv, clear imagedata.csv and graph
        nic_data.clear()
        graph_files = graphs.clear()
        for graph_file in graph_files:
            # Removes the file
            os.remove(os.path.join(dir_path, graph_file[1:]))

    # If there are no graphs and no data to load, show "No graphs generated"
    if( (graphs.is_empty() and nic_data.is_empty()) and not \
        (graphs.load_data() and nic_data.load_data(top_n_dest))):
        return render_template('library.html')

    # Show the page and display all the graphs from newest to oldest
    # Do not cache the page, so that the images display correctly
    return nocache(make_response(render_template(\
        'library.html', img_paths=graphs.location_list(), form=form, \
        graph_range=range(len(graphs.location_list())), \
        top_dest_range=range(top_n_dest), df_NICdata=nic_data.get_data())))

################################################################################

@app.route('/new-graph', methods=['GET', 'POST'])
def new_graph():

    form = GraphForm()
    nic = str(form.nic.data).strip()
    date = str(form.date.data)
    # timeInterval = str(form.timeInterval.data).strip()    TODO implement

    if form.validate_on_submit():
        # Create graph object based on information in the form
        try:
            # Creating a graph from the network useage data, add to list
            images_dir = './app/static/images/'
            next_index = graphs.get_next_file_index(nic)
            graph_location = str(images_dir + nic + '(' + next_index + ').png')

            new_graph = NetworkUsageGraph(nic, \
                str('./data/raw/' + nic + '_' + date + '.csv'))
            new_graph.generatePlot().savefig(graph_location)

            graphs.add(nic, graph_location[5:], date)#, timeInterval) TODO implement

            # Create table (actually df, abstracted to be table), add to list
            datafile = str('./data/raw/' + nic + '_' + date + '_COUNT.csv')
            ip_rank = RankIP(datafile)
            nic_data.add(ip_rank.get_top(top_n_dest), datafile)

        except FileNotFoundError:
            pass

        return redirect(url_for('library'))

    return render_template('new-graph.html', form=form)
