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


#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from aac_crud_driver import AnimalShelter

###########################
# Data Manipulation / Model
###########################

# server configuration and credentials are managed in the `db.yml` file

db = AnimalShelter()


# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.find({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

# DEBUG
# print(df)

#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

app.layout = html.Div([
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    html.Div(className='buttonRow', 
            style={'display' : 'flex'},
                children=[
                    html.Button(id='submit-button-one', n_clicks=0, children='Cats'),
                    html.Button(id='submit-button-two', n_clicks=0, children='Dogs')
                ]),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True}
                                  for i in df.columns],
                         data=df.to_dict('records'),
                         editable=False,
                         filter_action="native",
                         sort_action="native",
                         sort_mode="multi",
                         column_selectable=False,
                         row_selectable=False,
                         row_deletable=False,
                         selected_columns=[],
                         selected_rows=[],
                         page_action="native",
                         page_current=0,
                         page_size=10
                        ),
    html.Br(),
    html.Hr()
])

#############################################
# Interaction Between Components / Controller
#############################################
@app.callback(Output('datatable-id', "data"),
             [Input('submit-button-one', 'n_clicks'),
              Input('submit-button-two', 'n_clicks')
             ])
def on_click(button1, button2):
    # start case
    df = pd.DataFrame.from_records(db.find({}))
    
    # use higher number of button clicks to determine filter type, can you think of a better way? ...
    if (int(button1) > int(button2)):
        df = pd.DataFrame.from_records(db.read({"animal_type" : "Cat"}))
    elif (int(button2) > int(button1)):
        df = pd.DataFrame.from_records(db.read({"animal_type" : "Dog"}))
    
    # Cleanup Mongo _id field
    df.drop(columns=['_id'],inplace=True)
    return df.to_dict('records')

app.run_server(debug=True)

