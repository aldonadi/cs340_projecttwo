# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output


# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# For logging long-running queries
import time

# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from aac_crud_driver import AnimalShelter


###########################
# Data Manipulation / Model
###########################

# use credentials and DB connection details stored in `db.yml` instead of hardcoded
shelter = AnimalShelter()

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


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('Andrews_6-1_MilestoneApp')

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    html.Div(className='buttonRow', children=[html.P("quick filters")]),

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
        dl.Map(style={'width': '1000px', 'height': '500px'},
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
    

app.run_server(debug=True)

