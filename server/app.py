from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from course import Course
import telegram
import time
import os
import logging
from typing import Tuple, Set

# USERNAME = os.getenv("BU_USERNAME")
# PASSWORD = os.getenv("BU_PASSWORD")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
# LOGIN_TITLE = "Boston University | Login"
# REGISTRATION_TITLE = "Add Classes - Display"
# REGISTRATION_CFM = "Add Classes - Confirmation"
GITHUB_URL = "https://github.com/aaron-ang/bu-class-finder"
AUTH_URL = "https://shib.bu.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2"
MAIN_REG_URL = "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=regsched.pl"
COURSES: Set[Tuple[Course, int]] = set()
COURSES_TO_REMOVE = []

COURSES.add((Course("cas", "ec", "323", "b1"), ADMIN_CHAT_ID))
COURSES.add((Course("cas", "ph", "266", "a1"), ADMIN_CHAT_ID))

options = webdriver.ChromeOptions()
options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
options.add_argument('--no-sandbox')
options.headless = True
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])

service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome(service=service, options=options)
bot = telegram.Bot(token=BOT_TOKEN)
wait = WebDriverWait(driver, timeout=30)
logger = logging.getLogger()


# def login_user():
#     username_box = driver.find_element(By.ID, "j_username")
#     password_box = driver.find_element(By.ID, "j_password")
#     login_button = driver.find_element(By.NAME, "_eventId_proceed")

#     username_box.send_keys(USERNAME)
#     password_box.send_keys(PASSWORD)
#     login_button.click()

#     # Wait for manual authentication to pass
#     try:
#         wait.until(lambda driver: driver.title != LOGIN_TITLE)
#     except Exception:
#         bot.send_message(
#             ADMIN_CHAT_ID, "2FA failed, bot will try again in 1 min...")
#         return False

#     return True


def search_courses():
    for course_info in COURSES:
        course, _ = course_info
        # course refers to a Course object
        driver.get(course.reg_url)

        try:
            wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[3]/a"), str(course)))
            search_course(course_info)
        except:
            break


def search_course(course_info: Tuple[Course, int]):
    try:
        course_icon = driver.find_element(
            By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[1]")
        course_name = driver.find_element(
            By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[3]/a").text
        # /html/body/table[4]/tbody/tr[3]/td[7]/font if message exists
        # /html/body/table[4]/tbody/tr[2]/td[7]/font if message does not exist
        course_open = course_icon.find_elements(
            By.NAME, "SelectIt") != []  # input checkbox exists
    except Exception:
        return

    process_data(course_info, course_name, course_open)


def process_data(course_info, course_name, course_is_open):
    course, chat_id = course_info
    if course_name != course.__str__():
        msg = f"{course} does not exist or is not specific. Did you mean {course_name}?"
        bot.send_message(chat_id, msg)
        COURSES_TO_REMOVE.append(course_info)

    elif course_is_open:
        msg = f"{course_name} is now available at {course.reg_url}"
        # bot.send_message(chat_id, msg)
        # sync_reg_options()
        # register_course(course_name, chat_id)
        COURSES_TO_REMOVE.append(course_info)


# def sync_reg_options():
#     driver.find_element(
#         By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/a").click()
#     wait.until(EC.title_is, "Registration Options")
#     driver.execute_script("window.history.go(-1)")


# def register_course(course_name, chat_id):
#     input = driver.find_element(
#         By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[1]/input")
#     add_class_btn = driver.find_element(
#         By.XPATH, "/html/body/form/center[2]/table/tbody/tr/td[1]/input")

#     input.click()
#     add_class_btn.click()
#     alert = wait.until(EC.alert_is_present())
#     alert.accept()

#     msg_success = f"{course_name} successfully registered!"
#     msg_fail = f"Could not register {course_name} :("

#     try:
#         wait.until(EC.title_is(REGISTRATION_CFM))
#         cfm_img = driver.find_element(
#             By.XPATH, "/html/body/table[4]/tbody/tr[2]/td[1]/img")
#         if "checkmark" in cfm_img.get_attribute("src"):
#             bot.send_message(chat_id, msg_success)
#         else:
#             bot.send_message(chat_id, msg_fail)
#     except Exception:
#         bot.send_message(chat_id, msg_fail)


def start(update, context):
    msg = (f"Welcome to BU Course Availability Bot! Check out the code at {GITHUB_URL}")
    update.message.reply_text(msg)


# def current_courses(update, context):
#     if len(COURSES) == 0:
#         update.message.reply_text("No courses are being searched")
#         return

#     msg = "Bot is currently searching for:"
#     for course in COURSES:
#         msg += f"\n{course}"
#     update.message.reply_text(msg)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # updater = Updater(BOT_TOKEN, use_context=True)
    # dp = updater.dispatcher
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("courses", current_courses))
    # dp.add_error_handler(error)
    # updater.start_polling()
    # updater.idle()

    # Scrape website every minute
    while len(COURSES) != 0:
        search_courses()

        # # Keep driver in this loop until 2FA succeeds
        # while driver.current_url == AUTH_URL:
        #     time.sleep(60)
        #     driver.get(MAIN_REG_URL)
        #     try:
        #         wait.until(lambda driver: driver.title != LOGIN_TITLE)
        #     except Exception:
        #         # 2FA failed, restart loop
        #         continue

        while len(COURSES_TO_REMOVE) != 0:
            COURSES.remove(COURSES_TO_REMOVE.pop())

        time.sleep(60)

   # If COURSES is empty, quit webdriver and send message via Tele Bot
    driver.quit()


if __name__ == "__main__":
    main()
