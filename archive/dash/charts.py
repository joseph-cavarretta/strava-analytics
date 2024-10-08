from functools import reduce
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

 
# TABLE_HEADER_PROPS = {
#     'fill_color': '#FF8303',
#     'align': 'left',
#     'line_color': 'white',
#     'font': dict(color='white', size=13, family=TITLE_FONT)
# }
# TABLE_PROPS = {
#     'fill_color': '#FEDEBE',
#     'align': 'left',
#     'line_color': 'white',
#     'height': 30,
#     'font': dict(color='black', size=11, family=FONT)
# }
# BAR_PROPS = {
#     'bg_color': '#FEDEBE',
#     'bar_color': '#FF8303',
#     'font': FONT,
#     'height': 400
# }

"""
dbc.Card(
    dbc.CardBody([
        dcc.Graph(
            figure=px.bar(
                df, x="sepal_width", y="sepal_length", color="species"
            ).update_layout(
                template='plotly_dark',
                plot_bgcolor= 'rgba(0, 0, 0, 0)',
                paper_bgcolor= 'rgba(0, 0, 0, 0)',
            ),
            config={
                'displayModeBar': False
            }
)
"""

class ChartHandler:
    def __init__(self, data_path, non_aerobic_modes: list, strength_modes: list):
        self.data_path = data_path
        self.non_aerobic_modes = non_aerobic_modes
        self.strength_modes = strength_modes
        self.data = self.__get_dataframe()


    def __get_dataframe(self):
        return pd.read_csv(self.data_path)
    

    def bar_chart_by_week(self, x=None, y=None, title=None):
        barchart = px.bar(
            self.data, 
            x=x,
            y=y,
            title=title
            #color_discrete_sequence=[BAR_PROPS['bar_color']] * len(self.data)
        )
        barchart.update_layout(
            margin=dict(l=20, r=10, t=35, b=2),
            # plot_bgcolor=BAR_PROPS['bg_color'],
            # font_family=BAR_PROPS['font'],
            # title_font_family=TITLE_FONT,
            # xaxis_title='',
            # yaxis_title='',
            # height=BAR_PROPS['height'],
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


    def local_peaks_bar(self):
        df = ''
        dfs = [
            df.groupby('year').agg({'bear_peak_count':'sum'}).reset_index(),
            df.groupby('year').agg({'sanitas_count':'sum'}).reset_index(),
            df.groupby('year').agg({'second_flatiron_count':'sum'}).reset_index()
        ]
        df_merged = reduce(lambda left,right: pd.merge(left,right, on=['year'], how='left'), dfs)
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
            # plot_bgcolor=BAR_PROPS['bg_color'],
            # font_family=BAR_PROPS['font'],
            # title_font_family=TITLE_FONT,
            # xaxis_title='',
            # yaxis_title='',
            # legend_title='',
            # height=BAR_PROPS['height'],
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
                )
                # bgcolor=BAR_PROPS['bg_color'],
                # bordercolor=BAR_PROPS['bg_color']
            )  
        )
        barchart.update_yaxes(
            ticksuffix=' ',
            tickfont=dict(size=11, family='Open Sans, Light 300')
        )
        return barchart


    def table(self, cols=[], title=None):
        # table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        df = df.loc[:, cols]
        df.loc[df.name.str.len() > 38, 'name'] = df.loc[df.name.str.len() > 38, 'name'].str.slice(0,35) + '...'
        table = go.Figure(
            data=[
                go.Table(
                    columnwidth = [45, 10, 15, 20],
                    header=dict(
                        values=list(df.columns)
                        # fill_color=TABLE_HEADER_PROPS['fill_color'],
                        # align=TABLE_HEADER_PROPS['align'],
                        # line_color=TABLE_HEADER_PROPS['line_color'],
                        # font=TABLE_HEADER_PROPS['font']
                        
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns]
                        # fill_color=TABLE_PROPS['fill_color'],
                        # align=TABLE_PROPS['align'],
                        # line_color=TABLE_PROPS['line_color'],
                        # font=TABLE_PROPS['font'],
                        # height=TABLE_PROPS['height']
                    ))])
        table.update_layout(
            margin = dict(l=10, r=10, t=30, b=2),
            title = dict(text=title, y=0.99, x=0.025, font=dict(color='black')),
            #title_font_family=TITLE_FONT
        )
        return table


    #def scatter_max(self):
        # scatter = px.scatter(df.loc[~df['type'].isin(NON_AEROBIC)].sort_values(by=['day_of_month', 'month', 'elevation'], ascending=False).drop_duplicates(subset=['day_of_month', 'month'])[['month', 'day_of_month', 'year', 'name', 'type', 'hours', 'elevation']], 
        #             x='month', 
        #             y='day_of_month', 
        #             color='elevation', 
        #             size='hours',
        #             title='Longest Activities by Day',
        #             custom_data=['year', 'name', 'elevation', 'type', 'hours'],
        #             color_continuous_scale=[[0, '#FFAF42'], [0.3, '#FF8303'], [0.5, '#FE6E00'], [0.7, '#FD5602'], [1, '#DF2400']],
        #             category_orders={"month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
        #             )
        # scatter.update_traces(
        #     hovertemplate="<br>".join([
        #         "Name: %{customdata[1]}",
        #         "Type: %{customdata[3]}",
        #         "Date: %{x} %{y}, %{customdata[0]}",
        #         "Hours: %{customdata[4]}",
        #         "Elevation: %{customdata[2]}"
        #     ])
        # )
        # scatter.update_layout(
        #     margin=dict(l=15, r=10, t=35, b=2),
        #     plot_bgcolor=BAR_PROPS['bg_color'],
        #     height=430,
        #     xaxis_title='',
        #     yaxis_title='Day of Month',
        # )
        # scatter.update_yaxes(
        #     ticksuffix=' ',
        #     tickfont=dict(size=11, family='Open Sans, Light 300'),
        #     title_font=dict(size=11, family='Open Sans, Light 300')
        # )
        
        # return scatter