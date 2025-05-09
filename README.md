# Selenium Gclick Project

This project is designed to scrape the Gclick website to capture the names of responsible individuals for each task using Selenium.

## Project Structure

```
selenium-gclick-project
├── src
│   ├── main.py          # Entry point of the application
│   ├── gclick_scraper.py # Contains the main scraping logic
│   └── utils
│       └── helpers.py   # Utility functions for the project
├── requirements.txt      # Lists project dependencies
└── README.md             # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd selenium-gclick-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have the appropriate WebDriver installed for your browser (e.g., ChromeDriver for Google Chrome).

## Usage

To run the scraper, execute the following command:
```
python src/main.py
```

## Overview

This project utilizes Selenium to automate the process of accessing the Gclick website and extracting relevant data. The main functionality is encapsulated in the `gclick_scraper.py` file, while utility functions are provided in the `helpers.py` file to streamline the scraping process.