import pandas as pd
from functools import reduce
import plotly.express as px
import plotly.graph_objects as go

# DATA = pd.read_csv('/data/processed_activities.csv')
NON_AEROBIC = ['AlpineSki', 'WeightTraining', 'Workout', 'RockClimbing']
STRENGTH = ['WeightTraining', 'RockClimbing']
MONTHS = {
        "month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    }
FONT = 'Open Sans, Light 300'
TITLE_FONT = 'Open Sans, Medium 500'
COLORS = {
    'background': '#FEDEBE',
    'yellow': '#FFAF42',
    'light orange': '#FF8303',
    'orange': '#FE6E00',
    'dark orange': '#FD5602',
    'red': '#DF2400'
}
TABLE_HEADER_PROPS = {
    'fill_color': '#FF8303',
    'align': 'left',
    'line_color': 'white',
    'font': dict(color='white', size=13, family=TITLE_FONT)
}
TABLE_PROPS = {
    'fill_color': '#FEDEBE',
    'align': 'left',
    'line_color': 'white',
    'height': 30,
    'font': dict(color='black', size=11, family=FONT)
}
BAR_PROPS = {
    'bg_color': '#FEDEBE',
    'bar_color': '#FF8303',
    'font': FONT,
    'height': 400
}


def create_indicator(dataframe, agg, column):
    tile = go.Figure()
    tile.add_trace(go.Indicator(
        mode = "number",
        value = 300,
        domain = {'row': 0, 'column': 1}
        )
    )

def max_elevation_scatter_plot(dataframe):
    plot_cols = ['month', 'day_of_month', 'year', 'name', 'type', 'hours', 'elevation']
    sort_cols = ['day_of_month', 'month', 'elevation']
    dups_cols = ['day_of_month', 'month']
    plot_data = dataframe.loc[~dataframe['type'].isin(NON_AEROBIC)]
    
    scatter = px.scatter(
        plot_data.sort_values(by=sort_cols, ascending=False).drop_duplicates(subset=dups_cols)[plot_cols], 
        x='month', 
        y='day_of_month', 
        color='elevation', 
        size='hours',
        custom_data=['year', 'name', 'elevation', 'type'],
        category_orders=MONTHS
    )
    scatter.update_traces(
        hovertemplate="<br>".join([
            "Name: %{customdata[1]}",
            "Type: %{customdata[3]}",
            "Date: %{x} %{y}, %{customdata[0]}",
            "Elevation: %{customdata[2]}",
        ])
    )
    return scatter


def stacked_bar_by_month(dataframe, y=None, title=None, color=None):
    df = dataframe
    barchart = px.bar(
        df, 
        x="month", 
        y=y, 
        title=title, 
        color=color,
        custom_data=['year'],
        category_orders=MONTHS
    )
    barchart.update_traces(
        hovertemplate="<br>".join([
            "Month: %{x}",
            "Year: %{customdata[0]}",
            "Elevation: %{y:,}"
        ])
    )
    return barchart


def table(dataframe, cols=[], title=None):
    df = dataframe
    df = df.loc[:, cols]
    df.loc[df.name.str.len() > 38, 'name'] = df.loc[df.name.str.len() > 38, 'name'].str.slice(0,35) + '...'
    table = go.Figure(
        data=[
            go.Table(
                columnwidth = [45, 10, 15, 20],
                header=dict(
                    values=list(df.columns),
                    fill_color=TABLE_HEADER_PROPS['fill_color'],
                    align=TABLE_HEADER_PROPS['align'],
                    line_color=TABLE_HEADER_PROPS['line_color'],
                    font=TABLE_HEADER_PROPS['font']
                    
                ),
                cells=dict(
                    values=[df[col] for col in df.columns],
                    fill_color=TABLE_PROPS['fill_color'],
                    align=TABLE_PROPS['align'],
                    line_color=TABLE_PROPS['line_color'],
                    font=TABLE_PROPS['font'],
                    height=TABLE_PROPS['height']
                ))])
    table.update_layout(
        margin = dict(l=10, r=10, t=30, b=2),
        title = dict(text=title, y=0.99, x=0.025, font=dict(color='black')),
        title_font_family=TITLE_FONT
    )
    return table


def bar_chart_by_week(dataframe, x=None, y=None, title=None):
    df = dataframe
    barchart = px.bar(
        df, 
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=[BAR_PROPS['bar_color']] * len(df)
    )
    barchart.update_layout(
        margin=dict(l=20, r=10, t=35, b=2),
        plot_bgcolor=BAR_PROPS['bg_color'],
        font_family=BAR_PROPS['font'],
        title_font_family=TITLE_FONT,
        xaxis_title='',
        yaxis_title='',
        height=BAR_PROPS['height'],
        xaxis_type='category'
    )
    barchart.update_yaxes(
        ticksuffix=' ',
        tickfont=dict(size=11)
    )
    barchart.update_xaxes(
        tickprefix=' ',
        tickfont=dict(size=11),
        type='category'
    )
    return barchart


def local_peaks_bar(dataframe):
    df = dataframe
    dfs = [
        df.groupby('year').agg({'bear_peak_count':'sum'}).reset_index(),
        df.groupby('year').agg({'sanitas_count':'sum'}).reset_index(),
        df.groupby('year').agg({'second_flatiron_count':'sum'}).reset_index()
    ]
    df_merged = reduce(lambda  left,right: pd.merge(left,right, on=['year'], how='left'), dfs)
    barchart = px.bar(
        data_frame = df_merged.loc[df_merged.year != 2015],
        x = 'year',
        y = ['bear_peak_count','sanitas_count','second_flatiron_count'],
        color_discrete_map=dict(bear_peak_count='#FD5602', sanitas_count='#FF8303', second_flatiron_count='#FFAF42'),
        orientation = "v",
        barmode = 'group',
        title='Most Common Routes by Year'
    )
    barchart.update_layout(
        margin=dict(l=15, r=10, t=35, b=2),
        plot_bgcolor=BAR_PROPS['bg_color'],
        font_family=BAR_PROPS['font'],
        title_font_family=TITLE_FONT,
        xaxis_title='',
        yaxis_title='',
        legend_title='',
        height=BAR_PROPS['height'],
        legend=dict(
            #orientation='h',
            yanchor='top',
            y=0.93,
            xanchor='right',
            x=0.93,
            itemwidth=50,
            grouptitlefont=dict(
                family='Open Sans, Light 300',
                size=11,
                color='black'
            ),
            bgcolor=BAR_PROPS['bg_color'],
            bordercolor=BAR_PROPS['bg_color']
        )  
    )
    barchart.update_yaxes(
        ticksuffix=' ',
        tickfont=dict(size=11, family='Open Sans, Light 300')
    )
    return barchart


def scatter_max(dataframe):
    df = dataframe
    scatter = px.scatter(df.loc[~df['type'].isin(NON_AEROBIC)].sort_values(by=['day_of_month', 'month', 'elevation'], ascending=False).drop_duplicates(subset=['day_of_month', 'month'])[['month', 'day_of_month', 'year', 'name', 'type', 'hours', 'elevation']], 
                 x='month', 
                 y='day_of_month', 
                 color='elevation', 
                 size='hours',
                 title='Longest Activities by Day',
                 custom_data=['year', 'name', 'elevation', 'type', 'hours'],
                 color_continuous_scale=[[0, '#FFAF42'], [0.3, '#FF8303'], [0.5, '#FE6E00'], [0.7, '#FD5602'], [1, '#DF2400']],
                 category_orders={"month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
                 )
    scatter.update_traces(
        hovertemplate="<br>".join([
            "Name: %{customdata[1]}",
            "Type: %{customdata[3]}",
            "Date: %{x} %{y}, %{customdata[0]}",
            "Hours: %{customdata[4]}",
            "Elevation: %{customdata[2]}"
        ])
    )
    scatter.update_layout(
        margin=dict(l=15, r=10, t=35, b=2),
        plot_bgcolor=BAR_PROPS['bg_color'],
        height=430,
        xaxis_title='',
        yaxis_title='Day of Month',
    )
    scatter.update_yaxes(
        ticksuffix=' ',
        tickfont=dict(size=11, family='Open Sans, Light 300'),
        title_font=dict(size=11, family='Open Sans, Light 300')
    )
    
    return scatter