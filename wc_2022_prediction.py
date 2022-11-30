from collections.abc import Iterable
import pandas as pd

group_count, wc_teams_dict, matches, group, team, g, team1, team2 = 0, {}, [], [], [], [], [], []
matches_df, group_teams_df = pd.DataFrame(), pd.DataFrame()
groups = ["A", "B", "C", "D", "E", "F", "G", "H"]

dfs = pd.read_html('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup#Teams')

for i in range(len(dfs)):
    df = dfs[i]
    cols = list(df.columns.values)   
    if isinstance(cols[0], Iterable):
        if any("Tie-breaking criteria" in c for c in cols):
            s_pos = i+1

        if any("Match 46" in c for c in cols):
            e_pos = i+1
wc_teams_dict[groups[group_count]] = [[a.split(" ")[0], 0, []] for a in list(dfs[s_pos].iloc[:, 1].values)] #{(TEAM, POINTS, WIN PROBS)}

for i in range(s_pos+1, e_pos, 1):
    if len(dfs[i].columns) == 3:
        team_1 = dfs[i].columns.values[0]
        team_2 = dfs[i].columns.values[-1]
        matches.append((groups[group_count], team_1, team_2)) # (Group, Team1, Team2)
        g.append(groups[group_count])
        team1.append(team_1)
        team2.append(team_2)
    else:
        group_count+=1
        wc_teams_dict[groups[group_count]] = [[a, 0, []] for a in list(dfs[i].iloc[:, 1].values)]
        for a in list(dfs[i].iloc[:, 1].values):
            group.append(groups[group_count])
            team.append(a)

group_teams_df['Group'] = group
group_teams_df['Team'] = team

matches_df['Group'] = g
matches_df['Team 1'] = team1
matches_df['Team 2'] = team2

with pd.ExcelWriter('WC Teams and Matches.xlsx') as writer:
  group_teams_df.to_excel(writer, sheet_name='Groups ({})'.format(len(groups)))
  matches_df.to_excel(writer, sheet_name='Matches ({})'.format(len(matches_df)))

for g in groups:
  print(g)
  for m in matches:
    if g in m[0]:
      print(m[1], 'vs', m[2])
