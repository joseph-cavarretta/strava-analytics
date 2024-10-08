import plotly.express as px

MONTHS = {
        "month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
}

def stacked_bar_by_month(self, y=None, title=None, color=None):
        barchart = px.bar(
            self.data, 
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


def max_elevation_scatter_plot(self):
        plot_cols = ['month', 'day_of_month', 'year', 'name', 'type', 'hours', 'elevation']
        sort_cols = ['day_of_month', 'month', 'elevation']
        dups_cols = ['day_of_month', 'month']
        plot_data = self.data.loc[~self.data['type'].isin(NON_AEROBIC)]
    
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
    