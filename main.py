import os
import json
import src.automate as Automate
import src.parser as Parser
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect

pathFolderInData = r".\data_input"
pathFolderOutData = r".\data_output"
pathFolderLogParser = r".\log_parser"
pathFolderLogAutomate = r".\log_automate"

os.makedirs(pathFolderLogParser, exist_ok=True)
os.makedirs(pathFolderLogAutomate, exist_ok=True)
os.makedirs(f"{pathFolderOutData}_frame", exist_ok=True)
os.makedirs(f"{pathFolderOutData}_parse", exist_ok=True)

timeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

PATH_LOG_PARSER = os.path.join(pathFolderLogParser, f"data_{timeStamp}.txt")
with open(PATH_LOG_PARSER, "w", encoding="utf-8") as parserLog:
    parserLog.write(f"### ******************* Parser.py Log - {timeStamp} ******************* ###\n\n")


PATH_LOG_AUTOMATE = os.path.join(pathFolderLogAutomate, f"automate_{timeStamp}.txt")
with open(PATH_LOG_AUTOMATE, "w", encoding="utf-8") as automateLog:
    automateLog.write(f"### ******************* Automate.py Log - {timeStamp} ******************* ###\n\n")


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


xlsxList = [file for file in os.listdir(pathFolderInData) if file.endswith(".xlsx")]

Parser.parse_cpr_xlsx_bulk(xlsxList, pathFolderInData, pathFolderOutData, PATH_LOG_PARSER)


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

    Automate.s0_log_in(page, USERNAME, PASSWORD, PATH_LOG_AUTOMATE)
    Automate.s1_dismiss_announcement(page, PATH_LOG_AUTOMATE)
    Automate.s1_project_search_dir_view(page, DIR, PATH_LOG_AUTOMATE)
    Automate.s2_payroll_index_id_open(page, PAY3, PATH_LOG_AUTOMATE)

    page.wait_for_timeout(10000)

    # ---------------------
    context.close()
    browser.close()



with sync_playwright() as playwright:
    run(playwright)
