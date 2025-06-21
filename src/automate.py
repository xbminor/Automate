import re
from datetime import datetime
from playwright.sync_api import Page, TimeoutError, expect, Locator


STATUS_CODES= {
    0: "PASS",
    1: "ERROR",
    2: "LOG",
}


def LogToFile(status: int, msg: str, filePath: str, isPrint: bool):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status = STATUS_CODES.get(status, f"UNKNOWN ({status})")
    log = f"{timestamp} - {status} - {msg}"
    with open(filePath, "a", encoding="utf-8") as f:
        f.write(f"{log}\n")
    
    if isPrint:
        print(log)


def Login(page: Page, username: str, password: str, logPath: str) -> bool:
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

        msg = f"<Login> Logged in as ({username})."
        LogToFile(0, msg, logPath, True)
        return True

    except Exception as e:
        msg = f"<Login> ({username}): {e}."
        LogToFile(1, msg, logPath, True)
        return False
    

def DismissAnnoucement(page: Page, logPath: str) -> bool:
    try:
        button = page.get_by_role("button", name="Dismiss announcement")
        if button.is_visible(timeout=5000) and button.is_enabled():
            button.click()
            msg ="<Dismiss> Announcement removed."
            LogToFile(2, msg, logPath, True)
            return True
    except:
        msg = "<Dismiss> No announcement present."
        LogToFile(2, msg, logPath, True)
        return False


def ProjectSearchDirToView(page: Page, dir: str, logPath: str) -> Locator:
    try:
        dir = dir.strip()

        # verify correct page
        page.wait_for_selector('text=My Projects', timeout=5000)

        searchTextBox = page.get_by_role("textbox", name="Keyword Search")
        searchTextBox.scroll_into_view_if_needed()
        searchTextBox.fill("")
        searchTextBox.fill(dir)

        msg = f"<ProjSearchDirView> Searching 'My Projects' for matching DIR Number as ({dir})."
        LogToFile(2, msg, logPath, True)
    
        searchBox = page.get_by_role("button", name="Search", exact=True)
        searchBox.click()

        searchTable = page.get_by_role("table", name="My Projects")
        searchTable.scroll_into_view_if_needed()
        
        # Verify unique search results
        projectRow = searchTable.locator("tbody tr")
        expect(projectRow).to_have_count(1, timeout=5000)

        projectName = projectRow.locator("td").nth(0).text_content().strip()
        msg = f"<ProjSearchDirView> {projectRow.count()} result found as ({projectName})."
        LogToFile(0, msg, logPath, True)

        projectRow.get_by_role("button", name="View eCPRs", exact=True).click()
        return projectRow

    except Exception as e:
        msg = f"<ProjSearchDirView> ({dir}): {e}."
        LogToFile(1, msg, logPath, True)
        return None


# page.locator("button").filter(has_text="Submit Manual eCPR").click()
def PayrollIndexIdToOpen(page: Page, id: str, logPath: str) -> bool:
    try:
        id = id.strip()

        # verify correct page
        page.wait_for_selector('text=Payroll Runs', timeout=5000)

        # Find the matching row that contains the correct rowheader as id
        msg = f"<PayIndexIdOpen> Indexing 'Payroll Runs' for matching Payroll ID as ({id})."
        LogToFile(2, msg, logPath, True)
        payrollTable = page.get_by_role("table", name="Payroll Runs")
        payrollRow = payrollTable.locator("tr", has=page.get_by_role("rowheader", name=id, exact=True))

        if payrollRow.count() == 0:
            msg = f"<PayIndexIdOpen> ({id}), payroll table is empty: {e}"
            LogToFile(1, msg, logPath, True)
            return False

        # Verify the exact match
        payrollRowHeaderCell = payrollRow.get_by_role("rowheader").first
        expect(payrollRowHeaderCell).to_have_text(id, timeout=5000)

        idMatch = payrollRowHeaderCell.text_content().strip()
        msg = f"<PayIndexIdOpen> Found matching ID ({idMatch}), opening eCPR."
        LogToFile(0, msg, logPath, True)

        payrollRow.get_by_role("button", name="Open eCPR", exact=True).click()
        return True
    
    except Exception as e:
        msg = f"<PayIndexIdOpen> ({id}): {e}"
        LogToFile(1, msg, logPath, True)
        return False
