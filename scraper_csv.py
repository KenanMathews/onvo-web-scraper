import requests
from bs4 import BeautifulSoup
import csv
import os
import io
import onvo

def scrape_and_save(url, file_path,title,api_key):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    tables = soup.find_all("table")
    title = title[:50]
    dashboardid = onvo.create_dashboard(api_key,title)
    for table in tables:
        table_id = table.get("id")

        # Get column headers
        headers = []
        header_row = table.find("thead")
        if header_row:
            header_cells = header_row.find_all("th")
            for header in header_cells:
                headers.append(header.text.strip())

        stats_rows = table.find_all("tr")
        table_data = []

        for row in stats_rows:
            row_data = []

            # Extract data from each cell in the row
            cells = row.find_all("td")
            for cell in cells:
                cell_text = cell.text.strip()
                row_data.append(cell_text)

            table_data.append(row_data)
        # Save data to CSV
        file_name = file_path+os.sep+table_id+"_stats.csv"
        if headers:  # Write header row only if not empty
            with open(f"{file_name}", "w", newline="") as csvfile:
                csv_content = '\n'.join([','.join(row) for row in [headers] + table_data])
                csv_file = io.BytesIO(csv_content.encode())
                writer = csv.writer(csvfile)
                writer.writerow(headers)  # Write column headers
                writer.writerows(table_data)
                datasourceid = onvo.create_datasource(api_key,table_id)
                if onvo.upload_file_to_datasource(api_key,datasourceid,csv_file):
                    onvo.add_datasouce_to_dashboard(api_key,dashboardid,datasourceid)
        else:
            print(f"Skipping table {table_id} due to missing headers.")