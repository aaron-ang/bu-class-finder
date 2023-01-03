import os
import time
import asyncio
from typing import Dict, List
import telegram
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from course import Course
from client import mongo_client

BOT_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
ADMIN_ID = str(os.getenv("CHAT_ID"))
MONGO_URL = str(os.getenv("MONGO_URL"))

options = webdriver.ChromeOptions()
options.binary_location = str(os.getenv("GOOGLE_CHROME_BIN"))
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')


driver = webdriver.Chrome(executable_path=str(
    os.getenv("CHROMEDRIVER_PATH")), options=options)
wait = WebDriverWait(driver, timeout=30)

bot = telegram.Bot(token=BOT_TOKEN)
db = mongo_client["course_db"]
course_collection = db["courses"]

COURSE_MAP: Dict[Course, List[str]] = {}
COURSES_TO_REMOVE: List[Course] = []
RESULT_XPATH = ""

for course in course_collection.find():
    users = list(course["users"])
    # prune courses with no users
    if len(users) == 0:
        COURSES_TO_REMOVE.append(Course(course["name"]))
    else:
        COURSE_MAP[Course(course["name"])] = users


async def search_courses():
    for course in COURSE_MAP:
        driver.get(course.bin_url)
        try:
            # wait until elements are rendered
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/table[4]/tbody")))
            await search_course(course)
        except:
            break


async def search_course(course: Course):
    # check for pinned message
    if driver.find_elements(By.XPATH, "/html/body/table[4]/tbody/tr[2]/td[1]/font/table/tbody/tr/td[1]/img"):
        RESULT_XPATH = "/html/body/table[4]/tbody/tr[3]"
    else:
        RESULT_XPATH = "/html/body/table[4]/tbody/tr[2]"

    try:
        keywords = ["Class Full", "Class Closed"]
        num_seats = driver.find_element(
            By.XPATH, RESULT_XPATH + "/td[7]/font").text
        is_blocked = any([kw in driver.find_element(
            By.XPATH, RESULT_XPATH + "/td[13]/font").text for kw in keywords])
        is_avail = int(num_seats) > 0 and not is_blocked

        if is_avail:
            msg = f"{str(course)} is now available at {course.reg_url}"
            for uid in COURSE_MAP[course]:
                await bot.send_message(uid, msg)
            COURSES_TO_REMOVE.append(course)

    except Exception:
        return


async def main():
    # Scrape website every minute
    while True:
        await search_courses()

        for course in COURSES_TO_REMOVE:
            COURSE_MAP.pop(course)
            course_collection.delete_one({"name": str(course)})
        COURSES_TO_REMOVE.clear()

        time.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
