from playwright.sync_api import sync_playwright


def test_create_ticket():

    with sync_playwright() as p:

        #Launches a Chromium browser
        browser = p.chromium.launch(
            headless=False
        )

        #Create a New Browser Tab
        page = browser.new_page()

        #Navigate to the Help Desk Application
        page.goto("http://localhost:5173")

        page.click("text=New Ticket")

        assert page.locator("h2").is_visible()

        #Close Browser
        browser.close()


def test_fill_ticket_form():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("http://localhost:5173")

        page.click("text=New Ticket")

        page.fill("#ticket-title", "VPN Issue")

        page.fill(
            "#ticket-description",
            "Cannot connect to VPN"
        )

        page.select_option(
            "#ticket-category",
            "network"
        )

        assert page.locator(
            "#ticket-title"
        ).input_value() == "VPN Issue"

        browser.close()


def test_submit_ticket():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("http://localhost:5173")

        page.click("text=New Ticket")

        page.fill("#ticket-title", "VPN Issue")

        page.fill(
            "#ticket-description",
            "Cannot connect to VPN"
        )

        page.select_option(
            "#ticket-category",
            "network"
        )

        page.click(
            "button[type='submit']"
        )

        page.wait_for_timeout(2000)

        browser.close()


def test_ticket_created():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        page.goto("http://localhost:5173")

        page.click("text=New Ticket")

        page.fill(
            "#ticket-title",
            "VPN Issue"
        )

        page.fill(
            "#ticket-description",
            "Cannot connect to VPN"
        )

        page.select_option(
            "#ticket-category",
            "network"
        )

        page.click(
            "button[type='submit']"
        )

        page.click("text=Tickets")

        assert page.get_by_role(
            "cell",
            name="VPN Issue",
            exact=True
        ).first.is_visible()

        browser.close()