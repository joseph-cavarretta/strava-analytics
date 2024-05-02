"""
Created on Fri Sept 2 18:02:33 2022
@author: joseph.cavarretta
"""
import pandas as pd
from reports import overallReport, yearlyReport, runReport, climbingReport, strengthReport

def main():
    df = load_data()
    reports = ['overall', 'yearly', 'run', 'climb', 'strength']
    print("\n"+ ("=" * 70))
    print("Which activity report would you like to generate?")
    print("=" * 70)
    print("Enter one of the following options:")
    print(reports)
    report_type = input(">> ")

    if not report_type.lower() in reports:
        raise SystemExit("Not a valid entry. Report cancelled.")

    print_report(report_type, df)


def load_data():
    path = 'data/processed_activities.csv'
    data = pd.read_csv(path)
    return data


def print_report(report_type, dataframe):
    if report_type.lower() == 'overall':
        rep = overallReport(dataframe)
        rep.print_report()

    if report_type.lower() == 'yearly':
        rep = yearlyReport(dataframe)
        rep.print_report()

    if report_type.lower() == 'run':
        rep = runReport(dataframe)
        rep.print()

    if report_type.lower() == 'climb':
        rep = climbingReport(dataframe)
        rep.print()

    if report_type.lower() == 'strength':
        rep = strengthReport(dataframe)
        rep.print()


if __name__ == '__main__':
    main()