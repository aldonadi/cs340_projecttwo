# Setup the Jupyter version of Dash
from sys import set_asyncgen_hooks
from typing import dataclass_transform
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output

from dash import callback_context

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# For logging long-running queries
import time

# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from aac_crud_driver import AnimalShelter

# for loading quick filter buttons from the quick-filters.yml file
from quick_filter_buttons import QuickFilter, QuickFilters

###########################
# Data Manipulation / Model
###########################

# use credentials and DB connection details stored in `db.yml` instead of hardcoded
shelter = AnimalShelter()

# quick filter button query JSONs
quick_filters = {}

# number of quick-filter buttons for purposes of the callback (will be calculated during button generation)
num_quick_filter_buttons = 0


# class read method ('find' in my CRUD driver implementation) must support return
# of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
print("Retrieving all records...", end="")
start_time = time.time()
df = pd.DataFrame.from_records(shelter.find({}))
end_time = time.time()
total_time = end_time - start_time
total_records = len(df.to_dict(orient='records'))
print(f"obtained {total_records} records in {total_time:.2f} seconds.")

# dropping the '_id' field is not necessary for my CRUD driver because my 'find' implementation
# does not return the '_id' field unless the 'find' method optional argument 'include_id'
# is set to True

# used to automatically generate the quick-filter button bar
def create_filter_button_bar_html_element():
    # load the quick filter data from the quick-filters.yml file
    filters = QuickFilters.load()

    global quick_filters
    global num_quick_filter_buttons
    num_quick_filter_buttons = len(filters)

    # the array of button HTML elements that will be generated
    filter_buttons = []

    button_number = 1

    for filter in filters:
        button_id = f"quick-filter-button-{button_number}"   # to identify which button was clicked in the callback

        # TODO: consider removing the "data-query" from the button.
        # My first idea was to use the callback to identify which button ID was clicked (I have figured this part out)
        # and then to pull the 'data-query' attribute out of the clicked button (I cannot figure out how to do this)
        # Instead, I am storing the query filter JSON in a global dict (not ideal)

        # create and add the button HTML element for this quick filter
        button = html.Button(
                filter.name,                        # button text
                className="quick-filter",           # for CSS styling
                id=button_id,
                n_clicks=0, 
                **{"data-query": filter.query_json()})  # the query JSON to give to the CRUD driver # TODO: remove this as vestigial?
        filter_buttons.append(button)

        # add the filter's query JSON and name to the lookup dict
        quick_filters[button_id] = {
                'filter-name': filter.name,
                'query-json':  filter.query_json()
                }

        button_number += 1

    # add the final "Clear Filters" button
    button = html.Button("Clear Filters", className="quick-filter", id="clear-filters", n_clicks=0)
    filter_buttons.append(button)
    quick_filters["clear-filters"] = { 'filter-name': '', 'query-json': {} }

    # add a "Current quickfilter" status element
    current_filter = html.Em(id="current-quick-filter")
    filter_buttons.append(current_filter)

    # the parent <div> for the button bar, with the set of buttons
    button_bar = html.Div(className="quick-filter-button-bar", children=filter_buttons)

    return button_bar

    


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('Andrews_7-2_ProjectTwo')

app.layout = html.Div([
    html.Div(id='hidden-div'),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    create_filter_button_bar_html_element(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable="single",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[0],
        page_action="native",
        page_current=0,
        page_size=10
    ),
    html.Br(),
    html.Hr(),
    html.Div(
            id='map-id',
            className='col s12 m6',
            ),
    html.Hr(),

    # unique signature
    html.Div(id="unique-signature", children=[
        html.Img(src="/assets/glider.png", title="The Hacker Glider"),
        html.Span(" ~~ Andrew Wilson, SNHU-340, Winter 2025")
        ]),
])

    
#############################################
# Interaction Between Components / Controller
#############################################
#This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):
    dff = pd.DataFrame.from_dict(viewData)
    
    # prevent getting "Callback error updating map-id.children" on app startup when this
    # callback is run before any row is selected
    if dff.empty:
        return []

    # if no row is selected, display geolocation of the first row
    if index is None:
        row = 0
    else:
        row = index[0]
   
    # document magic column numbers
    colnum_breed = 4
    colnum_loc_lat = 13
    colnum_loc_long = 14
    colnum_name = 9

    # collect the necessary information from the selected row
    breed       =  dff.iloc[row, colnum_breed]
    animal_name =  dff.iloc[row, colnum_name]
    coordinates = [dff.iloc[row, colnum_loc_lat], dff.iloc[row, colnum_loc_long]]

    # Austin TX is at [30.75, -97.48]
    return [
        dl.Map(id="animal-location-map",
              center=[30.75, -97.48], zoom=10, 
              children=[
                  dl.TileLayer(id="base-layer-id"),
                  # Marker with tool tip and popup
                  dl.Marker(position=coordinates,
                           children=[
                               dl.Tooltip(breed),
                               dl.Popup([
                                   html.H1("Animal's Name"),
                                   html.P(animal_name)
                               ])
                           ])
              ])
    ]

# Callback for quick filter buttons:
#   inputs: all of the quick filter button n_clicked
#   outputs: data frame property of the main data table
#            a status line stating which quick filter is active
@app.callback(
    [Output('datatable-id', 'data'),                # to update the data table with filtered data
    Output('current-quick-filter', 'children')],        # to tell user which quick filter is selected
    [Input(f"quick-filter-button-{str(i)}", "n_clicks") for i in range(1, num_quick_filter_buttons + 1)],  # each quick filter button
    Input("clear-filters", "n_clicks"))             # the 'clear filter' button
def apply_quick_filter(*args):
    trigger = callback_context.triggered[0]
    clicked_button_id = trigger["prop_id"].split(".")[0]

    # TODO: remove debug breakpoint
    # import pdb; pdb.set_trace()

    # the data table's data frame
    global df
 
    # prevent callback errors during app load when no button has been clicked yet
    if clicked_button_id == "":
        return df.to_dict('records')    # don't hit the database again; no filters have been applied yet

    # retrieve the query JSON for the selected filter
    global quick_filters
    clicked_filter_query_json = quick_filters[clicked_button_id]['query-json']
    clicked_filter_name       = quick_filters[clicked_button_id]['filter-name']

    applied_filter_status_msg = ""
    if clicked_filter_name != "":
        applied_filter_status_msg = f"Current quick filter: {clicked_filter_name}"

    # re-query with the selected filter
    df = pd.DataFrame.from_records(shelter.find(clicked_filter_query_json))

    # pass the matching results back to the data table
    return (df.to_dict('records'), applied_filter_status_msg)


app.run_server(debug=True, port=8050, host="0.0.0.0")

