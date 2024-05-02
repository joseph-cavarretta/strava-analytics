class overallReport:
    def __init__(self, dataframe):
        self.data = dataframe
        self.run_data = dataframe.loc[dataframe.type == 'Run']
        self.bike_data = dataframe.loc[dataframe.type == 'Ride']
        self.strength_data = dataframe.loc[dataframe.type == 'WeightTraining']
        self.climb_data = dataframe.loc[dataframe.type == 'RockClimbing']
        
    def print_report(self):
        self.print_summary_stats()

    def print_summary_stats(self):
        print("\n" + ("*"*27) + " SUMMARY STATS " + ("*"*27) + "\n")
        print(f"Total Activities: {len(self.data):,}")
        print(f"Total Activity Duration: {round(sum(self.data.elapsed_time)/60/60):,} hours")
        print(f"Total Activity Distance: {round(sum(self.data.miles)):,} miles")
        print(f"Total Elevation Gain: {round(sum(self.data.elevation)):,} feet")
        
        print ("\n" + ("*"*27) + " Boulder Stats " + ("*"*27) + "\n")
        
        print(f"Total Bear Peak Summits: {sum(self.data.bear_peak_count):,}")
        print(f"Total Sanitas Summits: {sum(self.data.sanitas_count):,}")
        print(f"Total 2nd Flatiron Climbs: {sum(self.data.second_flatiron_count):,}")

        print ("\n" + ("*"*29) + " Run Stats " + ("*"*29) + "\n")

        print(f"Total Run Activities: {len(self.run_data):,}")
        print(f"Total Run Duration: {round(sum(self.run_data.elapsed_time)/60/60):,} hours")
        print(f"Total Run Distance: {round(sum(self.run_data.miles)):,} miles")
        print(f"Total Run Elevation Gain: {round(sum(self.run_data.elevation)):,} feet")

        print ("\n" + ("*"*29) + " Bike Stats " + ("*"*29) + "\n")

        print(f"Total Bike Activities: {len(self.bike_data):,}")
        print(f"Total Bike Duration: {round(sum(self.bike_data.elapsed_time)/60/60):,} hours")
        print(f"Total Bike Distance: {round(sum(self.bike_data.miles)):,} miles")
        print(f"Total Bike Elevation Gain: {round(sum(self.bike_data.elevation)):,} feet")

        print ("\n" + ("*"*28) + " Strength Stats " + ("*"*29) + "\n")

        print(f"Total Strength Workouts: {len(self.strength_data):,}")
        print(f"Total Strength Duration: {round(sum(self.strength_data.elapsed_time)/60/60):,} hours")
        print(f"Total Plyo Workouts: {sum(self.strength_data.plyo_count):,}")

        print ("\n" + ("*"*28) + " Climbing Stats " + ("*"*29) + "\n")

        print(f"Total Indoor Climbs: {sum(self.strength_data.indoor_climb_count):,}")
        print(f"Total Outdoor Climbs: {sum(self.climb_data.outdoor_climb_count):,}")
        print(f"Total Indoor Boulders: {sum(self.strength_data.indoor_boulder_count):,}")
        print(f"Total Outdoor Boulders: {sum(self.climb_data.outdoor_boulder_count):,}")
        

class yearlyReport:
    def __init__(self, dataframe):
        self.data = dataframe
        self.run_data = dataframe.loc[dataframe.type == 'Run']
        self.bike_data = dataframe.loc[dataframe.type == 'Ride']
        self.strength_data = dataframe.loc[dataframe.type == 'WeightTraining']
        self.climb_data = dataframe.loc[dataframe.type == 'RockClimbing']
        
    def print_report(self):
        self.print_summary_stats()
    
    def print_summary_stats(self):
        print("\n" + ("*"*27) + " YEARLY STATS " + ("*"*27) + "\n")
        print(f"Total Activities:\n")
        for year in self.data.year.unique():
            print(f"{year}: {len(self.data.loc[self.data.year == year]):,}")

        print(f"\nTotal Activity Duration:\n")
        for year in self.data.year.unique():
            print(f"{year}: {round((self.data.loc[self.data.year == year]['elapsed_time'].sum())/60/60):,} hours")
        
        print(f"\nTotal Activity Distance:\n")
        for year in self.data.year.unique():
            print(f"{year}: {round(self.data.loc[self.data.year == year]['miles'].sum()):,} miles")

        print(f"\nTotal Elevation Gain:\n")
        for year in self.data.year.unique():
            print(f"{year}: {round(self.data.loc[self.data.year == year]['elevation'].sum()):,} feet")
        
        print ("\n" + ("*"*27) + " Boulder Stats " + ("*"*27) + "\n")
        
        print(f"Total Bear Peak Summits:\n")
        for year in self.data.year.unique():
            print(f"{year}: {round(self.data.loc[self.data.year == year]['bear_peak_count'].sum()):,} summits")
        
        print(f"\nTotal Sanitas Summits:\n")
        for year in self.data.year.unique():
            print(f"{year}: {round(self.data.loc[self.data.year == year]['sanitas_count'].sum()):,} summits")

        print(f"\nTotal 2nd Flatiron Climbs:\n")
        for year in self.data.year.unique():
            print(f"{year}: {round(self.data.loc[self.data.year == year]['second_flatiron_count'].sum()):,} climbs")

        print ("\n" + ("*"*29) + " Run Stats " + ("*"*29) + "\n")

        print(f"Total Run Activities:\n")
        for year in self.run_data.year.unique():
            print(f"{year}: {round(len(self.run_data.loc[self.run_data.year == year])):,} runs")

        print(f"\nTotal Run Duration:\n")
        for year in self.run_data.year.unique():
            print(f"{year}: {round((self.run_data.loc[self.run_data.year == year]['elapsed_time'].sum())/60/60):,} hours")

        # print(f"Total Run Distance: {round(sum(self.run_data.miles)):,} miles")
        # print(f"Total Run Elevation Gain: {round(sum(self.run_data.elevation)):,} feet")

        # print ("\n" + ("*"*29) + " Bike Stats " + ("*"*29) + "\n")

        # print(f"Total Bike Activities: {len(self.bike_data):,}")
        # print(f"Total Bike Duration: {round(sum(self.bike_data.elapsed_time)/60/60):,} hours")
        # print(f"Total Bike Distance: {round(sum(self.bike_data.miles)):,} miles")
        # print(f"Total Bike Elevation Gain: {round(sum(self.bike_data.elevation)):,} feet")

        # print ("\n" + ("*"*28) + " Strength Stats " + ("*"*29) + "\n")

        # print(f"Total Strength Workouts: {len(self.strength_data):,}")
        # print(f"Total Strength Duration: {round(sum(self.strength_data.elapsed_time)/60/60):,} hours")
        # print(f"Total Plyo Workouts: {sum(self.strength_data.plyo_count):,}")

        # print ("\n" + ("*"*28) + " Climbing Stats " + ("*"*29) + "\n")

        # print(f"Total Indoor Climbs: {sum(self.strength_data.indoor_climb_count):,}")
        # print(f"Total Outdoor Climbs: {sum(self.climb_data.outdoor_climb_count):,}")
        # print(f"Total Indoor Boulders: {sum(self.strength_data.indoor_boulder_count):,}")
        # print(f"Total Outdoor Boulders: {sum(self.climb_data.outdoor_boulder_count):,}")


class runReport:
    def __init__(self, dataframe):
        self.data = dataframe
    # Run stats by year
    # Run stats by month
    # Run stats by week
    # Other specific metrics


class strengthReport:
    def __init__(self, dataframe):
        self.data = dataframe
    # strenth totals
    # plyo totals
    # indoor climb and boulder totals


class climbingReport:
    def __init__(self, dataframe):
        self.data = dataframe
    # grades climbed
    # total pitches
    # total sessions
    # indoor vs outdoor