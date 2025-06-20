from playwright.sync_api import Page, TimeoutError

def Login(page: Page, username: str, password: str) -> bool:
    try:
        page.get_by_role("link", name="Log in").click(timeout=5000)
        page.get_by_role("textbox", name="User name / Email").fill("")
        page.get_by_role("textbox", name="User name / Email").fill(username)
        page.get_by_role("textbox", name="Password").fill("")
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Log in").click()

        # Optional: wait for a known post-login element
        page.wait_for_selector('text=My Projects', timeout=5000)

        print("Login successful.")
        return True

    except TimeoutError:
        print("Login failed: timeout or element missing.")
        return False

    except Exception as e:
        print("Login failed:", e)
        return False
    


def DismissAnnoucement(page: Page):
    try:
        button = page.get_by_role("button", name="Dismiss announcement")
        if button.is_visible(timeout=5000) and button.is_enabled():
            button.click()
            print("Announcement dismissed.")
    except:
        print("No announcement present.")