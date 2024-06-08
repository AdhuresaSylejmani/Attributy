import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from typing import List


class DataProcessor:


    def __init__(self, data: pd.DataFrame) -> None:
   
        self.data = data

    def statistical_summary(self) -> pd.DataFrame:

        return self.data.describe()

    def store_plot(self, plot, path: str) -> None:
 
        plot.figure.savefig(path)

    def get_boxplot(self, column: str):

        return self.data.boxplot(column)

    def plot_and_save_histograms(self, columns: List[str]) -> Figure:

        fig = plt.figure(figsize=(15, 13))
        selected_data = self.data[columns]

        for i in range(1, selected_data.shape[1]+1):
            plt.subplot(2, 2, i)
            figure = plt.gca()
            figure.set_title(selected_data.columns[i-1])

            data_to_plot = selected_data.iloc[:, i-1].dropna()

            plt.hist(data_to_plot)
            plt.xlabel('Measure')
            plt.ylabel('Count')

        plt.tight_layout(pad=2)
        return fig


    def add_converted_column(self) -> None:

        self.data['converted'] = self.data['purchase'].apply(lambda x: 1 if pd.notna(x) else 0)

    def add_state_abbreviation_column(self) -> None:

        state_abbreviations = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'American Samoa': 'AS', 'California': 'CA', 'Colorado': 'CO',
            'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI',
            'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
            'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
            'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
            'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
            'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
            'Trust Territories': 'TT', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Virgin Islands': 'VI', 'Washington': 'WA', 'West Virginia': 'WV',
            'Wisconsin': 'WI', 'Wyoming': 'WY'
        }
        self.data['state_abbreviation'] = self.data['state'].map(state_abbreviations)

    def add_normalized_column(self, column: str) -> None:

        self.data[column + '_normalized'] = (self.data[column] - self.data[column].mean()) / self.data[column].std()

    def add_85_percentile_state(self) -> None:

        percentile_85 = self.data.groupby('state')['purchase'].quantile(0.85)
        self.data['85th_percentile_state'] = self.data.apply(lambda row: 1 if pd.notna(row['purchase']) and row['purchase'] >= percentile_85[row['state']] else 0, axis=1)

    def add_85_percentile_nationality(self) -> None:

        percentile_85_national = self.data['purchase'].quantile(0.85)
        self.data['85th_percentile_national'] = self.data['purchase'].apply(lambda x: 1 if pd.notna(x) and x >= percentile_85_national else 0)

    def fill_in_missing_with_median(self, column: str) -> None:

        median = self.data[column].median()
        self.data[column].fillna(median, inplace=True)
