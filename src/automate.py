import re
import src.util as Util
from datetime import date
from playwright.sync_api import Page, TimeoutError, expect, Locator



def s0_log_in(page: Page, username: str, password: str, logPath: str) -> bool:
    try:
        page.get_by_role("link", name="Log in").click(timeout=5000)

        usernameBox = page.get_by_role("textbox", name="User name / Email")
        usernameBox.fill("")
        usernameBox.fill(username)

        passwordBox = page.get_by_role("textbox", name="Password")
        passwordBox.fill("")
        passwordBox.fill(password)

        page.get_by_role("button", name="Log in").click()

        page.wait_for_selector('text=My Projects', timeout=5000)

        msg = f"<s0_log_in> Logged in as ({username})."
        Util.log_message(Util.STATUS_CODES.PASS, msg, logPath, True)
        return True

    except Exception as e:
        msg = f"<s0_log_in> ({username}): {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return False
    

def s1_dismiss_announcement(page: Page, logPath: str) -> bool:
    try:
        button = page.get_by_role("button", name="Dismiss announcement")
        if button.is_visible(timeout=5000) and button.is_enabled():
            button.click()
            msg ="<s1_dismiss> Announcement removed."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            return True
    except:
        msg = "<s1_dismiss> No announcement present."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        return False
    

def _s1_project_search_dir(page: Page, dir: str, logPath: str) -> Locator:
    try:
        dir = dir.strip()

        # verify correct page
        page.wait_for_selector('text=My Projects', timeout=5000)

        searchTextBox = page.get_by_role("textbox", name="Keyword Search")
        searchTextBox.scroll_into_view_if_needed()
        searchTextBox.fill("")
        searchTextBox.fill(dir)

        msg = f"<_s1_project_search_dir> Searching 'My Projects' for matching DIR Number as ({dir})."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
    
        searchBox = page.get_by_role("button", name="Search", exact=True)
        searchBox.click()

        searchTable = page.get_by_role("table", name="My Projects")
        searchTable.scroll_into_view_if_needed()
        
        # Verify unique search results
        projectRow = searchTable.locator("tbody tr")
        expect(projectRow).to_have_count(1, timeout=5000)

        projectName = projectRow.locator("td").nth(0).text_content().strip()
        msg = f"<_s1_project_search_dir> {projectRow.count()} result found as ({projectName})."
        Util.log_message(Util.STATUS_CODES.PASS, msg, logPath, True)
        return projectRow

    except Exception as e:
        msg = f"<_s1_project_search_dir> ({dir}): {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None
    
    

def s1_project_dir_cpr_view(page: Page, dir: str, logPath: str) -> Locator:
    try:
        projectRow = _s1_project_search_dir(page, dir, logPath)
        if not projectRow:
            return None

        projectRow.get_by_role("button", name="View eCPRs", exact=True).click()
        return projectRow

    except Exception as e:
        msg = f"<s1_project_dir_cpr_view> ({dir}): {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None


def s1_project_dir_cpr_new(page: Page, dir: str, logPath: str) -> Locator:
    try:
        projectRow = _s1_project_search_dir(page, dir, logPath)
        if not projectRow:
            return None

        projectRow.get_by_role("button", name="Submit", exact=True).click()
        return projectRow

    except Exception as e:
        msg = f"<s1_project_dir_cpr_new> ({dir}): {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None


# page.locator("button").filter(has_text="Submit Manual eCPR").click()
def s2_payroll_index_id_open(page: Page, id: str, logPath: str) -> bool:
    try:
        id = id.strip()

        # verify correct page
        page.wait_for_selector('text=Payroll Runs', timeout=5000)

        # Find the matching row that contains the correct rowheader as id
        msg = f"<s2_payroll_index_id_open> Indexing 'Payroll Runs' for matching Payroll ID as ({id})."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        payrollTable = page.get_by_role("table", name="Payroll Runs")
        payrollRow = payrollTable.locator("tr", has=page.get_by_role("rowheader", name=id, exact=True))

        if payrollRow.count() == 0:
            msg = f"<s2_payroll_index_id_open> ({id}), payroll table is empty."
            Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
            return False

        # Verify the exact match
        payrollRowHeaderCell = payrollRow.get_by_role("rowheader").first
        expect(payrollRowHeaderCell).to_have_text(id, timeout=5000)

        idMatch = payrollRowHeaderCell.text_content().strip()
        msg = f"<s2_payroll_index_id_open> Found matching ID ({idMatch}), opening eCPR."
        Util.log_message(Util.STATUS_CODES.PASS, msg, logPath, True)

        payrollRow.get_by_role("button", name="Open eCPR", exact=True).click()
        return True
    
    except Exception as e:
        msg = f"<s2_payroll_index_id_open> ({id}): {e}"
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return False



def s3_cpr_fill_from_open(page: Page, data: dict, logPath: str) -> bool:
    fakeData = {
        "primeCode" : "113061",
        "primeName" : "HARRIS CONSTRUCTION CO INC",
    }
    header = data["header"]
    employees = data["employees"]
    employeeNames = [employee for employee in employees]

    try:
        ### ****************************** Payroll Setup ***************************** ### 

        workPerformanceButton = page.get_by_role("radio", name="Regular Non-Performance")
        if workPerformanceButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Work performace is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            workPerformanceButton.check()
            msg = f"<s3_cpr_fill_from_open> Work performace is set to regular."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        # non performance not supported
        # needs search for generated name
        # non-performance -- page.locator("input[name=\"397\"]").check()


        finalPayrollButton = page.get_by_role("radio", name="No", exact=True)
        if finalPayrollButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Final payroll is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            msg = f"<s3_cpr_fill_from_open> Final payroll is set to No."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            finalPayrollButton.check()
        #final -- page.get_by_role("radio", name="Yes").check()
        
        # page.wait_for_timeout(1000)

        clearButton = page.get_by_role("button", name="Clear field subcontractor")
        if clearButton.is_visible():
            clearButton.click()
    
        page.get_by_role("link", name="Lookup using list").click()
        page.get_by_label("", exact=True).fill(fakeData["primeCode"])

        page.get_by_role("option", name=fakeData["primeName"]).click()
        msg = f"<s3_cpr_fill_from_open> Contract with ({fakeData['primeName']}) as ({fakeData['primeCode']})."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)


        payrollPeriodButton = page.get_by_role("radio", name="Weekly Bi-weekly Semi-monthly")
        if payrollPeriodButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Payroll period is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            msg = f"<s3_cpr_fill_from_open> Payroll period is set to weekly."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            payrollPeriodButton.check()

        
        weekStart = header['week_starting']
        payrollDateButton = page.locator(f"input[name=\"firstdate\"]")
        if payrollDateButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Payroll date is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            msg = f"<s3_cpr_fill_from_open> Payroll date is set to ({weekStart})"
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            payrollDateButton.fill(weekStart)


        page.wait_for_timeout(2000)

        button = page.locator(".main-content button").last
        if "next step" in button.text_content().strip().lower(): 
            msg = f"<s3_cpr_fill_from_open> Payroll Setup complete, continue to next step."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            button.click()
        else:
            msg = f"<s3_cpr_fill_from_open> Payroll Setup incomplete, unable to find next step button."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)

        ### ************************************************************************** ###



        ### *************************** Employee Selections ************************** ###

        for name in employeeNames:
            row = page.get_by_role("row", name=f"{name} ")
            if not row:
                msg = f"<s3_cpr_fill_from_open> Did not find employee ({name})."
                Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
                return False
            checkbox = row.get_by_role("checkbox")
            
            if not checkbox.is_checked():
                checkbox.check()
                msg = f"<s3_cpr_fill_from_open> Employee checked: ({name})."
                Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            else:
                msg = f"<s3_cpr_fill_from_open> Employee already checked: ({name})."
                Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)


        page.wait_for_timeout(2000)
        
        button = page.locator(".main-content button").last
        if "next step" in button.text_content().strip().lower(): 
            msg = f"<s3_cpr_fill_from_open> Employee Selection complete, continue to next step."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            button.click()
        else:
            msg = f"<s3_cpr_fill_from_open> Employee Selection incomplete, unable to find next step button."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        ### ************************************************************************** ###

        
        ### *************************** Payroll Information ************************** ###

        page.wait_for_timeout(2000)

        navigationSection = page.get_by_role("navigation")
        payrollInfoNavSectionButton = navigationSection.get_by_role("button", name=re.compile(r"Payroll Information", re.IGNORECASE))
        payrollInfoNavSectionButton.click()

        employeeNavSectionButtons = []

        reverseLookup = {}
        for firstLast in employeeNames:
            lastFirst = Util.name_to_last_first(firstLast)
            reverseLookup[lastFirst] = firstLast


        payrollInfoNavSectionUpdated = navigationSection.get_by_role("button")
        for i in range(payrollInfoNavSectionUpdated.count()):
            button = payrollInfoNavSectionUpdated.nth(i)
            text = button.text_content().strip()
    
            for reverseName in reverseLookup:
                if reverseName in text:
                    print(f"match found: ({text}) with ({reverseName}).")

                    employeeNavSectionButtons.append({
                        "name": reverseLookup[reverseName],
                        "button": button
                    })

        
        if len(employeeNavSectionButtons) is not len(employeeNames):
            print("Section employee buttons is not matching employee count")
            return 
        
        for i in range(len(employeeNavSectionButtons)):
            employeePayrollToProcess = employees[employeeNavSectionButtons[i]["name"]]
            print(f"Entering payroll information for ({employeeNavSectionButtons[i]["name"]}).")
            employeeNavSectionButtons[i]["button"].click()

            _fillEmployeePayrollInfo(page, employeePayrollToProcess, header["week_starting"])

            page.wait_for_timeout(2000)
            print(f"Completed payroll information for ({employeeNavSectionButtons[i]["name"]}).")


        ### ************************************************************************** ###

        return

    except Exception as e:
        msg = f"<s3_cpr_fill_from_open>: {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None
    


def _fillEmployeePayrollInfo(page: Page, payrollInfo, weekStart):
    page.locator("input[type=\"text\"]").fill("")
    page.locator("input[type=\"text\"]").fill(payrollInfo["work_pay_check_num"])

    isFringe = False
    if payrollInfo["work_classification"] == "Laborer Grp 2":
        page.locator("#craftPaid0").select_option("4bbbecb687644650c837eb1e3fbb354e")
        page.locator("#classPaid0").select_option("5548654ddb0c1a104489543ed39619bc")
        page.locator("#classPaid1").select_option("journeyman")
        isFringe = True
    
    elif payrollInfo["work_classification"] == "Operator Grp 3 N" or payrollInfo["work_classification"] == "Operator Grp 3":
        page.locator("#craftPaid0").select_option("cfbbecb687644650c837eb1e3fbb3552")
        page.locator("#classPaid0").select_option("3201f85687778ed4c837eb1e3fbb35cd")
        page.locator("#classPaid1").select_option("journeyman")
        page.locator("#other-classification").fill("Group 3")
        isFringe = False
    
    elif payrollInfo["work_classification"] == "Cement Mason":
        page.locator("#craftPaid0").select_option("c7bbecb687644650c837eb1e3fbb3546")
        page.locator("#classPaid0").select_option("0734d981dbc81a104489543ed39619e1")
        page.locator("#classPaid1").select_option("journeyman")
        isFringe = False

    elif payrollInfo["work_classification"] == "Driver":
        page.locator("#craftPaid0").select_option("47bbecb687644650c837eb1e3fbb3548")
        page.locator("#classPaid0").select_option("ee01f85687778ed4c837eb1e3fbb35b7")
        page.locator("#other-classification").fill("Dump Truck")
        isFringe = False

    elif payrollInfo["work_classification"] == "Apprentice" or payrollInfo["work_classification"] == "Apprentice 1":
        page.locator("#craftPaid0").select_option("4bbbecb687644650c837eb1e3fbb354e")
        page.locator("#classPaid0").select_option("5548654ddb0c1a104489543ed39619bc")
        page.locator("#classPaid1").select_option("apprentice")
        page.get_by_role("combobox").nth(3).select_option("number:2")
        isFringe = True
    
    
    if payrollInfo["work_pay_type_RT"]:
        # sunday
        rtSunButton = page.locator(".div-table-cell.ng-scope").first.get_by_role("spinbutton")
        rtSunButton.fill(payrollInfo["hours_rt"][0]["value"])

        # monday
        rtMonButton = page.locator(".div-table-body > div > div:nth-child(3)").first.get_by_role("spinbutton")
        rtMonButton.fill(payrollInfo["hours_rt"][1]["value"])

        # tuesday
        rtTueButton = page.locator(".div-table-body > div > div:nth-child(4)").first.get_by_role("spinbutton")
        rtTueButton.fill(payrollInfo["hours_rt"][2]["value"])

        # wednesday
        rtWedButton = page.locator(".div-table-body > div > div:nth-child(5)").first.get_by_role("spinbutton")
        rtWedButton.fill(payrollInfo["hours_rt"][3]["value"])

        # thursday
        rtThuButton = page.locator(".div-table-body > div > div:nth-child(6)").first.get_by_role("spinbutton")
        rtThuButton.fill(payrollInfo["hours_rt"][4]["value"])

        # friday
        rtFriButton = page.locator(".div-table-body > div > div:nth-child(7)").first.get_by_role("spinbutton")
        rtFriButton.fill(payrollInfo["hours_rt"][5]["value"])

        # saturday
        rtSatButton = page.locator(".div-table-body > div > div:nth-child(8)").first.get_by_role("spinbutton")
        rtSatButton.fill(payrollInfo["hours_rt"][6]["value"])


    if payrollInfo["work_pay_type_OT"]:
        overtimeLink = page.locator("a").filter(has_text="Add Overtime")
        if overtimeLink.count() > 0:
            overtimeLink.first.click()
        else:
            print("Overtime already added.")
        
        # sunday
        otSunButton = page.locator(".div-table-body > div:nth-child(2) > div:nth-child(2)").get_by_role("spinbutton")
        otSunButton.fill(payrollInfo["hours_ot"][0]["value"])

        # monday
        otMonButton = page.locator(".div-table-body > div:nth-child(2) > div:nth-child(3)").get_by_role("spinbutton")
        otMonButton.fill(payrollInfo["hours_ot"][1]["value"])

        # tuesday
        otTueButton = page.locator(".div-table-body > div:nth-child(2) > div:nth-child(4)").get_by_role("spinbutton")
        otTueButton.fill(payrollInfo["hours_ot"][2]["value"])

        # wednesday
        otWedButton = page.locator("div:nth-child(2) > div:nth-child(5)").get_by_role("spinbutton")
        otWedButton.fill(payrollInfo["hours_ot"][3]["value"])

        # thursday
        otThuButton = page.locator("div:nth-child(2) > div:nth-child(6)").get_by_role("spinbutton")
        otThuButton.fill(payrollInfo["hours_ot"][4]["value"])

        # friday
        otFriButton = page.locator("div:nth-child(2) > div:nth-child(7)").get_by_role("spinbutton")
        otFriButton.fill(payrollInfo["hours_ot"][5]["value"])

        # saturday
        otSatButton = page.locator("div:nth-child(2) > div:nth-child(8)").get_by_role("spinbutton")
        otSatButton.fill(payrollInfo["hours_ot"][6]["value"])


    if payrollInfo["work_pay_type_DT"]:
        page.get_by_role("link", name="Add Doubletime").click()
        
        # sunday
        dtSunButton = page.locator(".div-table-body > div:nth-child(3) > div:nth-child(2)").get_by_role("spinbutton")
        dtSunButton.fill(payrollInfo["hours_dt"][0]["value"])

        # monday
        dtMonButton = page.locator(".div-table-body > div:nth-child(3) > div:nth-child(3)").get_by_role("spinbutton")
        dtMonButton.fill(payrollInfo["hours_dt"][1]["value"])

        # tuesday
        dtTueButton = page.locator("div:nth-child(3) > div:nth-child(4)").get_by_role("spinbutton")
        dtTueButton.fill(payrollInfo["hours_dt"][2]["value"])

        # wednesday
        dtWedButton = page.locator("div:nth-child(3) > div:nth-child(5)").get_by_role("spinbutton")
        dtWedButton.fill(payrollInfo["hours_dt"][3]["value"])

        # thursday
        dtThuButton = page.locator("div:nth-child(3) > div:nth-child(6)").get_by_role("spinbutton")
        dtThuButton.fill(payrollInfo["hours_dt"][4]["value"])

        # friday
        dtFriButton = page.locator("div:nth-child(3) > div:nth-child(7)").get_by_role("spinbutton")
        dtFriButton.fill(payrollInfo["hours_dt"][5]["value"])

        # saturday
        dtSatButton = page.locator("div:nth-child(3) > div:nth-child(8)").get_by_role("spinbutton")
        dtSatButton.fill(payrollInfo["hours_dt"][6]["value"])
    

    # page.get_by_role("link", name="Remove Doubletime").click()
    # page.get_by_role("link", name="Remove Overtime").click()

    if isFringe:
        page.locator("#fringeYes0").check()

        FRINGE_RATES = [
            {
                "start": date(2023, 7, 1),
                "end": date(2024, 6, 30),
                "rates": {
                    "hnw": "10.10",
                    "pen": "14.36",
                    "vac": "3.26",
                    "trn": "0.52",
                    "oth": "0.32"
                }
            },
            {
                "start": date(2024, 7, 1),
                "end": date(2025, 6, 30),
                "rates": {
                    "hnw": "10.60",
                    "pen": "14.96",
                    "vac": "3.51",
                    "trn": "0.52",
                    "oth": "0.32"
                }
            },
        ]

        fringeRates = None
        dateWeekStart = Util.string_to_date(weekStart)
        for fringeRatePlan in FRINGE_RATES:
            if fringeRatePlan["start"] <= dateWeekStart <= fringeRatePlan["end"]:
                fringeRates = fringeRatePlan["rates"]
                print(f"Selected rates between ({fringeRatePlan["start"]}) and ({fringeRatePlan["end"]})")

        # Health / Welfare 
        fringeButtonHNW = page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(2)").first.get_by_role("spinbutton")
        fringeButtonHNW.fill(fringeRates["hnw"])

        # Pension
        fringeButtonPEN = page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(3)").first.get_by_role("spinbutton")
        fringeButtonPEN.fill(fringeRates["pen"])

        # Vacation / Holiday
        fringeButtonVAC = page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(4)").first.get_by_role("spinbutton")
        fringeButtonVAC.fill(fringeRates["vac"])

        # Training
        fringeButtonTRN = page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(8)").get_by_role("spinbutton")
        fringeButtonTRN.fill(fringeRates["trn"])

        #Other
        fringeButtonOTH = page.locator(".div-table > .div-table-body > .div-table-row > div:nth-child(9)").get_by_role("spinbutton")
        fringeButtonOTH.fill(fringeRates["oth"])
    else:
        page.locator("#fringeNo0").check()

    # RT Rate
    fringeRTRateButton = page.locator(".div-table > .div-table-body > .div-table-row > div").first.get_by_role("spinbutton")
    fringeRTRateButton.fill(payrollInfo["work_pay_rate_rt"])

    # OT Rate
    fringeOTRateButton = page.locator(".div-table-body > .div-table-row > div:nth-child(10)").get_by_role("spinbutton")
    fringeOTRateButton.fill(payrollInfo["work_pay_rate_ot"])

    # DT Rate
    fringeDTRateButton = page.locator(".div-table-body > .div-table-row > div:nth-child(11)").get_by_role("spinbutton")
    fringeDTRateButton.fill(payrollInfo["work_pay_rate_dt"])


    # Federtal Tax
    taxFedButton = page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div").first.get_by_role("spinbutton")
    taxFedButton.fill(payrollInfo["work_pay_tax_fed"])

    # FICA
    fica = f"{float(payrollInfo['work_pay_tax_social']) + float(payrollInfo['work_pay_tax_medic']):.2f}"
    taxFICAButton = page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div:nth-child(2)").get_by_role("spinbutton")
    taxFICAButton.fill(fica)

    # State Tax
    taxStateButton = page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div:nth-child(3)").get_by_role("spinbutton")
    taxStateButton.fill(payrollInfo["work_pay_tax_state"])

    #SDI
    taxSDIButton = page.locator("div:nth-child(2) > .div-table-body > .div-table-row > div:nth-child(4)").get_by_role("spinbutton")
    taxSDIButton.fill(payrollInfo["work_pay_tax_other"])

    # Gross wages
    grossWageButton = page.locator(".wages-section > .div-table > .div-table-body > .div-table-row > .div-table-cell").get_by_role("spinbutton")
    grossWageButton.fill(payrollInfo["work_pay_gross_total"])

    return