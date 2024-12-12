import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import pandas as pd
import numpy as np
import plotly.express as px
import colorlover

# Read in data
df_y1 = pd.read_csv('data/rb_y1_preds.csv')
df_all = pd.read_csv('data/rb_y1-y3_preds.csv')

# Helper Functions
def get_y1_data(year):
    return df_y1[df_y1.Draft_Year==year]

def get_all_data(year):
    return df_all[df_all.Draft_Year==year]

def discrete_background_color_bins(df, n_bins=9, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.selectY1-Y3_PPR_PPG_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })

    return styles

# Global Variables
years = list(range(2010,2024,1))
styles_all = discrete_background_color_bins(df_all,columns=['Y1-Y3_PPR_PPG','5%','Mean','95%'])
styles_y1 = discrete_background_color_bins(df_y1,columns=['Y1_PPR_PPG','5%','Mean','95%'])
sort_dict = {
    'Floor (5% Quantile)':'5%',
    'Mean':'Mean',
    'Ceiling (95% Quanilte)':'95%'
}

# Page Layout
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Br(),
                     html.H1("Running Back Prospect Fantasy Projections",
                            style={'textAlign': 'center'})],
                    className='mt-4')
        ]),
        dbc.Row([
            dbc.Col(html.H5("Forcasting Fantasy Football Range of Outcomes",
                            style={'textAlign': 'center'}),className='mb-4')
        ]),
        dbc.Row([
            dbc.Col([
                html.H5("Select Year:"),
                dcc.Dropdown(
                    id='rb-year-selector',
                    options=years,
                    value=2023,
                    multi=False,
                    #className='text-center'
                ),
            ],align='center'),
            dbc.Col([
                html.H5("Sort By:"),
                dcc.Dropdown(
                    id='rb-sort-selector',
                    options=['Floor (5% Quantile)','Mean','Ceiling (95% Quanilte)'],
                    value='Mean',
                    multi=False,
                    #className='text-center'
                ),
            ]),
        ],className='mb-4 mt-4 mx-4'),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H3(children='Years 1-3 PPR Points/Game Forcast',
                            className='text-center text-light '),
                    body=True, color='#1c0313'
                )
            ),
        ]),
        dbc.Row([
            dbc.Col(
                children =[
                    dcc.Loading(
                        id='rb-all-loading',
                        type='graph',
                        fullscreen=True,
                        children=[
                            dcc.Graph(
                                id='rb-all-plot',
                                style={'width': '100vh'},
                                config={'displayModeBar': False},
                            )
                        ]
                    ),
                ],
                className='mt-3 justify-content-center'
            ),
            dbc.Col([
                dash_table.DataTable(
                    id='rb-all-table',
                    sort_action='native',
                    editable=False,
                    style_data_conditional=styles_all,
                    cell_selectable=False,
                    style_table={'overflowX': 'scroll',
                        'padding': 10},
                    style_cell={
                        'color':'black',
                        'fontSize': 13,
                        'font-family': 'Nunito Sans',
                        'textAlign':'center'},
                    merge_duplicate_headers=True,
                    style_cell_conditional=[
                        {'if': {'column_id':'Y1-Y3_PPR_PPG'},
                         'width': '10%'},
                        {'if': {'column_id':'5%'},
                         'width': '10%'},
                        {'if': {'column_id':'Mean'},
                         'width': '10%'},
                        {'if': {'column_id':'95%'},
                         'width': '10%'},
                    ],
                )
            ],className='mb-4, px-4')
        ]),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Card(
                    html.H3(children='Years 1 PPR Points/Game Forcast',
                            className='text-center text-light'),
                    body=True, color='#1c0313'
                )
            ]),
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='rb-y1-plot',
                          style={'width': '100vh'},
                          config={'displayModeBar': False},
                ),
                className='mt-3 justify-content-center'
            ),
            dbc.Col([
                dash_table.DataTable(
                    id='rb-y1-table',
                    sort_action='native',
                    editable=False,
                    style_data_conditional=styles_y1,
                    cell_selectable=False,
                    style_table={'overflowX': 'scroll',
                        'padding': 10},
                    style_cell={
                        'color':'black',
                        'fontSize': 13,
                        'font-family': 'Nunito Sans',
                        'textAlign':'center'},
                    merge_duplicate_headers=True,
                    style_cell_conditional=[
                        {'if': {'column_id':'Y1_PPR_PPG'},
                         'width': '10%'},
                        {'if': {'column_id':'5%'},
                         'width': '10%'},
                        {'if': {'column_id':'Mean'},
                         'width': '10%'},
                        {'if': {'column_id':'95%'},
                         'width': '10%'},
                    ],
                )
            ],className='mb-4, px-4'),
        ]),
        dbc.Col([html.Br(),html.Br()])
    ])
])

# Callbacks
@app.callback([Output('rb-all-plot','figure'),
               Output('rb-y1-plot','figure')],
              [Input('rb-year-selector','value'),
               Input('rb-sort-selector','value')])
def update_plot(year,sort_by):
    df_all = get_all_data(year).sort_values(by=sort_dict[sort_by],ascending=True,ignore_index=True)

    fig_05 = px.scatter(df_all, y="Name", x="5%")
    fig_05.update_traces(marker=dict(size=10,symbol='line-ns',
                                   line=dict(width=2, color="black")))
   
    fig = px.scatter(df_all, y="Name", x="Mean", color='Mean',
                     color_continuous_scale='blues')
    fig.update_traces(marker=dict(size=14,line=dict(width=1,color='black')))

    fig_95 = px.scatter(df_all, y="Name", x="95%")
    fig_95.update_traces(marker=dict(size=10,symbol='line-ns',
                                   line=dict(width=2, color="black")))
    fig.add_trace(fig_05.data[0])
    fig.add_trace(fig_95.data[0])
    
    for i, row in df_all.iterrows():
        if row["5%"]!=row["95%"]:
            x = np.array([row['5%'], row['95%']])
            y = np.array([row['Name'], row['Name']])
            df_line = pd.DataFrame({'FantPPG':x,'Name':y})
            fig_line = px.line(df_line,x='FantPPG',y='Name')
            fig_line.update_traces(line_color='black')
            fig.add_trace(fig_line.data[0])

    fig_mean = px.scatter(df_all, y="Name", x="Mean", color='Mean',
                     color_continuous_scale='blues')
    fig_mean.update_traces(marker=dict(size=14,line=dict(width=1,color='black')))
    fig.add_trace(fig_mean.data[0])
    
    # modify plot shading and reduce bottom margin
    fig.update_layout({
        'plot_bgcolor': '#EBEBF1',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'margin': {'b':20}
    })
    fig.update(layout_coloraxis_showscale=False)
    fig.update_yaxes(tickangle=-20,title="",fixedrange=True)
    fig.update_xaxes(title_text='Projected Yr1-Yr3 PPR Points Per Game',
                     side='top',tickvals=np.arange(0,df_all['95%'].max()+1,1),fixedrange=True)
    fig.update_layout(height=(len(df_all)*30),
                         hoverlabel={'bgcolor':'white'})
    
    
    df_y1 = get_y1_data(year).sort_values(by=sort_dict[sort_by],ascending=True,ignore_index=True)

    fig_05_y1 = px.scatter(df_y1, y="Name", x="5%")
    fig_05_y1.update_traces(marker=dict(size=10,symbol='line-ns',
                                   line=dict(width=2, color="black")))
   
    fig_y1 = px.scatter(df_y1, y="Name", x="Mean", color='Mean',
                     color_continuous_scale='blues')
    fig_y1.update_traces(marker=dict(size=14,line=dict(width=1,color='black')))

    fig_95_y1 = px.scatter(df_y1, y="Name", x="95%")
    fig_95_y1.update_traces(marker=dict(size=10,symbol='line-ns',
                                   line=dict(width=2, color="black")))
    fig_y1.add_trace(fig_05_y1.data[0])
    fig_y1.add_trace(fig_95_y1.data[0])
    
    for i, row in df_y1.iterrows():
        if row["5%"]!=row["95%"]:
            x = np.array([row['5%'], row['95%']])
            y = np.array([row['Name'], row['Name']])
            df_line = pd.DataFrame({'FantPPG':x,'Name':y})
            fig_line = px.line(df_line,x='FantPPG',y='Name')
            fig_line.update_traces(line_color='black')
            fig_y1.add_trace(fig_line.data[0])

    fig_mean_y1 = px.scatter(df_y1, y="Name", x="Mean", color='Mean',
                     color_continuous_scale='blues')
    fig_mean_y1.update_traces(marker=dict(size=14,line=dict(width=1,color='black')))
    fig_y1.add_trace(fig_mean_y1.data[0])
    
    # modify plot shading and reduce bottom margin
    fig_y1.update_layout({
        'plot_bgcolor': '#EBEBF1',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'margin': {'b':20}
    })
    fig_y1.update(layout_coloraxis_showscale=False)
    fig_y1.update_yaxes(tickangle=-20,title="",fixedrange=True)
    fig_y1.update_xaxes(title_text='Projected Yr1 PPR Points Per Game',
                     side='top',tickvals=np.arange(0,df_y1['95%'].max()+1,1),fixedrange=True)
    fig_y1.update_layout(height=(len(df_y1)*30),
                         hoverlabel={'bgcolor':'white'})

    return fig, fig_y1


@app.callback([Output('rb-all-table','data'),
               Output('rb-all-table','columns'),
               Output('rb-y1-table','data'),
               Output('rb-y1-table','columns')],
              [Input('rb-year-selector','value'),
               Input('rb-sort-selector','value')])
def update_table(year,sort_by):
    df_all = get_all_data(year).sort_values(by=sort_dict[sort_by],ascending=False,ignore_index=True)
    df_all['Y1-Y3_PPR_PPG']=df_all['Y1-Y3_PPR_PPG'].map("{:,.2f}".format)
    data_all = df_all.to_dict('records')
    columns_all=[
        {'name':['','Name'],'id':'Name'},
        {'name':['Team','College'],'id':'School'},
        {'name':['Team','NFL'],'id':'Landing_Team'},
        {'name':['','Actual PPR PPG Years 1-3'],'id':'Y1-Y3_PPR_PPG'},
        {'name':['Projected PPR PPG Years 1-3','5th Percentile'],'id':'5%'},
        {'name':['Projected PPR PPG Years 1-3','Mean'],'id':'Mean'},
        {'name':['Projected PPR PPG Years 1-3','95th Percentile'],'id':'95%'}
    ]

    df_y1 = get_y1_data(year).sort_values(by=sort_dict[sort_by],ascending=False,ignore_index=True)
    df_y1['Y1_PPR_PPG']=df_y1['Y1_PPR_PPG'].map("{:,.2f}".format)
    data_y1 = df_y1.to_dict('records')
    columns_y1=[
        {'name':['','Name'],'id':'Name'},
        {'name':['Team','College'],'id':'School'},
        {'name':['Team','NFL'],'id':'Landing_Team'},
        {'name':['','Actual PPR PPG Years 1'],'id':'Y1_PPR_PPG'},
        {'name':['Projected PPR PPG Years 1','5th Percentile'],'id':'5%'},
        {'name':['Projected PPR PPG Years 1','Mean'],'id':'Mean'},
        {'name':['Projected PPR PPG Years 1','95th Percentile'],'id':'95%'}
    ]
    
    return data_all, columns_all, data_y1, columns_y1

@app.callback(Output('rb-all-loading','children'),Input('rb-all-plot','value'))
def loading_wr_all_plot(value):
    time.sleep(1)
    return value


