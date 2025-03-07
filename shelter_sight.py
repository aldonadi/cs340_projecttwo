# ProjectTwoDashboard - ShelterSight Web Dashboard
#
# Andrew Wilson, SNHU, CS-340 Winter 2025
#
# Professor: Dr. James Webb
#
# 7-2 Project Two
#
# Due 2/23/2025

# Set up the Jupyter version of Dash
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
import pandas as pd

# For logging long-running queries
import time

# driver to interface with MongoDB backend server
from aac_crud_driver import AnimalShelter

# for loading quick filter buttons from the quick-filters.yml file
from quick_filter_buttons import QuickFilters

###########################
# Data Manipulation / Model
###########################

# use credentials and DB connection details stored in `db.yml` instead of hardcoded
shelter = AnimalShelter()

# quick filter button query JSONs
quick_filters = {}

# number of quick-filter buttons for purposes of the callback
# (will be calculated during button generation)
num_quick_filter_buttons = 0

# class read method ('find' in my CRUD driver implementation) must support return
# of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
print("Retrieving all records...", end="")
start_time = time.time()
# NOTE: Database Hit
df = pd.DataFrame.from_records(shelter.find({}, limit=20))  # TODO: remove the record limit for production
end_time = time.time()
total_time = end_time - start_time
total_records = len(df.to_dict(orient='records'))
print(f"obtained {total_records} records in {total_time:.2f} seconds.")


# dropping the '_id' field is not necessary for my CRUD driver because my 'find'
# implementation does not return the '_id' field unless the 'find' method
# optional argument 'include_id' is set to True

def create_filter_button_bar_html_element():
    """
    Uses the quick filters defined in the YAML file and creates a bar of
    buttons that can be clicked to enable the given quick filter.
    """

    # load the quick filter data from the quick-filters.yml file
    filters = []
    try:
        filters = QuickFilters.load()
    except Exception as e:
        # if there is an error, the app continues, but no quick filter buttons
        # will be displayed
        print(f"Error loading quick filters: {e}")
        return []

    # TODO: restructure to not need these kludgy global variables
    global quick_filters
    global num_quick_filter_buttons
    num_quick_filter_buttons = len(filters)

    # the array of button HTML elements that will be generated
    filter_buttons = []
    button_number = 1
    for filt in filters:
        #  to identify which button was clicked in the callback
        button_id = f"quick-filter-button-{button_number}"

        # My first idea was to use the callback to identify which button ID was
        # clicked (I have figured this part out) and then to pull the 'data-query'
        # attribute out of the clicked button (I cannot figure out how to do this)
        # Instead, I am storing the query filter JSON in a global dict (not ideal)

        # create and add the button HTML element for this quick filter
        button = html.Button(
            filt.name,  # button text
            className="quick-filter",  # for CSS styling
            id=button_id,
            n_clicks=0)

        filter_buttons.append(button)

        # add the filter's query JSON and name to the lookup dict
        quick_filters[button_id] = {
            'filter-name': filt.name,
            'query-json': filt.query_json()
        }

        button_number += 1

    # add the final "Clear Filters" button
    button = html.Button(
        children="Clear Filters",
        className="quick-filter",
        id="clear-filters",
        n_clicks=0
    )

    filter_buttons.append(button)
    # TODO: fix this kludgy mess: associate filter json with button ID
    quick_filters["clear-filters"] = {'filter-name': '', 'query-json': {}}

    # the parent <div> for the button bar, with the set of buttons
    button_bar = html.Div(className="quick-filter-button-bar", children=filter_buttons)

    return button_bar


def get_quick_filter_button_classnames(clicked_button_id, total_buttons):
    """
    Based on the given clicked button id string and the total number of buttons,
    returns a list of CSS class names, one per button, such that only the selected
    button gets the extra 'selected' class for styling.
    """
    class_names = []
    for i in range(1, total_buttons + 1):
        button_id = f"quick-filter-button-{i}"
        if button_id == clicked_button_id:
            class_names.append("quick-filter selected")
        else:
            class_names.append("quick-filter")

    return class_names


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('Andrews_7-2_ProjectTwo')

app.layout = html.Div([
    html.Div(id='hidden-div'),
    html.Div(className="top-header", children=[
        html.Div(className="logo", children=html.Img(src="assets/grazioso-salvare-logo.png")),
        html.Div(className="header-text", children=(html.H1('SNHU CS-340 Dashboard')))
    ]),
    html.Hr(),
    create_filter_button_bar_html_element(),
    html.Div(className="data-table", children=
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
    )
             ),
    html.Br(),
    html.Hr(),
    html.Div(className="viz", children=[
        html.Div(
            id='breed-chart-container',
            className='breed-chart'),
        html.Div(
            id='animal-location-map-container',
            className='location-map')
    ]),
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
# This callback will highlight a row on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geolocation chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in
# the form of a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the
# form of a list. For this application, we are only permitting single row
# selection so there is only one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('animal-location-map-container', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(view_data, index):
    # the map should always be displayed, even if no record is selected
    animal_map = dl.Map(
        id="animal-location-map",
        center=[30.75, -97.48],    # Austin TX is at [30.75, -97.48]
        zoom=8,   # TODO: ensure dropped pins are never offscreen
        children=[dl.TileLayer(id="base-layer-id")]
    )

    # get the DataFrame representing data currently visible in the table
    dff = pd.DataFrame.from_dict(view_data)

    # only create the map marker/pin if records are shown in the current filter
    # and if one is selected
    if not dff.empty:
        # if no row is selected, display geolocation of the first row
        if index is None:
            row = 0
        elif not index:
            row = -1
        else:
            row = index[0]

        # document magic column numbers
        colnum_breed = 4
        colnum_loc_lat = 13
        colnum_loc_long = 14
        colnum_name = 9

        # collect the necessary information from the selected row
        breed = dff.iloc[row, colnum_breed]
        animal_name = dff.iloc[row, colnum_name]
        coordinates = [dff.iloc[row, colnum_loc_lat], dff.iloc[row, colnum_loc_long]]

        # create and add the map marker
        marker = dl.Marker(position=coordinates,
                           children=[
                               dl.Tooltip(breed),
                               dl.Popup([
                                   html.H1("Animal's Name"),
                                   html.P(animal_name)
                               ])
                           ])

        animal_map.children.append(marker)


    return [animal_map]


# This callback will update the breed composition pie chart whenever the list
# of visible records change (due to a new query or live-filtering in the table)
@app.callback(
    Output('breed-chart-container', "children"),
    Input('datatable-id', "derived_virtual_data"))
def update_breed_chart(view_data):
    MAX_BREEDS_IN_PIE_CHART = 15

    # get a DataFrame representing the visible filtered records
    dff = pd.DataFrame.from_dict(view_data)

    # if there are no records visible, show a message to the user instead of a pie chart
    if len(dff) == 0:
        return html.Div(
            children="Sorry, can't show a pie chart since no records match the current filters.",
            className="empty-breed-chart"
        )

    # get the frequency counts of breeds from the currently-shown table data
    breed_frequencies = dff['breed'].value_counts()

    # to prevent super unwieldy pie charts with hundreds of slices,
    # keep ONLY the top 15 and lump the rest into "Other breeds"
    if len(breed_frequencies) <= MAX_BREEDS_IN_PIE_CHART:
        # at most 15 breeds are shown, so there is no need to consolidate
        displayed_breeds = breed_frequencies.index
        displayed_counts = breed_frequencies.values

    else:  # too many breeds; consolidate
        # get just the top most-frequent breeds
        top_breed_freqs = breed_frequencies.head(MAX_BREEDS_IN_PIE_CHART)

        # calculate how many breeds are NOT in the top
        total_breed_count = breed_frequencies.sum()
        top_breed_count = top_breed_freqs.sum()
        other_breed_count = (total_breed_count - top_breed_count)

        # pull out the top breed names and counts
        displayed_breeds = list(top_breed_freqs.index)
        displayed_counts = list(top_breed_freqs.values)

        # add the "Other breeds" category at the end
        displayed_breeds.append("Other breeds")
        displayed_counts.append(other_breed_count)

    # create the pie chart
    pie_chart = px.pie(names=displayed_breeds, values=displayed_counts, hole=0.3)

    # make hover show something prettier than 'label=Poodle\nvalue=67'
    pie_chart.update_traces(hovertemplate="%{label}<br>%{value} records<extra></extra>")

    # make the chart use more of its Div space and share its space with the map
    pie_chart.update_layout(margin=dict(t=5, b=5, l=5, r=5), autosize=True)

    return dcc.Graph(id="breed-chart", figure=pie_chart)


# Callback for quick filter buttons:
# Based on which button was clicked, it requiries the backend database with the
# specific query for that button. It also updates the button classes so that
# active button can get special "active filter" styling
@app.callback(
    [Output('datatable-id', 'data'),
     [Output(f"quick-filter-button-{str(i)}", "className") for i in range(1, num_quick_filter_buttons + 1)]
     ],
    [Input(f"quick-filter-button-{str(i)}", "n_clicks") for i in range(1, num_quick_filter_buttons + 1)],
    Input("clear-filters", "n_clicks"))
def apply_quick_filter(*args):  # variable args due to having an unknown number of filter buttons

    # use callback_context to determine which button was clicked
    # I used this approach rather than the conventional "n_clicked" because I
    # was trying to obtain the button ID and its query without needing to store
    # a bunch of global variables like `quick_filters`. I ended up failing to
    # implement my scheme due in part to this project using older versions of
    # dash.
    trigger = callback_context.triggered[0]
    clicked_button_id = trigger["prop_id"].split(".")[0]  # get the clicked button's id

    # the data table's data frame
    global df

    # returns "quick-filter" class for all buttons, with the active button
    # getting the "quick-filter selected" classes.
    quick_filter_button_classnames = get_quick_filter_button_classnames(clicked_button_id, num_quick_filter_buttons)

    # prevent callback errors during app load when no button has been clicked yet
    if clicked_button_id == "":
        return [df.to_dict('records'),
                quick_filter_button_classnames]  # don't hit the database again; no filters have been applied yet

    # retrieve the query JSON for the selected filter
    global quick_filters
    clicked_filter_query_json = quick_filters[clicked_button_id]['query-json']

    # re-query with the selected filter
    # NOTE: Database Hit
    df = pd.DataFrame.from_records(shelter.find(clicked_filter_query_json))

    return [df.to_dict('records'), quick_filter_button_classnames]


app.run_server(debug=True, port=8050, host="localhost")
