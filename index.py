from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app, server
from apps import about, rb_projs, wr_projs

# top navbar
navbar_header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('About', href='/about')),
        dbc.NavItem(dbc.NavLink('WR Projections', href='/wr_projs')),
        dbc.NavItem(dbc.NavLink('RB Projections', href='/rb_projs'))
        ],
    brand='Fantasy Football Crystal Ball',
    color='#1c0313',
    sticky='top',
    dark=True
)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar_header,
    html.Div(id='page-content'),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/wr_projs':
        return wr_projs.layout
    elif pathname == '/rb_projs':
        return rb_projs.layout
    else:
        return about.layout

if __name__ == '__main__':
    app.run_server()
