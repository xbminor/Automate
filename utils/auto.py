from playwright.sync_api import Page, TimeoutError, expect, Locator

def Login(page: Page, username: str, password: str) -> bool:
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

        print("Login successful.")
        return True

    except TimeoutError:
        print("Login failed: timeout or element missing.")
        return False

    except Exception as e:
        print("Login failed:", e)
        return False
    


def DismissAnnoucement(page: Page) -> bool:
    try:
        button = page.get_by_role("button", name="Dismiss announcement")
        if button.is_visible(timeout=5000) and button.is_enabled():
            button.click()
            print("Announcement dismissed.")
            return True
    except:
        print("No announcement present.")
        return False


def SearchMyProjects(page: Page, searchValue: str, isViewOnSearchComplete: bool) -> Locator:
    try:
        page.wait_for_selector('text=My Projects', timeout=5000)

        searchTextBox = page.get_by_role("textbox", name="Keyword Search")
        searchTextBox.scroll_into_view_if_needed()
        searchTextBox.fill("")
        searchTextBox.fill(searchValue)

        searchBox = page.get_by_role("button", name="Search", exact=True)
        searchBox.click()

        searchTable = page.get_by_role("table", name="My Projects")
        searchTable.scroll_into_view_if_needed()
        
        projectRow = searchTable.locator("tbody tr")
        expect(projectRow).to_have_count(1, timeout=5000)

        projectName = projectRow.locator("td").nth(0).text_content().strip()
        print("Searched for", searchValue, "and", projectRow.count(), "result found as", projectName)

        if isViewOnSearchComplete:
            projectRow.get_by_role("button", name="View eCPRs", exact=True).click()

        return projectRow

    except Exception as e:
        print("Search failed:", e)
        return None