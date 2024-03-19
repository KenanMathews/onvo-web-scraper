# Onvo Web Scraper
## Description
This is a Python application that scrapes tables from a URL and stores them in a CSV file, which can then be uploaded to Onvo for data analysis.

##Installation
To use this application, ensure that you have Python 3.x installed on your system. Then, follow these steps:

Clone this repository to your local machine.
Navigate to the project directory.
pip install -r requirements.txt

## Requirements
The application requires the following dependencies:

```
beautifulsoup4==4.12.2
lxml==5.1.0
nba_api==1.4.1
pandas==2.1.4
pytz==2023.3.post1
requests==2.31.0
requests-toolbelt==1.0.0
tkcalendar==1.6.1
```
The project also uses resources from 
- [Basketball Reference Web Scraper](https://github.com/jaebradley/basketball_reference_web_scraper) - A library for generating reports from basketball reference website


## Usage
Run the application with:
```
python3 scraper-ui.py
```

The scraped tables will be saved in a CSV file within the project directory.
Upload the CSV file to Onvo for data analysis.

## Build

You can build the executable using pyinstaller but running the build.sh file in the repository

## Contributing
If you want to contribute to this project, feel free to fork the repository and submit a pull request.

