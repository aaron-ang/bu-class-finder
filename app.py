from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from course import Course
import telegram
import time
import os
import logging
from typing import List, Set

# USERNAME = os.getenv("BU_USERNAME")
# PASSWORD = os.getenv("BU_PASSWORD")
BOT_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
CHAT_IDS = str(os.getenv("CHAT_ID")).split(",")
AA_CHAT_ID = CHAT_IDS[0]
KB_CHAT_ID = CHAT_IDS[1]
JP_CHAT_ID = CHAT_IDS[2]
AF_CHAT_ID = CHAT_IDS[3]
GITHUB_URL = "https://github.com/aaron-ang/bu-class-finder"
AUTH_URL = "https://shib.bu.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2"
MAIN_REG_URL = "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=regsched.pl"
COURSES: Set[Course] = set()
COURSES_TO_REMOVE: List[Course] = []

COURSE_MAP = {
    "CAS CS 411 A1": [AF_CHAT_ID],
    "CAS EC 363 B1": [JP_CHAT_ID],
}

for c in COURSE_MAP:
    COURSES.add(Course(c))

options = webdriver.ChromeOptions()
options.binary_location = os.getenv("GOOGLE_CHROME_BIN")  # type: ignore
options.headless = True
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(executable_path=os.getenv(
    "CHROMEDRIVER_PATH"), options=options)  # type: ignore
bot = telegram.Bot(token=BOT_TOKEN)
wait = WebDriverWait(driver, timeout=30)
logger = logging.getLogger()


def search_courses():
    for course in COURSES:
        driver.get(course.reg_url)

        try:
            # wait until elements are rendered
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/table[4]/tbody/tr[2]/td[2]")))
            search_course(course)
        except:
            break


def search_course(course: Course):
    try:
        # TODO: check if course is not locked?
        course_open = int(driver.find_element(
            By.XPATH, "/html/body/table[4]/tbody/tr[2]/td[7]/font").text) > 0
    except Exception:
        return

    process_data(course, course_open)


def process_data(course: Course, course_is_open: bool):
    if course_is_open:
        msg = f"{str(course)} is now available at {course.reg_url}"
        for uid in COURSE_MAP[str(course)]:
            bot.send_message(uid, msg)
        COURSES_TO_REMOVE.append(course)


def main():
    # Scrape website every minute
    while len(COURSES) != 0:
        search_courses()
        time.sleep(60)

    driver.quit()


if __name__ == "__main__":
    main()
