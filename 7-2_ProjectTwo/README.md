# CS 340 Project Two: ShelterSight

## What is it?

**ShelterSight** is a Dash-based dashboard web app for filtering, sorting,
and visualizing animal shelter records.

It uses simple YAML files for database connection config and defining
custom quick filters. It shows recorded animal locations on a map and
includes a pie chart to provide insight for the composition of breeds
that match the current filter.

## See it in Action

![Lists the directory files.
Opens `db.yml` and `quick-filters.yml` in a text editor. 
Opens app. Activates each quick filter. Demonstrates 
map pinpoint. Edits `quick-filters.yml` to add a filter.
Demonstrates new filter.](screencast.gif "ShelterSight Screencast")

## Installation

ShelterSight requires **Python 3**, a running **MongoDB** backend server, and
 Python modules **jupyter-notebook, dash, jupyter_dash, dash_leaflet, plotly, 
  pyyaml, pymongo,** and **pandas**.

1. **Install Python 3.x**
   * Download and install it from [the Python official website](https://neovim.io/)
2. **Install MongoDB**
   * Follow MongoDB's [official guide](https://www.mongodb.com/docs/manual/installation/)
3. **Install dependencies**
   * Using `pip`:
   
     `pip install jupyter-notebook dash dash-leaflet jupyter-dash plotly pandas pymongo pyyaml`

   * Using `conda`:
   
     `conda install jupyter-notebook dash dash-leaflet jupyter-dash plotly pandas pymongo pyyaml`
4. **Clone the repo**
   * `git clone https://github.com/aldonadi/cs340_projecttwo`

## Configuration

### Server Connection and Authentication

Edit the `db.yml` with configuration for your MongoDB server:
```yml
# Server connection details
hostname: nv-desktop-services.apporto.com
port: 32471

# Credentials
username: aacuser
password: i3-bNzTV6OF#V-'a00e+=iKh&JQs

# Name of the shelter database
db_name: AAC

# Name of the document containing shelter documents
collection_name: animals
```

## Running 

1. Start `jupyter-notebook`
2. Open `ShelterSight.ipynb` or `ProjectTwoDashboard.ipynb`
3. Run the first code block.
4. Navigate your web browser to http://localhost:8050

## Creating new quick filters

Edit the `quick-filters.yml` file to edit or create new quick filter buttons.

```yaml
# Quick Filter buttons
- Water Rescue:                 # text to be shown on the button
    breeds:                     # match any of these breed substrings (e.g. "Chesa" matches "Chesapeake"t
      - Labrador Retriever Mix
      - Chesa
      - Newfoundland
    sex: Intact Female          # match this 'sex_upon_outcome'
    min-age-in-weeks: 26        # 'age_upon_outcome_in_weeks' must be greater than or equal to this
    max-age-in-weeks: 156       # 'age_upon_outcome_in_weeks' must be less than or equal to this
```

The `breeds` array holds substrings. In fact, these are strings are actually placed in
regular expression string like `(Lab|Chesa|Newfoundland)`, so you can use some regex
notation if you like.

## Design Decisions

This app loosely follows the "Model/View/Controller" structure.

MongoDB is used as the backend because it makes it much easier to store
unstructured data and map database objects to programming objects. It is
also built to be scalable moreso than relational databases. MongoDB is also
free for use and has a great body of documentation.

Module `pymogno` is used as the Python/MongoDB interface. It provides a thin
API wrapper using `dict`s that makes it easy to write conventional Mongo code
that just works in Python.

The `aac_crud_driver.py` is the database layer and model. It packages search
queries into `dict`s and calls the relevant `pymongo` API. Results are stored
in `pandas` `DataFrame`s since these are portable, fast, and have a ton of
built-in functionality.

The UI uses the `Dash` framework for organizing and integrating the visual
elements. Dash provides a simple and powerful API for quickly creating interfaces.
The "View" is made up of a tree of `dash.html.Div` elements that are given
IDs to be referenced.

The "Controller" aspect is made of several dash `@callback` methods. Dash
automatically monitors the connected input fields, executes the appropriate 
callbacks, and puts the output in the proper places.

# Development

I used **git** for version control, which was essential for my over 240 commits. Being
able to cheaply branch out, work on a potential feature and abandon it without
disturbing the "good state" code made it much easier to experiment. I used 
**[neovim](https://neovim.io/)** primarily as my text editor. The 
**[pyright](https://github.com/microsoft/pyright)** and 
**[coc](https://github.com/neoclide/coc.nvim)** plugins turn neovim into a full-fledged
Python IDE.

I pulled the Jupyter notebook Python code out into a simply Python file and used that
for testing, since editing Jupyter notebook code in a regular text editor is...not at
all convenient.

## Challenges

I came to the Dash framework with experience in other frameworks, and tried to 
implement the visual effects I wanted without first taking time to understand 
how Dash works. This resulted in me spending a lot of time fighting against Dash,
trying to force my way instead of working with it. For example, for the quick
filter button styling effect, where the active filter is given an additional CSS
class attribute, my first approach was to look up the button element by ID and 
manually edit the `className` property. However, in the version of Dash that I
used in development, there was no public API provided to make this simple. I 
spent too much time reverse-engineering the Dash internal interfaces and methods
trying to write my own hooks into the guts of the library. In the end, I finally
realized I could just return the class names of all buttons as another output from
the callback method. Once I began to work *with* the framework instead of *against*
it, the development process was more pleasant. (*Note: editing the properties of
arbitrary Dash elements was added in
[Dash v2.17.0](https://github.com/plotly/dash/releases/tag/v2.17.0)*).

Another difficult aspect was trying to keep my code modular, clean, and easy to
follow. I am still see many opportunities for tidying up and encapsulating more 
concerns into their own classes. For example, the guts of the Button Bar are 
currently scattered throughout the main app. I would much rather package that up
into its own class that provides a clean API for the app layout code to call and
connect to callbacks. I do have a branch with about a day of development toward that
end, but I ran out of time.

Finally, the screencast was much more difficult than I anticipated. From developing
the script, practicing the sequence, setting up the files for best presentation,
running through a dozen or so takes with mistakes, needing to re-do the recording
after making UI changes to the app, I probably spent 4 hours in total working on 
the screen recording.

## Links

* https://www.mongodb.com/
* https://dash.plotly.com/
* https://www.dash-leaflet.com/
* https://pandas.pydata.org/
* https://neovim.io/
* https://github.com/microsoft/pyright
* https://github.com/neoclide/coc.nvim

## TODO / Roadmap

See [TODO.md](./TODO.md)

## Contact

Andrew Wilson
