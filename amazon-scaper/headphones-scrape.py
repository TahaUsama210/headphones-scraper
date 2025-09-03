import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Edge options
options = EdgeOptions()
options.add_argument("--inprivate")

# Use Selenium Manager to automatically fetch the right driver
service = Service()
browser = webdriver.Edge(service=service, options=options)

try:
    print("Loading Amazon headphones deals...")
    browser.get("https://www.amazon.ca/s?k=headphones&rh=p_n_deal_type%3A6479691011")

    # Wait for search results to load
    headphones = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
    )

    data = []

    for headphone in headphones:
        try:
            title = headphone.find_element(By.XPATH, ".//span[@class='a-size-medium']").text
            link = headphone.find_element(By.XPATH, ".//a[@class='a-link-normal s-no-outline']").get_attribute("href")
            sale_price = headphone.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            original_price = headphone.find_element(
                By.XPATH, ".//span[@class='a-price a-text-price']//span[@class='a-offscreen']"
            ).text

            data.append({
                "title": title,
                "sale_price": sale_price,
                "original_price": original_price,
                "url": link
            })

            # Small random delay to look less like a bot
            time.sleep(random.uniform(1, 3))

        except Exception:
            continue

    # Save results to CSV
    pd.DataFrame(data).to_csv("amazon_headphones_on_sale.csv", index=False)
    print("Data saved successfully!")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'browser' in locals():
        browser.quit()
    print("Cleanup complete")
