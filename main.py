import re
import os
import json
import utils.auto as Auto
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect


timeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logName = f"Log_Auto_{timeStamp}.txt"
LOG_AUTO_PATH = os.path.join(r".\output_logs", logName)
with open(LOG_AUTO_PATH, "w", encoding="utf-8") as file:
    file.write(f"### ******************* Auto.py Log - {timeStamp} ******************* ###\n\n")


with open(r".\config.json", "r") as configFile: 
    config = json.load(configFile)

USERNAME = config["username"]
PASSWORD = config["password"]
DIR = config["dir"]
PAY1 = config["pay1"]
PAY2 = config["pay2"]
PAY3 = config["pay3"]
PAY4 = config["pay4"]
PAY5 = config["pay5"]



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width":1280, "height":1440},
        #viewport={"width":960, "height":1080},
        # record_video_dir="videos",
        # record_video_size={"width":960, "height":1080}
    )
    page = context.new_page()
    page.goto("https://services.dir.ca.gov/gsp")

    Auto.Login(page, USERNAME, PASSWORD, LOG_AUTO_PATH)
    Auto.DismissAnnoucement(page, LOG_AUTO_PATH)
    Auto.ProjectSearchDirToView(page, DIR, LOG_AUTO_PATH)

    Auto.PayrollIndexIdToOpen(page, PAY3, LOG_AUTO_PATH)

  

    page.wait_for_timeout(10000)

    # ---------------------
    context.close()
    browser.close()



with sync_playwright() as playwright:
    run(playwright)

