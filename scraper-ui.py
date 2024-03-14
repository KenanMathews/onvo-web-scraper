import tkinter as tk
from tkinter import filedialog, IntVar, messagebox, scrolledtext
import scraper_csv
from tkinter import ttk
import json
import threading
import time
import onvo

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

class ScraperUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Basketball Reference Scraper")
        self.geometry("500x500")  # Wider and taller window

        # Change to themed style
        style = ttk.Style()
        style.theme_use("clam")  # Change to your desired theme

        self.url_label = tk.Label(self, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self, width=50)  # Wider entry
        self.url_entry.pack()

        self.dashboard_name_label = tk.Label(self, text="Dashboard Name:")
        self.dashboard_name_label.pack()

        self.dashboard_name_entry = tk.Entry(self, width=50)  # Wider entry
        self.dashboard_name_entry.pack()

        self.extra_field_label = tk.Label(self, text="Enter Onvo integration key:")
        self.extra_field_label.pack()

        self.extra_field_entry = tk.Entry(self, width=50)  # Wider entry
        self.extra_field_entry.pack()

        self.connect_button = tk.Button(self, text="Connect", command=self.show_dropdown)
        self.connect_button.pack()

        self.dropdown_label = tk.Label(self, text="Select an option:")
        self.dropdown_label.pack_forget()
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self, textvariable=self.dropdown_var)
        self.dropdown.pack_forget()

        self.load_button = tk.Button(self, text="Load", command=self.load_option)
        self.load_button.pack_forget()

        self.ask_input_label = tk.Label(self, text="Enter your question:")
        self.ask_input_label.pack_forget()
        self.ask_input = scrolledtext.ScrolledText(self, width=40, height=5)
        self.ask_input.pack_forget()

        self.ask_button = tk.Button(self, text="Ask", command=self.ask_question)
        self.ask_button.pack_forget()

        self.save_button = tk.Button(self, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="indeterminate")

        self.json_data = []

    def show_dropdown(self):
        # Clear previous options
        self.dropdown['values'] = ()
        api_key = self.extra_field_entry.get()
        self.json_data = onvo.load_dashboards(api_key)
        options = [item["title"] for item in self.json_data]
        self.dropdown['values'] = options
        # Show dropdown and load button
        self.dropdown_label.pack()
        self.dropdown.pack()
        self.load_button.pack()

    def load_option(self):
        selected_title = self.dropdown_var.get()
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

    def ask_question(self):
        question = self.ask_input.get("1.0", tk.END)
        api_key = self.extra_field_entry.get()
        selected_title = self.dropdown_var.get()
        selected_id = ""
        for item in self.json_data:
            if item["title"] == selected_title:
                selected_id = item["id"]
        if len(selected_id)>0:
            # Show loader dialog
            loader_dialog = LoaderDialog(self, "Loading...")
            data = onvo.ask_question(api_key,selected_id,question)
            loader_dialog.destroy()
            # Show message box with question
            messagebox.showinfo("Question", data)

    def save_to_csv(self):
        url = self.url_entry.get()
        dashboard_name = self.dashboard_name_entry.get()
        extra_value = self.extra_field_entry.get()
        selected_option = self.dropdown_var.get()
        print("Selected option:", selected_option)
        if url:
            file_path = filedialog.askdirectory()
            if file_path:
                self.save_button.config(state="disabled")
                self.progress_bar.pack(pady=5)
                self.progress_bar.start()
                threading.Thread(target=self.run_scrape_and_save, args=(url, file_path, dashboard_name, extra_value)).start()

    def run_scrape_and_save(self, url, file_path, dashboard_name, extra_value):
        scraper_csv.scrape_and_save(url, file_path, dashboard_name, extra_value)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.save_button.config(state="normal")
        self.show_completion_popup()

    def show_completion_popup(self):
        messagebox.showinfo("Success", "CSV file has been saved successfully!")

if __name__ == "__main__":
    app = ScraperUI()
    app.mainloop()
