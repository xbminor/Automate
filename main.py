import re
import json
import utils.auto as Auto
from playwright.sync_api import Playwright, sync_playwright, expect


with open(r".\config.json", "r") as configFile: 
    config = json.load(configFile)

USERNAME = config["username"]
PASSWORD = config["password"]
DIR = config["dir"]
USER_FIRST_LAST = config["user_first_last"]



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

    Auto.Login(page, USERNAME, PASSWORD)
    Auto.DismissAnnoucement(page)

    Auto.SearchMyProjects(page, DIR, True)

    

  

    page.wait_for_timeout(10000)

    # ---------------------
    context.close()
    browser.close()



with sync_playwright() as playwright:
    run(playwright)

