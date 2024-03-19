from nba_api.stats import endpoints
from nba_api.stats.static import players, teams
from integkey import IntegrationKeyManager
import onvo
from pandas import DataFrame

manager = IntegrationKeyManager("integration_key.pkl")
manager.load_integration_key() 
api_key = manager.integration_key

player_api_actions =  ["Player Profile", "Player Career Stats", "Player Fantasy Profile", "Player Dashboard", "Player Awards"]

def save_df_to_csv(df,filepath):
    df.to_csv(filepath)
def save_push_to_onvo(obj,title,filepath,dashboardid):
    if obj is not None:
        index = 1
        for df in obj.get_data_frames():
            save_df_to_csv(df,f"{filepath}/{title} Table {index}.csv")
            if dashboardid is not None:
                datasourceid = onvo.create_datasource(api_key, title)
                if onvo.upload_file_to_datasource(api_key, datasourceid,df.to_csv(index=False)):
                    onvo.add_datasouce_to_dashboard(api_key, dashboardid, datasourceid)
                    index = index + 1 
def get_all_player_stats(player_ids,filepath, selected_option):
    if selected_option in player_api_actions:
        dashboardid = onvo.create_dashboard(api_key,selected_option)
        for player_id in player_ids:
            if selected_option == "Player Profile":
                get_player_profile(player_id,filepath,dashboardid)
            elif selected_option == "Player Career Stats":
                get_player_career_stats(player_id,filepath,dashboardid)
            elif selected_option == "Player Fantasy Profile":
                get_player_fantasy_profile(player_id,filepath,dashboardid)
            elif selected_option == "Player Dashboard":
                get_player_dashboard(player_id,filepath,dashboardid)
            elif selected_option == "Player Awards":
                get_player_awards(player_id,filepath,dashboardid)
    return dashboardid
def get_player_career_stats(player_id,filepath,dashboardid):
    career_stats = endpoints.PlayerCareerStats(player_id=player_id)
    title = f"{players.find_player_by_id(player_id)['full_name']} Career Stats"
    save_push_to_onvo(career_stats,title,filepath,dashboardid)
def get_player_fantasy_profile(player_id,filepath,dashboardid):
    pfp = endpoints.PlayerFantasyProfile(player_id=player_id)
    title = f"{players.find_player_by_id(player_id)['full_name']} Fantasy Profile"
    save_push_to_onvo(pfp,title,filepath,dashboardid)
def get_player_dashboard(player_id,filepath,dashboardid):
    pdp = endpoints.PlayerDashboardByYearOverYear(player_id=player_id)
    title = f"{players.find_player_by_id(player_id)['full_name']} YoY"
    save_push_to_onvo(pdp,title,filepath,dashboardid)
def get_player_profile(player_id,filepath,dashboardid):
    pp = endpoints.PlayerProfileV2(player_id=player_id)
    title = f"{players.find_player_by_id(player_id)['full_name']} Profile"
    save_push_to_onvo(pp,title,filepath,dashboardid)
def get_player_awards(player_id,filepath,dashboardid):
    pa = endpoints.PlayerAwards(player_id=player_id)
    title = f"{players.find_player_by_id(player_id)['full_name']} Awards"
    save_push_to_onvo(pa,title,filepath,dashboardid)

team_api_actions =  ["Team year by year stats", "Team Dashboard"]

def get_all_team_stats(team_ids,filepath, selected_option):
    if selected_option in team_api_actions:
        dashboardid = onvo.create_dashboard(api_key,selected_option)
        for team_id in team_ids:
            if selected_option == "Team year by year stats":
                get_team_yby_stats(team_id,filepath,dashboardid)
            elif selected_option == "Team Dashboard":
                get_team_dashboard(team_id,filepath,dashboardid)
    return dashboardid
def get_team_yby_stats(team_id,filepath,dashboardid):
    stats = endpoints.TeamYearByYearStats(team_id=team_id)
    title = f"{teams.find_team_name_by_id(team_id)['full_name']} YbY Stats"
    save_push_to_onvo(stats,title,filepath,dashboardid)
def get_team_dashboard(team_id,filepath,dashboardid):
    stats = endpoints.TeamPlayerDashboard(team_id=team_id)
    title = f"{teams.find_team_name_by_id(team_id)['full_name']} Dashboard"
    save_push_to_onvo(stats,title,filepath,dashboardid)


