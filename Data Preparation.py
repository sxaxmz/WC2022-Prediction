import pandas as pd

"""
Date Range

Matches in 2018 after WC until match before WC  2022.
"""
df_goalscorers = pd.read_csv('goalscorers.csv')
df_results = pd.read_csv('results.csv')
df_shootouts = pd.read_csv('shootouts.csv')
df_fifa_ranking = pd.read_csv('fifa_ranking-2022-10-06.csv')

df_results["date"] = pd.to_datetime(df_results["date"])
df_results = df_results[(df_results["date"] >= "2018-8-1")].reset_index(drop=True)
print(' Results Dataset: \n', df_results.sort_values("date").tail())

df_fifa_ranking["rank_date"] = pd.to_datetime(df_fifa_ranking["rank_date"])
df_fifa_ranking = df_fifa_ranking[(df_fifa_ranking["rank_date"] >= "2018-8-1")].reset_index(drop=True)
print('Fifa Ranking Dataset: \n', df_fifa_ranking.sort_values("rank_date").tail())

"""## Missing"""

print('Missing Count: \n',df_results.isna().sum(),'\n')
df_results.dropna(inplace=True)
print('Data Type: \n', df_results.dtypes, '\n')
print('Home Team: \n', df_results['home_team'].value_counts())

print('Missing Count: \n',df_shootouts.isna().sum(), '\n')
df_shootouts.dropna(inplace=True)
print('Data Type: \n', df_shootouts.dtypes, '\n')
print('Home Team: \n', df_shootouts['home_team'].value_counts(), '\n')

print('Missing Count: \n',df_goalscorers.isna().sum(), '\n')
df_goalscorers.dropna(inplace=True)
print('Data Type: \n', df_goalscorers.dtypes, '\n')
print('Home Team: \n', df_goalscorers['home_team'].value_counts(), '\n')

print('Missing Count: \n',df_fifa_ranking.isna().sum(), '\n')
df_fifa_ranking.dropna(inplace=True)
print('Data Type: \n', df_fifa_ranking.dtypes, '\n')
print('Country Name: \n', df_fifa_ranking['country_full'].value_counts(), '\n')

"""
Unify Names

As some teams have different names in ranking and results datasets 
"""

df_fifa_ranking["country_full"] = df_fifa_ranking["country_full"].str.replace("IR Iran", "Iran").str.replace("Korea Republic", "South Korea").str.replace("USA", "United States")
df_fifa_ranking = df_fifa_ranking.set_index(['rank_date']).groupby(['country_full'], group_keys=False).resample('D').first().fillna(method='ffill').reset_index()

"""
Merge Datasets

Fifa ranking & Results
"""

df_wc_ranked = df_results.merge(df_fifa_ranking[["country_full", "total_points", "previous_points", "rank", "rank_change", "rank_date"]], left_on=["date", "home_team"], right_on=["rank_date", "country_full"]).drop(["rank_date", "country_full"], axis=1)

df_wc_ranked = df_wc_ranked.merge(df_fifa_ranking[["country_full", "total_points", "previous_points", "rank", "rank_change", "rank_date"]], left_on=["date", "away_team"], right_on=["rank_date", "country_full"], suffixes=("_home", "_away")).drop(["rank_date", "country_full"], axis=1)

"""Sample Output"""

df_wc_ranked[(df_wc_ranked.home_team == "Qatar") | (df_wc_ranked.away_team == "Qatar")].tail(10)

"""Export Merged Dataset"""

df_wc_ranked.to_excel('WC_Ranked_Results_Fifa_Merged.xlsx')