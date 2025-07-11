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
PROJECT_DIR = config["project_dir"]
CPR_OPEN = config["cpr_open"]
CPR_ID = config["cpr_id"]
PRIME_ID = config["prime_id"]
PRIME_NAME = config["prime_name"]
CPR_NON_WORK = config["cpr_non_work"]


xlsxList = [file for file in os.listdir(pathFolderInData) if file.endswith(".xlsx") or file.endswith(".xlsm")]
parsedData = Parser.parse_cpr_xlsx_bulk(xlsxList, pathFolderInData, pathFolderOutData, PATH_LOG_PARSER)

currentDataSet = parsedData[0]
print(f"Running file: ({currentDataSet["header"]["payroll_number"]})")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width":1280, "height":1440},
        # viewport={"width":960, "height":1080},
        # record_video_dir="videos",
        # record_video_size={"width":960, "height":1080}
    )
    page = context.new_page()
    page.goto("https://services.dir.ca.gov/gsp")

    Automate.s0_log_in(page, USERNAME, PASSWORD, PATH_LOG_AUTOMATE)
    Automate.s1_dismiss_announcement(page, PATH_LOG_AUTOMATE)

    if CPR_OPEN:
        Automate.s1_project_dir_cpr_view(page, PROJECT_DIR, PATH_LOG_AUTOMATE)
        Automate.s2_cpr_index_id_open(page, CPR_ID, PATH_LOG_AUTOMATE)
    else:
        Automate.s1_project_dir_cpr_new(page, PROJECT_DIR, PATH_LOG_AUTOMATE)
    
    if CPR_NON_WORK:
        Automate.s3_cpr_fill_non_work(page, PRIME_ID, PRIME_NAME, currentDataSet, PATH_LOG_AUTOMATE)
    else:
        Automate.s3_cpr_fill(page, PRIME_ID, PRIME_NAME, currentDataSet, PATH_LOG_AUTOMATE)

    # ---------------------
    context.close()
    browser.close()

#Payroll ID PRRUN2466494



with sync_playwright() as playwright:
    run(playwright)
