import random

from playwright.sync_api import sync_playwright

from constants import BASE_HOST_URL, EMAIL, PASSWORD


def _wait(page):
    time = random.randint(1000, 2500)  # Randomly select between 1 second to 2.5 seconds
    page.wait_for_timeout(time)


def switch_to_most_recent_page(browser):
    return browser.context.pages[-1]


def visit_host_page(host_id, page, message):
    url = BASE_HOST_URL.format(host_id=host_id)
    page.goto(url, timeout=0)
    page.wait_for_selector('.l1d1x245')
    properties = page.query_selector_all('.l1d1x245')  # select <a> tag of properties
    with page.context.expect_page() as property_page:
        properties[0].click()

    _wait(page)
    page = property_page.value
    page.wait_for_selector('._1dj2p4gk')
    host_contact = page.query_selector('._1dj2p4gk')  # Get <a> tag for contact button
    host_contact.click()
    _wait(page)
    # try login else use exsisting session
    try:
        page.wait_for_selector('._1x0diny1')  # wait for login dialog
        page.query_selector_all('._snbhip0')[-1].click()  # Click on continue with email
        page.wait_for_selector('._c5rhl5')  # wait for email element to be available
        page.fill('._c5rhl5', EMAIL)  # fill email
        page.click('._6hkhatt')  # Click continue
        page.wait_for_selector('._c5rhl5')  # wait for password element to be available
        page.fill('._c5rhl5', PASSWORD)  # fill password
        page.click('._6hkhatt')  # click continue
        _wait(page)
    except Exception as e:
        print('Session already found.')

    # send message
    page.wait_for_selector('#contactHostMessage')
    page.fill('#contactHostMessage', message)
    _wait(page)
    page.click('._16l1qv1')  # click check in and check out date
    page.fill('#checkIn-book_it', '9/13/2022')  # fill check in date
    page.keyboard.press('Enter')
    page.click('._13ah4vr') # click on calendar element
    page.keyboard.press('ArrowRight')
    page.keyboard.press('Enter')
    # page.fill('#checkOut-book_it', '9/14/2022')  # fill check out date
    # page.wait_for_selector('._1lerwp6l') # wait for save button
    # page.click('._1lerwp6l') # click save button
    _wait(page)
    # page.click('.with-new-header')
    page.click('._1dj2p4gk')  # click on send message

    page.wait_for_timeout(10000)


def run(hosts_ids, message):
    with sync_playwright() as p:
        user_data_dir = '/Users/haseeb/PycharmProjects/AirbnbBot/user_data'
        browser = p.chromium.launch_persistent_context(user_data_dir, headless=False)
        page = browser.new_page()
        for host_id in hosts_ids:
            visit_host_page(host_id, page, message)

        browser.close()


if __name__ == '__main__':
    pass
    # hosts_ids = [
    #     3807501,
    # ]
    # run(hosts_ids)
