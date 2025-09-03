import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure Edge options
options = EdgeOptions()
options.add_argument("--inprivate")

# Set up Edge through Flatpak
try:
    print("Launching Edge via Flatpak...")
    edge_process = subprocess.Popen(
        ["flatpak", "run", "com.microsoft.Edge"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Use WebDriver normally (requires msedgedriver in PATH)
    print("Initializing WebDriver...")
    browser = webdriver.Edge(options=options)
    
    # Your scraping code
    print("Loading GitHub page...")
    browser.get("https://github.com/collections/machine-learning")
    
    projects = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//h1[@class='h3 lh-condensed']"))
    )
    
    projects_list = {
        proj.text: proj.find_element(By.XPATH, ".//a").get_attribute('href') 
        for proj in projects
    }
    
    pd.DataFrame.from_dict(projects_list, orient='index', columns=['url'])\
               .rename_axis('project').reset_index()\
               .to_csv('projects.csv', index=False)
    
    print("Data saved successfully!")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'browser' in locals():
        browser.quit()
    if 'edge_process' in locals():
        edge_process.terminate()
    print("Cleanup complete")