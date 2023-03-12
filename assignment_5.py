from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
# from jupyter_dash import JupyterDash
import seaborn as sn
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output

mpg= sn.load_dataset('mpg')

# Define the graphs
fig1 = px.scatter(mpg, x="horsepower", y="mpg",
                 animation_frame="model_year",
                 animation_group="origin",
                 size="weight", color="origin", hover_name="name",
                 log_x=True, size_max=45, range_x=[30,250], range_y=[0,60])

cylinders_count = mpg.groupby(['cylinders'])['mpg'].count().reset_index(name='count')
cylinders_count['stage'] = cylinders_count['cylinders'].astype(str) + ' cylinders'
fig2 = px.funnel(cylinders_count, x='count', y='stage')

mpg_count = mpg.groupby(['model_year', 'origin'])['mpg'].count().reset_index(name='count')
fig3 = px.area(mpg_count, x='model_year', y='count', color='origin', line_group='origin')

mpg_mean = mpg.groupby(['model_year', 'origin'])['mpg'].mean().reset_index(name='mean_mpg')
fig4 = px.line(mpg_mean, x='model_year', y='mean_mpg', color='origin', line_group='origin', hover_name='origin',
        line_shape="spline", render_mode="svg")

fig5 = px.scatter(mpg, x='horsepower', y='mpg', color='model_year', hover_name='name',
                 size='weight', facet_col='origin', log_x=True, size_max=15,
                 range_x=[20, 250], range_y=[5, 50])


# Define the dropdown options
dropdown_options = [
    {'label': 'Figure 1', 'value': 'fig1'},
    {'label': 'Figure 2', 'value': 'fig2'},
    {'label': 'Figure 3', 'value': 'fig3'},
    {'label': 'Figure 4', 'value': 'fig4'},
    {'label': 'Figure 5', 'value': 'fig5'}
]

# Define the app
app = Dash(__name__)

# Define the app layout with a dropdown menu and a div for displaying the selected figure
app.layout = html.Div(children=[
    html.H1(children='Assignment: 5'),
    html.Div(children='''
                Visualizations using Dash :A web application framework for your data.
            '''),
    dcc.Markdown('''
                # Dropdown for all the visualizations using DCC
            '''),
    dcc.Dropdown(
        id='dropdown',
        options=dropdown_options,
        value='fig5'
    ),
    dcc.Markdown('''
             # Slider for all the visualizations using DCC
            '''),
    dcc.Slider(
        id='slider',
        min=1,
        max=5,
        step=1,
        value=1,
        marks={
            '1': {'label': 'Graph 1'},
            '2': {'label': 'Graph 2'},
            '3': {'label': 'Graph 3'},
            '4': {'label': 'Graph 4'},
            '5': {'label': 'Graph 5'},
        }
    ),
    html.Div(id='figure-container')
])

@app.callback(Output('figure-container', 'children'),
              Input('dropdown', 'value'),
              Input('slider', 'value'))
def update_figure(selected_value, slider_value):
    fig = None
    if selected_value == 'fig1' or slider_value == 1:
        fig = fig1
    elif selected_value == 'fig2' or slider_value == 2:
        fig = fig2
    elif selected_value == 'fig3' or slider_value == 3:
        fig = fig3
    elif selected_value == 'fig4' or slider_value == 4:
        fig = fig4
    elif selected_value == 'fig5' or slider_value == 5:
        fig = fig5
    return dcc.Graph(id='figure', figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)