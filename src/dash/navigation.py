import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import dash

items_style = {
    'font-family': 'arial',
    'margin-top':'0.8%',
    'margin-left':'2%'
}
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavbarBrand("Mountain Stats", style={"font-size": "150%", 'margin-left': '-15%', 'vertical-align':'middle'}),
        dbc.NavItem(dbc.NavLink("Home", href="/"), style=items_style),
        dbc.NavItem(dbc.NavLink("Yearly Stats", href="/Yearly_Stats"), style=items_style),
        dbc.NavItem(dbc.NavLink("Run", href="/Run_Stats"), style=items_style),
        dbc.NavItem(dbc.NavLink("Ride", href="/Ride_Stats"), style=items_style),
        dbc.NavItem(dbc.NavLink("Strength/Climbing", href="/Strength_Stats"), style=items_style)
    ],
    color="#FF8303",
    dark=True,
    links_left=True
)