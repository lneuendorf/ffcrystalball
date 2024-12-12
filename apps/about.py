import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import pandas as pd

df = pd.read_csv("data/scoring.csv")

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                children = [
                    html.Br(),
                    html.Br(),
                    html.H1("Who am I?"),
                    html.P("My name is Luke Neuendorf. I am an aspiring Data Scientist \
                            and fantasy football fanatic. I am a student at \
                            UW-Madison pursing masters degree in machine \
                            learning."),
                    html.Br(),
                    html.H1("What's the goal of this project?"),
                    html.P("When I started making fantasy football rooki \
                           projections, I generated a singuar number, a players \
                           mean projected fantasy points. The problem is this \
                           does not show a players broader range of outcomes. \
                           This is why I incoperated quantile regression, which \
                           captures 90% of a players possible outcomes from the \
                           5th to 95th quantile. This can help demonstrate \
                           which prospects are more volitile and have a higher \
                           'cieling'."),
                    html.Br(),
                    html.H1("What was the modeling process?"),
                    html.P(
                        children=[
                            "Warning, this section gets into the weeds. ",
                            "I used a combination of ",
                            dcc.Link("Peter Howard's",
                                     href='https://twitter.com/pahowdy',
                                     target='_blank'),
                            " Prospect Database and ",
                            dcc.Link("FantasyData's",
                                     href="https://fantasydata.com/",
                                     target='_blank'),
                            " NFL Database as my dataset. Since the wide \
                            receiver and running back datasets are small, \
                            overfitting is a problem. To counteract this, I \
                            eliminated features that had a high Variable \
                            Inflation Factor (VIF, a measure of \
                            multicollinearity) and I used early \
                            stopping when training the models.",
                            html.Br(),html.Br(),
                            "For the quantile regression, I used gradient \
                            boosting with a pinball loss function. For the mean \
                            regression, I used XGBoost with a mean absolute \
                            error (MAE) loss function. I choose a mean absolute \
                            error loss function over the more typical mean square \
                            error (MSE) loss function because there are many outliers \
                            in the dataset, and I didn't want the model to focus \
                            on reducing outlier error. Furthermore, MAE is \
                            easier to interpret. In this instance, the MAE is \
                            the average of the differences between actual and \
                            predicted NFL fantasy points per game. I also \
                            trained a baseline model using linear regression \
                            with NFL draft pick as the only feature. This \
                            provided a good way to benchmark the model results. \
                            In the below table are the error metrics of each of \
                            the regression to the mean models. A smaller MAE is \
                            better."
                        ]),
                    dash_table.DataTable(
                        data = df.to_dict('records'),
                        columns=[
                            {'name':['',''],'id':'category'},
                            {'name':['Wide Reciever','Yr1 Model'],'id':'wr_y1'},
                            {'name':['Wide Reciever','Yr1-Yr3 Model'],'id':'wr_y1-y3'},
                            {'name':['Running Back','Yr1 Model'],'id':'rb_y1'},
                            {'name':['Running Back','Yr1-Yr3 Model'],'id':'rb_y1-y3'},
                        ],
                        style_cell={
                            'color':'black',
                            'font-family':'Nunito Sans',
                            'textAlign':'center'},
                        editable=False,
                        cell_selectable=False,
                        merge_duplicate_headers=True,
                    ),
                    html.P(
                        children=[
                            html.Br(),
                            "The notebooks containing the model code can be found ",
                            dcc.Link("here",
                                     href='https://github.com/lneuendorf/NFL_Prospect_Models/tree/main',
                                     target='_blank'),
                            "."
                        ]),
                ],
                className='mx-5'
            )
        ]),
        dbc.Row([html.Br(),html.Br()]),
    ]),
])
