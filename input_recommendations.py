import os

from dash import Dash
import dash_table as dt
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from recommender_sys_for_input import *

# suppressing chained calculation warnings, comment if you want them to reappear for checks
pd.set_option('mode.chained_assignment',None)

path = os.path.dirname(os.path.abspath(__file__))

# set filename
infile = "/organisation-test.xlsx"

# create df
df = pd.read_excel(path+infile, usecols = "A:U", engine='openpyxl') 

# filter for only open tasks
open_tasks = df[(df['Status']!='Deprecated')&(df['Status']!='Done')]


top_n = 7

########## future: could also take comments and first step into account? ###########

# reduce amount of columns to only few ones and match based on title for now 
open_tasks = open_tasks[['ID','Name','Deadline']]


static_view_title = open_tasks['Name'].iloc[0]

static_recommendation = initialize_frame_for_recommender(open_tasks,
                                            static_view_title,'Name',top_n)

# prototype which is always displayed
static_view_open_tasks = open_tasks.head(top_n)



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#### HOW TO MAKE DATA TABLE INVISIBLE BY DEFAULT?

app.layout =    dbc.Container([
                    dbc.Row([
                        html.Div([
                        
                        html.Div([
                            dcc.Input(id='input-1-submit', type='text', placeholder='What do you feel like doing?', 
                            # using autocomplete here to let the browser make a judgment
                            autoComplete='on', style={'width': '74%','display': 'inline-block'}),
                            html.Button('Submit', id='btn-submit', style={'width': '26%','display': 'inline-block'}),
                        ]),
                        ### ALSO POSSIBLY CREATE SOME VERTICAL DISTANCE HERE
                        html.Div(
                        [
                            html.Div(
                                [  
                                    html.H3(id='task_recommendations_title',
                                            children=f'Top {top_n} Recommendations for "{static_view_title}"',
                                            style={'margin-right': '2em'})
                                ],
                            ),
                            html.Div([
                                        ############################################
                                        ### Dash DataTable for spreadsheet view ####
                                        ############################################
                            dt.DataTable(
                                id = 'task_recommendations_table',
                                # start with the static recommendation first
                                data = static_recommendation.to_dict('records'),
                                # display task ID and name 
                                columns=[{'id': c, 'name': c} for c in static_recommendation.columns],
                                style_as_list_view=True,
                                style_cell={'padding': '5px'},
                                style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                                # align these cells left
                                style_cell_conditional=[
                                    {
                                        'if': {'column_id': c},
                                        'textAlign': 'left'
                                    } for c in ['Name', 'Deadline', 'first step filled']
                                ],
                            ) 
                            ]),

                            ######## ALTERNATIVE WAY OF DISPLAYING RECOMMENDATIONS? E.G. THROUGH SCATTER / BUBBLEPLOT?

                        ]
                        ),
                        html.Br(), html.Hr()
                        ])
                    ], justify="center", align="center", className="h-50"
                    )
                    ],style={"height": "100vh"})

                    

### update the DataTable data###
@app.callback(
    Output('task_recommendations_table', 'data'),
    Output('task_recommendations_title', 'children'),
    [Input('btn-submit', 'n_clicks')],
    [State('input-1-submit', 'value')])
def update_data_table(clicked, value):

    """
    Creates new recommendations based on the selected value in the dropdown.
    
    Args:
    n_clicks (int): amount of clicks on submit
    value (string): Name of the task

    Returns:
    df (Dict): df of recommendations in format Dictionary for Dash DataTable
    """

    # always check this for no selection
    if not clicked:

        title = f'Top {top_n} Recommendations for "{static_view_title}"'
        table_data = static_recommendation.to_dict('records')

        return table_data, title

    if clicked:

        print(f'this is our current value: {value}')

        new_recommendations = initialize_frame_for_recommender(open_tasks,
                                                value ,'Name',top_n, True)

        new_recommendations.reset_index(drop = True, inplace=True)

        recommendations_title = f'Top {top_n} Recommendations for "{value}"'

        # setting values for integrating the data from dataframe into the datatable
        return new_recommendations.to_dict('records'), recommendations_title

if __name__ == '__main__':
    app.run_server(debug=True)