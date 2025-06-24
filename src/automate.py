import re
import src.util as Util
from datetime import datetime
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



def s3_cpr_fill_from_open(page: Page, data, logPath: str) -> bool:
    fakeData = {
        "primeCode" : "113061",
        "primeName" : "HARRIS CONSTRUCTION CO INC",
        "weekStart" : "2024-06-09",
        "weekEnd" : "2024-06-15",
    }
    fakeEmployees = [
        "Derrick Rye",
        "Fernando Hernandez",
        "Gerardo Lunar-Rodriguez",
        "Juan Torres-Martinez",
        "Oliver Browner"
    ]

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

        
        
        payrollDateButton = page.locator(f"input[name=\"firstdate\"]")
        if payrollDateButton.is_disabled():
            msg = f"<s3_cpr_fill_from_open> Payroll date is disabled."
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
        else:
            msg = f"<s3_cpr_fill_from_open> Payroll date is set to ({fakeData['weekStart']})"
            Util.log_message(Util.STATUS_CODES.LOG, msg, logPath, True)
            payrollDateButton.fill(fakeData['weekStart'])


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

        for name in fakeEmployees:
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



        ### ************************************************************************** ###

        return

    except Exception as e:
        msg = f"<s3_cpr_fill_from_open>: {e}."
        Util.log_message(Util.STATUS_CODES.FAIL, msg, logPath, True)
        return None