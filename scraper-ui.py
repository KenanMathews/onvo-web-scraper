import tkinter as tk
from tkinter import ttk, messagebox
from integkey import IntegrationKeyManager
import onvo 
import os
from os.path import abspath
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import scraper_csv
import threading
import webbrowser
from nba_api.stats.static import players
from nba_api.stats.static import teams
import nba_api_integ


class LinkLabel(ttk.Label):
    def __init__(self, master, text, url, *args, **kwargs):
        super().__init__(master, text=text, cursor="hand2", *args, **kwargs)
        self.url = url
        self.bind("<Button-1>", self.open_link)
        
    def open_link(self, event):
        webbrowser.open(self.url)

class LoaderDialog(tk.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.title("Loader")
        self.geometry("200x100")
        self.label = tk.Label(self, text=message)
        self.label.pack(pady=20)
        self.loader = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        self.loader.pack(pady=5)
        self.loader.start()

class ScraperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python UI with Tabs")
        self.root.geometry("800x600")  # Set the size of the main application window

        # Create a Tab Control
        self.tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.api_tab = ttk.Frame(self.tab_control)
        self.scraper_tab = ttk.Frame(self.tab_control)
        self.settings_tab = ttk.Frame(self.tab_control)
        self.dashboard_tab = ttk.Frame(self.tab_control)

        # Add tabs to the Tab Control
        self.tab_control.add(self.api_tab, text='NBA API Tool')
        self.tab_control.add(self.scraper_tab, text='Scraper Tool')
        self.tab_control.add(self.settings_tab, text='Settings')
        self.tab_control.add(self.dashboard_tab, text='Dashboard')

        # Set up the layout for the Scraper Tool tab
        self.setup_api_tab()

        # Set up the layout for the Scraper Tool tab
        self.setup_scraper_tab()

        # Set up the layout for the Settings tab
        self.setup_settings_tab()

        # Set up the layout for the Dashboard tab
        self.setup_dashboard_tab()

        # Pack Tab Control to make it visible
        self.tab_control.pack(expand=1, fill="both")

        self.check_dashboard_condition()

        self.create_directory_if_not_exists(self.get_export_dir())

    def setup_api_tab(self):
        self.api_frame = ttk.Frame(self.api_tab)
        self.api_frame.pack(pady=10)

        self.season_end_year_label = tk.Label(self.api_frame, text="Player List")
        self.season_end_year_label.pack(pady=5)
        
        self.playerinfo = players.get_players()

        options = nba_api_integ.player_api_actions

        # Create the select box
        self.player_action_select_box = ttk.Combobox(self.api_frame, values=options)
        self.player_action_select_box.pack(pady=10)
         
        search_var_1 = tk.StringVar()
        self.search_entry = ttk.Entry(self.api_frame, textvariable=search_var_1)
        self.search_entry.pack()
        self.search_entry.bind('<KeyRelease>', lambda event: self.on_search(self.player_select_box,search_var_1.get().lower(),self.playerinfo,'full_name'))

        self.player_select_box = tk.Listbox(self.api_frame, height=5, selectmode=tk.MULTIPLE)
        self.player_select_box.pack()
        self.load_search_options(self.player_select_box,self.playerinfo,'full_name')
         
        self.generate_player_api_report = ttk.Button(self.api_frame, text="Generate Report", command=self.handle_player_report)
        self.generate_player_api_report.pack(pady=10)

        self.teaminfo = teams.get_teams()
         
         
        self.season_end_year_label = tk.Label(self.api_frame, text="Team List")
        self.season_end_year_label.pack(pady=5)

        options = nba_api_integ.team_api_actions
         # Create the select box
        self.team_action_select_box = ttk.Combobox(self.api_frame, values=options)
        self.team_action_select_box.pack(pady=10)

        search_var_2 = tk.StringVar()
        self.search_entry = ttk.Entry(self.api_frame, textvariable=search_var_2)
        self.search_entry.pack()
        self.search_entry.bind('<KeyRelease>', lambda event: self.on_search(self.team_select_box,search_var_2.get().lower(),self.teaminfo,'full_name'))

        self.team_select_box = tk.Listbox(self.api_frame, height=5)
        self.team_select_box.pack()
        self.load_search_options(self.team_select_box,self.teaminfo,'full_name')

        self.generate_team_api_report = ttk.Button(self.api_frame, text="Generate Report", command=self.handle_team_report)
        self.generate_team_api_report.pack(pady=10)
    
    def handle_player_report(self):
        player_ids = self.get_player_from_select_box()
        dashboardid = nba_api_integ.get_all_player_stats(player_ids,self.get_export_dir(),self.player_action_select_box.get())
        self.show_completion_popup(self.construct_onvo_url(dashboardid))
    
    def handle_team_report(self):
        team_ids = self.get_teams_from_select_box()
        dashboardid = nba_api_integ.get_all_team_stats(team_ids,self.get_export_dir(),self.team_action_select_box.get())
        self.show_completion_popup(self.construct_onvo_url(dashboardid))
    def load_search_options(self,box,items, key):
        for item in items:
            box.insert(tk.END, item[key])

    def on_search(self,box,search_query,items,key):
        box.delete(0, tk.END)  # Clear previous items

    # Filter items based on search query
        filtered_items = [item for item in items if any(search_query in str(val).lower() for val in item.values())]
        for item in filtered_items:
            box.insert(tk.END, item[key])

    def get_player_career_stats(self):
        player = self.get_player_from_select_box()
        if player is not None:
            nba_api_integ.get_player_career_stats(player['id'],self.get_export_dir())
    def get_player_fantasy_profile(self):
        player = self.get_player_from_select_box()
        if player is not None:
            nba_api_integ.get_player_fantasy_profile(player['id'],self.get_export_dir())
    def get_player_dashboard(self):
        player = self.get_player_from_select_box()
        if player is not None:
            nba_api_integ.get_player_dashboard(player['id'],self.get_export_dir())
    def get_player_from_select_box(self):
        player_ids = []
        selected_items = self.player_select_box.curselection()
        for idx in selected_items:
            player_name = self.player_select_box.get(idx)
            player_obj = self.get_player_obj_by_full_name(player_name)
            player_ids.append(player_obj['id'])
        return player_ids
    def get_player_obj_by_full_name(self,value):
        try:
            return players.find_players_by_full_name(value)[0]
        except:
            return None
    def get_teams_from_select_box(self):
        team_ids = []
        selected_items = self.team_select_box.curselection()
        for idx in selected_items:
            team_name = self.team_select_box.get(idx)
            team_obj = self.get_team_obj_by_full_name(team_name)
            team_ids.append(team_obj['id'])
        return team_ids
    def get_team_obj_by_full_name(self,value):
        try:
            return teams.find_teams_by_full_name(value)[0]
        except:
            return None
    def setup_scraper_tab(self):
        # Create frame for selection and labels in the Scraper Tool tab
        self.selection_frame = ttk.Frame(self.scraper_tab)
        self.selection_frame.pack(pady=10)

        # Selection and labels
        self.report_combobox = ttk.Combobox(self.selection_frame, values=["Players box scores by a date",
                                                                          "Players season statistics for a season",
                                                                          "Players advanced season statistics for a season",
                                                                          "All Team box scores by a date",
                                                                          "Schedule for a season"])
        self.report_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.report_combobox.config(width=30)

        # Date Entry
        self.date_label = tk.Label(self.scraper_tab, text="Enter Date (use this format 1-1-2018):")
        self.date_label.pack(pady=5)
        self.date_entry = tk.Entry(self.scraper_tab)
        self.date_entry.pack(pady=5)

        # Season End Year Entry
        self.season_end_year_label = tk.Label(self.scraper_tab, text="Enter Season End Year:")
        self.season_end_year_label.pack(pady=5)
        self.season_end_year_entry = tk.Entry(self.scraper_tab)
        self.season_end_year_entry.pack(pady=5)

        # Inputs and button
        self.generate_button = ttk.Button(self.scraper_tab, text="Generate Report", command=self.on_generate_report)
        self.generate_button.pack(pady=10)

        # Field 1 (Basketball Reference URL)
        tk.Label(self.scraper_tab, text="Basketball Reference URL:").pack(pady=5)
        self.url_entry = ttk.Entry(self.scraper_tab)
        self.url_entry.pack(pady=5)
        self.url_entry.config(width=30)

        # Field 2 (Dashboard Name)
        tk.Label(self.scraper_tab, text="Dashboard Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.scraper_tab)
        self.name_entry.pack(pady=5)
        self.name_entry.config(width=30)

        self.scrape_button = ttk.Button(self.scraper_tab, text="Scrape URL", command=self.on_scrape_report)
        self.scrape_button.pack(pady=10)
                
        self.progress_bar = ttk.Progressbar(self.scraper_tab, orient="horizontal", length=200, mode="indeterminate")

        # Bind combobox selection event to toggle fields
        #self.report_combobox.bind("<<ComboboxSelected>>", self.toggle_fields)

    def setup_settings_tab(self):
        # Create frame for settings in the Settings tab
        self.settings_frame = ttk.Frame(self.settings_tab)
        self.settings_frame.pack(pady=10)

        # Integration Key Label
        self.integration_key_label = ttk.Label(self.settings_frame, text="Integration Key:")
        self.integration_key_label.pack(pady=10)

        # Integration Key Entry
        self.integration_key_entry = ttk.Entry(self.settings_frame)
        self.integration_key_entry.pack(pady=5)

        # Save Integration Key Button
        self.save_integration_key_button = ttk.Button(self.settings_frame, text="Save Integration Key", command=self.save_integration_key)
        self.save_integration_key_button.pack(pady=5)

        self.integration_key_info = ttk.Label(self.settings_frame, text="Sign into onvo and use the below url to get key")
        self.integration_key_info.pack(pady=10)

        self.link_label = LinkLabel(self.settings_frame, text="Onvo", url="https://dashboard.onvo.ai/api-keys")
        self.link_label.pack(padx=10, pady=10)

    def setup_dashboard_tab(self):
        # Create frame for dashboard in the Dashboard tab
        self.dashboard_frame = ttk.Frame(self.dashboard_tab)
        self.dashboard_frame.pack(pady=10)

        # Extra Field Label
        self.extra_field_label = ttk.Label(self.dashboard_frame, text="Select an option:")
        self.extra_field_label.pack(pady=10)

        # Extra Field Combobox
        self.dashboard_combobox = ttk.Combobox(self.dashboard_frame, state="readonly")
        self.dashboard_combobox.pack(pady=5)
        self.show_dropdown()

        # Ask Input Field
        self.load_button = ttk.Button(self.dashboard_frame, text="Load", command=self.load_option)
        self.load_button.pack()

        self.ask_input_label = ttk.Label(self.dashboard_frame, text="Ask Input:")
        self.ask_input = tk.Text(self.dashboard_frame, height=4, width=50)
        self.ask_button = ttk.Button(self.dashboard_frame, text="Ask", command=self.ask_option)
        

    def toggle_fields(self, event):
        selected_report = self.report_combobox.get()
        if selected_report in ["Players box scores by a date", "All Team box scores by a date"]:
            self.date_label.pack()
            self.date_entry.pack()
            self.season_end_year_label.pack()
            self.season_end_year_entry.pack()
        elif selected_report in ["Players season statistics for a season", "Players advanced season statistics for a season", "Schedule for a season"]:
            self.date_label.pack_forget()
            self.date_entry.pack_forget()
            self.season_end_year_label.pack()
            self.season_end_year_entry.pack()
        else:
            # Hide both date and season end year fields if the selected report is not recognized
            self.date_label.pack_forget()
            self.date_entry.pack_forget()
            self.season_end_year_label.pack_forget()
            self.season_end_year_entry.pack_forget()


    def save_integration_key(self):
        # Get integration key from entry field
        integration_key = self.integration_key_entry.get()
        if onvo.load_dashboards(integration_key) is not None:
        # Save integration key from entry field to file
            manager = IntegrationKeyManager("integration_key.pkl")
            manager.integration_key = integration_key
            manager._save_integration_key()
            self.check_dashboard_condition()
            self.show_dropdown()
        else:
            messagebox.showinfo("Invalid key", "The key you have entered might be incorrect. Check and try again.")

    def show_dropdown(self):
        # Clear previous options
        self.dashboard_combobox['values'] = ()
        manager = IntegrationKeyManager("integration_key.pkl")
        manager.load_integration_key()
        if manager.integration_key is not None:
            self.json_data = onvo.load_dashboards(manager.integration_key)
            if self.json_data is not None:
                options = [item["title"] for item in self.json_data]
                self.dashboard_combobox['values'] = options
    def load_option(self):
        # Get selected option from dropdown
        selected_title = self.dashboard_combobox.get()
        print(selected_title)
        for item in self.json_data:
            if item["title"] == selected_title:
                selected_id = item["id"]
                print("Loaded option:", selected_title)
                print("ID:", selected_id)
                break
        # Show ask input field and button
        self.ask_input_label.pack()
        self.ask_input.pack()
        self.ask_button.pack()
    def ask_option(self):
        selected_title = self.dashboard_combobox.get()
        for item in self.json_data:
            if item["title"] == selected_title:
                selected_id = item["id"]
                print("Loaded option:", selected_title)
                print("ID:", selected_id)
                break
        question = self.ask_input.get("1.0", tk.END)
        if len(selected_id)>0:
            # Show loader dialog
            manager = IntegrationKeyManager("integration_key.pkl")
            manager.load_integration_key()            
            loader_dialog = LoaderDialog(self.dashboard_frame, "Loading...")
            data = onvo.ask_question(manager.integration_key,selected_id,question)
            loader_dialog.destroy()
            # Show message box with question
            messagebox.showinfo("Question", data)
    def check_dashboard_condition(self):
    # Check condition to show/hide dashboard tab
        integration_key_manager = IntegrationKeyManager("integration_key.pkl")
        integration_key_manager.load_integration_key()
        integration_key = integration_key_manager.integration_key
        try:
            if integration_key is not None and onvo.load_dashboards(integration_key) is not None:
                self.tab_control.add(self.dashboard_tab, text='Dashboard')
            else:
                self.tab_control.hide(self.dashboard_tab)
        except Exception as e:
            print("Error loading dashboards:", e)
    def on_generate_report(self):
        dashboardid = None
        selected_value = self.report_combobox.get()
        index = self.report_combobox["values"].index(selected_value)
        reportObject = str(index+1)
        inputDate = self.date_entry.get()
        endYear = self.season_end_year_entry.get()
        file = None
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        self.generate_button.config(state="disabled")
        parent_directory = os.path.dirname(os.getcwd())
        if reportObject == "1":
            # Generate report for players box scores by a date
            inputDate = self.date_entry.get()
            fileName = f"all-player-box-report-{inputDate}.csv"
            dateList = inputDate.split("-")
            output_file_path = f"{self.get_export_dir()}/{fileName}"
            file = open(output_file_path, 'w')
            client.player_box_scores(
                day=dateList[0],
                month=dateList[1],
                year=dateList[2],
                output_type=OutputType.CSV,
                output_file_path=output_file_path
            )
            file.close()
            print(f"Report exported at: {abspath(output_file_path)}!!\n\n")
            
        elif reportObject == "2":
            # Generate report for players season statistics for a season
            endYear = self.season_end_year_entry.get()
            fileName = f"all-player-season-report-{endYear}.csv"
            output_file_path = f"{self.get_export_dir()}/{fileName}"
            file = open(output_file_path, 'w')
            client.players_season_totals(
                season_end_year=endYear,
                output_type=OutputType.CSV,
                output_file_path=output_file_path
            )
            file.close()
            print(f"Report exported at: {abspath(output_file_path)}!!\n\n")
            
        elif reportObject == "3":
            # Generate report for players advanced season statistics for a season
            endYear = self.season_end_year_entry.get()
            fileName = f"all-player-advanced-season-report-{endYear}.csv"
            output_file_path = f"{self.get_export_dir()}/{fileName}"
            file = open(output_file_path, 'w')
            client.players_advanced_season_totals(
                season_end_year=endYear,
                output_type=OutputType.CSV,
                output_file_path=output_file_path
            )
            file.close()
            print(f"Report exported at: {abspath(output_file_path)}!!\n\n")
            
        elif reportObject == "4":
            # Generate report for all team box scores by a date
            inputDate = self.date_entry.get()
            fileName = f"all-team-report-{inputDate}.csv"
            dateList = inputDate.split("-")
            output_file_path = f"{self.get_export_dir()}/{fileName}"
            file = open(output_file_path, 'w')
            client.team_box_scores(
                day=dateList[0],
                month=dateList[1],
                year=dateList[2],
                output_type=OutputType.CSV,
                output_file_path=output_file_path
            )
            file.close()
            print(f"Report exported at: {abspath(output_file_path)}!!\n\n")
            
        elif reportObject == "5":
            # Generate report for season schedule for a season
            endYear = self.season_end_year_entry.get()
            fileName = f"season-schedule-{endYear}.csv"
            output_file_path = f"{self.get_export_dir()}/{fileName}"
            file = open(output_file_path, 'w')
            client.season_schedule(
                season_end_year=endYear,
                output_type=OutputType.CSV,
                output_file_path=output_file_path
            )
            file.close()
            print(f"Report exported at: {abspath(output_file_path)}!!\n\n")
        if file is not None:
            manager = IntegrationKeyManager("integration_key.pkl")
            manager.load_integration_key()       
            api_key = manager.integration_key
            datasourceid = onvo.create_datasource(api_key,selected_value)
            with open(output_file_path, 'r') as file:
                        file_contents = file.read()
            if onvo.upload_file_to_datasource(api_key,datasourceid,file_contents):
                dashboardid = onvo.create_dashboard(api_key,selected_value)
                onvo.add_datasouce_to_dashboard(api_key,dashboardid,datasourceid)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.generate_button.config(state="normal")
        self.show_completion_popup(self.construct_onvo_url(dashboardid))
    def on_scrape_report(self):
        manager = IntegrationKeyManager("integration_key.pkl")
        manager.load_integration_key()       
        api_key = manager.integration_key
        url = self.url_entry.get()
        dashboard_name = self.name_entry.get()
        if url:
            self.scrape_button.config(state="disabled")
            self.progress_bar.pack(pady=5)
            self.progress_bar.start()
            threading.Thread(target=self.run_scrape_and_save, args=(url, f"{self.get_export_dir()}", dashboard_name, api_key)).start()
    def run_scrape_and_save(self, url, file_path, dashboard_name, api_key):
        dashboardid = scraper_csv.scrape_and_save(url, file_path, dashboard_name, api_key)
        
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.scrape_button.config(state="normal")
        self.show_completion_popup(self.construct_onvo_url(dashboardid))
    def show_completion_popup(self,url):
        message = "CSV file has been saved successfully!"
        popup_window = tk.Toplevel(root)
        popup_window.title("Report generation completed")
        # Create a label with the GitHub link
        label = ttk.Label(popup_window, text=message)
        label.pack(padx=10, pady=10)
        label = ttk.Label(popup_window, text="View Dashboard: ")
        label.pack(padx=10, pady=10)

        # Create a button to open the GitHub link
        button = ttk.Button(popup_window, text="Open Dashboard", command=lambda: webbrowser.open(url))
        button.pack(padx=10, pady=10)
    def construct_onvo_url(self,dashboardid):
        if dashboardid is not None:
            return f"https://dashboard.onvo.ai/dashboards/{dashboardid}"
    def create_directory_if_not_exists(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Directory '{directory}' created.")
    def get_export_dir(self):
        return f"{os.path.dirname(os.getcwd())}/exported_files"
if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperUI(root)
    root.mainloop()
