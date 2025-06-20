import re
import json
import utils.browser_tools as bUtils
from playwright.sync_api import Playwright, sync_playwright, expect


with open(r".\config.json", "r") as configFile: 
    config = json.load(configFile)

USERNAME = config["username"]
PASSWORD = config["password"]
DIR = config["dir"]
ACCOUNT = config["account"]



def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        viewport={"width":1280, "height":1440},
        #viewport={"width":960, "height":1080},
        record_video_dir="videos",
        record_video_size={"width":960, "height":1080}
    )
    page = context.new_page()
    page.goto("https://services.dir.ca.gov/gsp")

    bUtils.Login(page, USERNAME, PASSWORD)
    bUtils.DismissAnnoucement(page)

    isValidDir = False
    validDirCount = 0

    while not isValidDir:
        page.get_by_role("textbox", name="Keyword Search").scroll_into_view_if_needed()
        page.get_by_role("textbox", name="Keyword Search").fill(DIR)
        page.get_by_role("button", name="Search", exact=True).click()

        page.wait_for_timeout(2000)

        searchTable = page.get_by_role("table", name="My Projects")
        searchTable.scroll_into_view_if_needed()

        rows = searchTable.locator("tbody tr")
        rowsCount = rows.count()

        if rowsCount > 0 and validDirCount < rowsCount:
            cell = rows.nth(validDirCount).locator("td").nth(0)
            cell.click()
        
            fieldsToCompare = ["Name", "Project ID", "Project Number", "Contract Number"]
            for field in fieldsToCompare:
                value = page.get_by_role("textbox", name=field).input_value()
                if value == DIR:
                    isValidDir = True
                    print("Match Found ", field, " is ", value, " matching with ", DIR)
                    break
            
            page.goto("https://services.dir.ca.gov/gsp")
            if not isValidDir:
                validDirCount+=1
        else:
            print("No matching projects found for ", DIR)
            return
        

    page.get_by_role("textbox", name="Keyword Search").scroll_into_view_if_needed()
    page.get_by_role("textbox", name="Keyword Search").fill(DIR)
    page.get_by_role("button", name="Search", exact=True).click()

    page.wait_for_timeout(2000)

    searchTable = page.get_by_role("table", name="My Projects")
    searchTable.scroll_into_view_if_needed()

    validDirRow = searchTable.locator("tbody tr").nth(validDirCount)
    columns = validDirRow.locator("td")

    for i in range(columns.count()):
        cell = columns.nth(i)
        cellText = cell.inner_text().strip()

        if cellText == "View eCPRs":
            cell.locator("a, button").click()
            break
    

    page.wait_for_timeout(2000)


    payrollTable = page.get_by_role("table", name="Payroll Runs")



    page.locator("button").filter(has_text="Submit Manual eCPR").click()
    
    
    page.get_by_role("radio", name="Regular Non-Performance").check()
    #non-performance -- page.locator("input[name=\"397\"]").check()
    
    page.get_by_role("radio", name="No", exact=True).check()
    #final -- page.get_by_role("radio", name="Yes").check()
    
    page.get_by_role("link", name="Lookup using list").click()
    page.get_by_label("", exact=True).fill("113061")
    page.get_by_role("option", name="HARRIS CONSTRUCTION CO INC").click()
    #entire search drop -- locator("#select2-drop")
    #search selection -- locator(".select2-search")
    #search type area -- get_by_label("", exact=True)

    page.get_by_role("radio", name="Weekly Bi-weekly Semi-monthly").check()

    page.locator("input[name=\"firstdate\"]").fill("2024-06-30")
    page.get_by_role("button", name="Next Step").click()

    page.wait_for_timeout(2000)

    page.get_by_role("row", name="Gerardo Lunar-Rodriguez ").get_by_role("checkbox").check()
    page.get_by_role("row", name="Juan Torres-Martinez ").get_by_role("checkbox").check()
    #sound important -- locator(".fixTableHead")
    #todo -- get_by_role("link", name="Add Employee")
    page.get_by_role("button", name="Next Step (0)").click()

    page.wait_for_timeout(2000)

    #for check which employee to start with -- locator(".main-content")
    #employees on side bar to open -- get_by_role("button", name=" Payroll Information Action").click()
    #page.get_by_role("button", name=" Torres-Martinez, Juan -").click()
    #page.get_by_role("button", name=" Lunar-Rodriguez, Gerardo -").click()


    ### **************************** Employee Section **************************** ### 
    


    ## --------------------- Check number --------------------- ##
    page.locator("input[type=\"text\"]").fill("2861")
    ## -------------------------------------------------------- ##


    ## -------------------- Classifcations -------------------- ##
    # Laborer and Related Classifications
    page.locator("#craftPaid0").select_option("4bbbecb687644650c837eb1e3fbb354e")
    page.locator("#classPaid0").select_option("5548654ddb0c1a104489543ed39619bc")

    # Cement Mason
    page.locator("#craftPaid0").select_option("c7bbecb687644650c837eb1e3fbb3546")
    page.locator("#classPaid0").select_option("0734d981dbc81a104489543ed39619e1")

    # Driver (On/Off-Hauling to/from Construction Site)
    page.locator("#craftPaid0").select_option("47bbecb687644650c837eb1e3fbb3548")
    page.locator("#classPaid0").select_option("ee01f85687778ed4c837eb1e3fbb35b7")
    page.locator("#other-classification").fill("Dump Truck")
   
    # Operating Engineer (Heavy and Highway Work)
    page.locator("#craftPaid0").select_option("cfbbecb687644650c837eb1e3fbb3552")
    page.locator("#classPaid0").select_option("3201f85687778ed4c837eb1e3fbb35cd")
    page.locator("#other-classification").fill("Group 3")

    page.locator("#classPaid1").select_option("journeyman")

    page.locator("#classPaid1").select_option("apprentice")
    page.get_by_role("combobox").nth(3).select_option("number:3")
    page.get_by_role("combobox").nth(3).select_option("number:1")
    ## -------------------------------------------------------- ##
    

    ## ------------------------- Time ------------------------- ##
    # might be everything -- page.locator(".classification-section").click()
    # might be table -- page.locator(".col-lg-12 > div > .div-table > div").click()
    # might be only RT,OT,DT -- page.get_by_text("Straight Time 0hr include").click()

    # sunday
    page.locator(".div-table-cell.ng-scope").first
    page.locator(".div-table-body > div:nth-child(2) > div:nth-child(2)")
    page.locator(".div-table-body > div:nth-child(3) > div:nth-child(2)")
    
    # monday
    page.locator(".div-table-body > div > div:nth-child(3)").first
    page.locator(".div-table-body > div:nth-child(2) > div:nth-child(3)")
    page.locator(".div-table-body > div:nth-child(3) > div:nth-child(3)")

    # tuesday
    page.locator(".div-table-body > div > div:nth-child(4)").first
    page.locator(".div-table-body > div:nth-child(2) > div:nth-child(4)")
    page.locator("div:nth-child(3) > div:nth-child(4)")

    # wednesday
    page.locator(".div-table-body > div > div:nth-child(5)").first
    page.locator("div:nth-child(2) > div:nth-child(5)")
    page.locator("div:nth-child(3) > div:nth-child(5)")

    # thursday
    page.locator(".div-table-body > div > div:nth-child(6)").first
    page.locator("div:nth-child(2) > div:nth-child(6)")
    page.locator("div:nth-child(3) > div:nth-child(6)")

    # friday
    page.locator(".div-table-body > div > div:nth-child(7)").first
    page.locator("div:nth-child(2) > div:nth-child(7)")
    page.locator("div:nth-child(3) > div:nth-child(7)")

    # saturday
    page.locator(".div-table-body > div > div:nth-child(8)").first
    page.locator("div:nth-child(2) > div:nth-child(8)")
    page.locator("div:nth-child(3) > div:nth-child(8)")

    page.get_by_role("link", name="Add Overtime").click()
    page.get_by_role("link", name="Add Doubletime").click()
    page.get_by_role("link", name="Remove Doubletime").click()
    page.get_by_role("link", name="Remove Overtime").click()
    ## -------------------------------------------------------- ##


    ## ------------------------ Fringe ------------------------ ##
    page.locator("#fringeYes0").check()
    page.locator("#fringeNo0").check()

    # might be data -- page.get_by_text("Hourly rates - Journey level Learn when to fill out fringe rates Basic Hourly").click()

    # RT Rate
    page.locator(".div-table > .div-table-body > .div-table-row > div").first

    # Health / Welfare 
    page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(2)").first

    # Pension
    page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(3)").first

    # Vacation / Holiday
    page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(4)").first

    # Training
    page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(8)")

    #Other
    page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(9)")

    # OT Rate
    page.locator(".div-table-body > .div-table-row > div:nth-child(10)")

    # DT Rate
    page.locator(".div-table-body > .div-table-row > div:nth-child(11)")

    # Total OT Rate
    page.locator(".div-table-body > .div-table-row > div:nth-child(13)")

    # Total DT Rate
    page.locator(".div-table-body > .div-table-row > div:nth-child(14)")
    ## -------------------------------------------------------- ##


    ## ----------------- Add Classifications ------------------ ##
    page.get_by_role("button", name="Add Craft/Classification/Level").click()
    page.get_by_role("button", name=" Remove Classification").click()
    ## -------------------------------------------------------- ##


    ## ---------------------- Deduction ----------------------- ##
    # Federtal Tax
    page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div").first

    # FICA
    page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div:nth-child(2)")

    # State Tax
    page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div:nth-child(3)")

    #SDI
    page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div:nth-child(4)")
    ## -------------------------------------------------------- ##


    ## --------------------- Gross Wages ---------------------- ##
    # Total Gross Pay (Gross Wages for all projects included in this check *)
    page.locator(".wages-section > .div-table > .div-table-body > .div-table-row > .div-table-cell").click()
    
    # row section header for net wages for all projects -- locator("div:nth-child(3) > .div-table-head")
    ## -------------------------------------------------------- ##


    ## ---------------------- Next Step ----------------------- ##
    # Next Employee
    page.get_by_role("button", name="Next Employee").click()

    # Next Step To Review
    page.get_by_role("button", name="Next Step").click()

    # Saving Progress
    page.get_by_role("button", name="Save").click()
    ## -------------------------------------------------------- ##
    
    
    
    ### ************************************************************************** ###





    ### ***************************** Reviews/Submit ***************************** ###


    ## ----------------------- Reviews ------------------------ ##
    # might be table -- locator(".empl-table")
    page.get_by_role("button", name="Next Step").click()
    ## -------------------------------------------------------- ##

    ## ----------------------- Signing ------------------------ ##
    page.get_by_role("textbox").first.fill(ACCOUNT)
    page.get_by_role("button", name="Sign and Submit", exact=True)
    ## -------------------------------------------------------- ##



    ### ************************************************************************** ###


    page.wait_for_timeout(10000)

    # ---------------------
    context.close()
    browser.close()



with sync_playwright() as playwright:
    run(playwright)

