import re
import src.util as Util
from datetime import date
from playwright.sync_api import Page, TimeoutError, expect, Locator

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


def s2_cpr_index_id_open(page: Page, id: str, logPath: str) -> bool:
    try:
        id = id.strip()

        # verify correct page
        page.wait_for_selector('text=Payroll Runs', timeout=5000)

        # Find the matching row that contains the correct rowheader as id
        msg = f"<s2_cpr_index_id_open> Indexing 'Payroll Runs' for matching Payroll ID as ({id})."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)

        while True:
            payrollTable = page.get_by_role("table", name="Payroll Runs")
            payrollRow = payrollTable.locator("tr", has_text=id)

            if payrollRow.count() > 0:
                break

            nav = page.locator('.col-md-12').first.get_by_role("navigation")
            navPageNext = nav.get_by_role("link", name="Next Page")
            if navPageNext.is_enabled():
                navPageNext.click()
                page.wait_for_timeout(2000)

        # Verify the exact match
        payrollRowHeaderCell = payrollRow.nth(0).locator("td").nth(1)
        expect(payrollRowHeaderCell).to_have_text(id, timeout=5000)

        idMatch = payrollRowHeaderCell.text_content().strip()
        msg = f"<s2_cpr_index_id_open> Found matching ID ({idMatch}), opening eCPR."
        Util.log_message(Util.STATUS_CODES.PASS, msg, logPath, True)

        payrollRow.get_by_role("button", name="Open eCPR", exact=True).click()
        return True
    
    except Exception as e:
        msg = f"<s2_cpr_index_id_open> ({id}): {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return False



def s3_cpr_fill_non_work(page: Page, primeId: str, primeName: str, data: dict, logPath: str) -> bool:
    header = data["header"]

    try:
        ### ****************************** Payroll Setup ***************************** ### 

        workPerformanceButton = page.get_by_text("Non-Performance No work was").get_by_role("radio")
        if workPerformanceButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Work performace is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            workPerformanceButton.check()
            msg = f"<s3_cpr_fill_from_open> Work performace is set to regular."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)


        finalPayrollButton = page.get_by_role("radio", name="No", exact=True)
        if finalPayrollButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Final payroll is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            msg = f"<s3_cpr_fill_from_open> Final payroll is set to No."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            finalPayrollButton.check()

        clearButton = page.get_by_role("button", name="Clear field subcontractor")
        if clearButton.is_visible():
            clearButton.click()
    
        page.get_by_role("link", name="Lookup using list").click()
        page.get_by_label("", exact=True).fill(primeId)

        page.get_by_role("option", name=primeName).click()
        msg = f"<s3_cpr_fill_from_open> Contract with ({primeName}) as ({primeId})."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)

        page.locator(".main-content").click()
        page.get_by_role("button", name="Save").click()
        print(f"Completed payroll, now saving.")
        page.wait_for_timeout(5000)


        ### ************************************************************************** ###
    
    except Exception as e:
        msg = f"<s3_cpr_fill_from_open>: {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None
    
    






def s3_cpr_fill(page: Page, primeId: str, primeName: str, data: dict, logPath: str) -> bool:
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
        page.get_by_label("", exact=True).fill(primeId)

        page.get_by_role("option", name=primeName).click()
        msg = f"<s3_cpr_fill_from_open> Contract with ({primeName}) as ({primeId})."
        Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)


        payrollPeriodButton = page.get_by_role("radio", name="Weekly", exact=True)
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

        page.locator(".main-content").click()
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

        page.wait_for_timeout(2000)

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
        
        for i in range(len(employeeNavSectionButtons)):
            # if employeeNavSectionButtons[i]["name"] == "Nathan Hayes":
            #     continue

            employeePayrollToProcess = employees[employeeNavSectionButtons[i]["name"]]
            print(f"Entering payroll information for ({employeeNavSectionButtons[i]["name"]}).")
            employeeNavSectionButtons[i]["button"].click()

            _fillEmployeePayroll(page, employeePayrollToProcess, header["week_starting"])

            page.wait_for_timeout(2000)
            print(f"Completed payroll information for ({employeeNavSectionButtons[i]["name"]}).")


        ### ************************************************************************** ###

        page.get_by_role("button", name="Save").click()
        print(f"Completed payroll, now saving.")
        page.wait_for_timeout(5000)

        return

    except Exception as e:
        msg = f"<s3_cpr_fill_from_open>: {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None
    



def _combox_select_option(container: Locator, strLabel: str, strOption: str):
    label = container.get_by_text(strLabel)
    combox = label.locator("xpath=following::select").first
    combox.select_option(strOption)


def _spin_fill(container: Locator, sectionTitle: str, listHours: list[dict]) -> list[Locator]:
    label = container.get_by_text(sectionTitle)
    spinbuttons = label.locator("xpath=following::input[@role='spinbutton']")
    for i, spin in enumerate([spinbuttons.nth(i) for i in range(7)]):
        spin.fill(listHours[i]["value"])



def _fillEmployeePayrollClass(page: Page, payroll: list[dict], weekStart: str, countClasses: int, sectionWorkClass: Locator):

    isFringe = False
    payrollInfo = payroll["class"][countClasses]
    if payrollInfo["work_classification"] == "Laborer Grp 2":
        _combox_select_option(sectionWorkClass, f"Craft paid {countClasses+1}:", "Laborer and Related Classifications")
        _combox_select_option(sectionWorkClass, f"Classification paid {countClasses+1}:", "Construction Laborers Including Bridge Laborers, General Laborers And Cleanup Laborers -")
        _combox_select_option(sectionWorkClass, "Level:", "Journeyman")
        isFringe = True
    
    elif payrollInfo["work_classification"] == "Operator Grp 3 N" or payrollInfo["work_classification"] == "Operator Grp 3":
        _combox_select_option(sectionWorkClass, f"Craft paid {countClasses+1}:", "Operating Engineer (Heavy and Highway Work)")
        _combox_select_option(sectionWorkClass, f"Classification paid {countClasses+1}:", "Other (Please specify)")
        texboxClass = sectionWorkClass.get_by_text("Other Classification (Please specify):") 
        texboxClass.fill("Group 3")
        _combox_select_option(sectionWorkClass, "Level:", "Journeyman")
        isFringe = False
    
    elif payrollInfo["work_classification"] == "Cement Mason":
        _combox_select_option(sectionWorkClass, f"Craft paid {countClasses+1}:", "Cement Mason")
        _combox_select_option(sectionWorkClass, f"Classification paid {countClasses+1}:", "Cement Mason -")
        _combox_select_option(sectionWorkClass, "Level:", "Journeyman")
        isFringe = False

    elif payrollInfo["work_classification"] == "DMP Truck Driver" or payrollInfo["work_classification"] == "Dump Truck Driver RT" or payrollInfo["work_classification"] == "Dump Truck Driver":
        _combox_select_option(sectionWorkClass, f"Craft paid {countClasses+1}:", "Driver (On/Off-Hauling to/from Construction Site)")
        _combox_select_option(sectionWorkClass, f"Classification paid {countClasses+1}:", "Other (Please specify)")
        texboxClass = sectionWorkClass.get_by_text("Other Classification (Please specify):") 
        texboxClass.fill("Dump Truck")
        _combox_select_option(sectionWorkClass, "Level:", "Journeyman")
        isFringe = False

    elif payrollInfo["work_classification"] == "Apprentice" or payrollInfo["work_classification"] == "Apprentice 1" or payrollInfo["work_classification"] == "Apprentice Period 1":
        _combox_select_option(sectionWorkClass, f"Craft paid {countClasses+1}:", "Laborer and Related Classifications")
        _combox_select_option(sectionWorkClass, f"Classification paid {countClasses+1}:", "Construction Laborers Including Bridge Laborers, General Laborers And Cleanup Laborers -")
        _combox_select_option(sectionWorkClass, "Level:", "Apprentice")
        _combox_select_option(sectionWorkClass, "Apprentice Period:", "2")
        isFringe = True
    
    elif payrollInfo["work_classification"] == "Foreman" or payrollInfo["work_classification"] == "Foreman/Laborer":
        _combox_select_option(sectionWorkClass, f"Craft paid {countClasses+1}:", "Laborer and Related Classifications")
        _combox_select_option(sectionWorkClass, f"Classification paid {countClasses+1}:", "Other (Please specify)")
        texboxClass = sectionWorkClass.get_by_text("Other Classification (Please specify):") 
        texboxClass.fill("Foreman")
        _combox_select_option(sectionWorkClass, "Level:", "Journeyman")


        isFringe = True if payroll["employee_name"] == "Nathan A Hayes" else False
    
    
    if payrollInfo["work_pay_type_RT"]:
        _spin_fill(sectionWorkClass, "Straight Time", payrollInfo["hours_rt"])

    if payrollInfo["work_pay_type_OT"]:
        linkOvertime = sectionWorkClass.get_by_role("link", name="Add Overtime")
        if linkOvertime.is_visible():
            linkOvertime.first.click()
       
        _spin_fill(sectionWorkClass, "Over Time", payrollInfo["hours_ot"])
        
    if payrollInfo["work_pay_type_DT"]:
        linkDoubletime = sectionWorkClass.get_by_role("link", name="Add Doubletime")
        if linkDoubletime.is_visible():
            linkDoubletime.first.click()

        _spin_fill(sectionWorkClass, "Double Time", payrollInfo["hours_dt"])
    
    

    sectionFringe = page.locator(".journey-level-section")
    listSpinFringe = [sectionFringe.get_by_role("spinbutton").nth(i) for i in range(20)]

    sectionBenefit = page.locator(".benefit-question")
    listCheckBenefit = [sectionBenefit.get_by_role("checkbox").nth(i) for i in range(4)]

    if isFringe:
        listCheckBenefit[0+2*countClasses].check()
        listCheckBenefit[1+2*countClasses].uncheck()

        fringeRates = None
        dateWeekStart = Util.string_to_date(weekStart)
        for fringeRatePlan in FRINGE_RATES:
            if fringeRatePlan["start"] <= dateWeekStart <= fringeRatePlan["end"]:
                fringeRates = fringeRatePlan["rates"]

        listSpinFringe[1+10*countClasses].fill(fringeRates["hnw"])
        listSpinFringe[2+10*countClasses].fill(fringeRates["pen"])
        listSpinFringe[3+10*countClasses].fill(fringeRates["vac"])
        listSpinFringe[4+10*countClasses].fill(fringeRates["trn"])
        listSpinFringe[5+10*countClasses].fill(fringeRates["oth"])

    else:
        listCheckBenefit[0+2*countClasses].uncheck()
        listCheckBenefit[1+2*countClasses].check()


    listSpinFringe[0+10*countClasses].fill(payrollInfo["work_pay_rate_rt"])
    listSpinFringe[6+10*countClasses].fill(payrollInfo["work_pay_rate_ot"])
    listSpinFringe[7+10*countClasses].fill(payrollInfo["work_pay_rate_dt"])

    print(f"\tEntered: {payrollInfo["work_classification"]}")




def _fillEmployeePayroll(page: Page, payrollInfo, weekStart):
    page.locator("#positiveNumber_1").fill("")
    page.locator("#positiveNumber_1").fill(payrollInfo["work_pay_check_num"])
    
    sectionWorkClass1 = page.locator(".classification-section").first
    sectionWorkClass2 = page.get_by_text("Remove Classification * Craft")
    
    _fillEmployeePayrollClass(page, payrollInfo, weekStart, 0, sectionWorkClass1)
    if len(payrollInfo["class"]) > 1:
        if sectionWorkClass2.is_hidden():
            page.locator(".add-classification").first.click()

        _fillEmployeePayrollClass(page, payrollInfo, weekStart, 1, sectionWorkClass2)

    sectionDeduction = page.get_by_text("Deductions (per payroll) Federal Tax FICA (Soc. Sec.) State Tax SDI Dues Fund/")
    listSpinDeduction = [sectionDeduction.get_by_role("spinbutton").nth(i) for i in range(4)]
    fica = f"{float(payrollInfo['work_pay_tax_social']) + float(payrollInfo['work_pay_tax_medic']):.2f}"

    listSpinDeduction[0].fill(payrollInfo["work_pay_tax_fed"])
    listSpinDeduction[1].fill(fica)
    listSpinDeduction[2].fill(payrollInfo["work_pay_tax_state"])
    listSpinDeduction[3].fill(payrollInfo["work_pay_tax_other"])

    # Gross wages
    grossWageButton =  page.locator("#positiveNumber_12")
    grossWageButton.fill(payrollInfo["work_pay_gross_total"])

    page.locator(".main-content").click()

    return