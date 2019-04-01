from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import GraphForm, LibraryForm
from app.utility import GraphList
from analyze import NetworkUsageGraph
import os

# TODO Clean up the file paths

# Holds a list of all graphs and related data
reportfile = './app/static/images/imagedata.csv'
graphs = GraphList(reportfile)

@app.route('/')
@app.route('/index')
def index():
    # Use library as the main page
    return redirect(url_for('library'))

@app.route('/library')
def library():

    form = LibraryForm()

    if form.validate_on_submit():
        # Clear images dir except for imagedata.csv, clear imagedata.csv and graph
        pass

    # If there are no graphs and no data to load, show "No graphs generated"
    if(graphs.is_empty() and not graphs.load_data()):
        return render_template('library.html')

    # Show the page and display all the graphs from newest to oldest
    return render_template('library.html', img_paths=graphs.location_list())

@app.route('/new-graph', methods=['GET', 'POST'])
def new_graph():

    form = GraphForm()
    nic = str(form.nic.data).strip()
    time = str(form.time.data).strip()
    timeInterval = str(form.timeInterval.data).strip()

    if form.validate_on_submit():
        # Create graph object based on information in the form
        try:
            graph_dir = './app/static/images/'
            next_index = graphs.get_next_file_index(nic)
            graph_location = str(graph_dir + nic + '(' + next_index + ').png')

            new_graph = NetworkUsageGraph(nic, str('./data/raw/' + nic + '.csv'))
            new_graph.generatePlot().savefig(graph_location)

            graphs.add(nic, graph_location[5:], time, timeInterval)

        except FileNotFoundError:
            pass

        return redirect(url_for('library'))

    return render_template('new-graph.html', form=form)
