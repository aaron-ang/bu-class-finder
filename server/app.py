from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from course import Course
import telegram
from telegram.ext import Updater, CommandHandler
import time
import os
import logging

USERNAME = os.getenv("BU_USERNAME")
PASSWORD = os.getenv("BU_PASSWORD")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("CHAT_ID")
LOGIN_TITLE = "Boston University | Login"
REGISTRATION_TITLE = "Add Classes - Display"
REGISTRATION_CFM = "Add Classes - Confirmation"
GITHUB_URL = "https://github.com/aaron-ang/bu-class-notif"
AUTH_URL = "https://shib.bu.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2"
MAIN_REG_URL = "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=regsched.pl"
COURSES = set()
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


def login_user():
    username_box = driver.find_element(By.ID, "j_username")
    password_box = driver.find_element(By.ID, "j_password")
    login_button = driver.find_element(By.NAME, "_eventId_proceed")

    username_box.send_keys(USERNAME)
    password_box.send_keys(PASSWORD)
    login_button.click()

    # Wait for manual authentication to pass
    try:
        wait.until(lambda driver: driver.title != LOGIN_TITLE)
    except Exception:
        bot.send_message(
            ADMIN_CHAT_ID, "2FA failed, bot will try again in 1 min...")
        return False

    return True


def search_courses():
    for course_info in COURSES:
        course, chat_id = course_info
        # course refers to a Course object
        driver.get(course.reg_url)

        if driver.title == LOGIN_TITLE:
            if not login_user():
                return

        try:
            wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[3]/a"), str(course)))
            search_course(course_info)
        except:
            break


def search_course(course_info):
    try:
        course_icon = driver.find_element(
            By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[1]")
        course_name = driver.find_element(
            By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[3]/a").text
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
        sync_reg_options()
        register_course(course_name, chat_id)
        COURSES_TO_REMOVE.append(course_info)


def sync_reg_options():
    driver.find_element(
        By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/a").click()
    wait.until(EC.title_is, "Registration Options")
    driver.execute_script("window.history.go(-1)")


def register_course(course_name, chat_id):
    input = driver.find_element(
        By.XPATH, "/html/body/form/table[1]/tbody/tr[2]/td[1]/input")
    add_class_btn = driver.find_element(
        By.XPATH, "/html/body/form/center[2]/table/tbody/tr/td[1]/input")

    input.click()
    add_class_btn.click()
    alert = wait.until(EC.alert_is_present())
    alert.accept()

    msg_success = f"{course_name} successfully registered!"
    msg_fail = f"Could not register {course_name} :("

    try:
        wait.until(EC.title_is(REGISTRATION_CFM))
        cfm_img = driver.find_element(
            By.XPATH, "/html/body/table[4]/tbody/tr[2]/td[1]/img")
        if "checkmark" in cfm_img.get_attribute("src"):
            bot.send_message(chat_id, msg_success)
        else:
            bot.send_message(chat_id, msg_fail)
    except Exception:
        bot.send_message(chat_id, msg_fail)


def quit_driver():
    msg = "Webdriver has quit, please restart application."
    bot.send_message(ADMIN_CHAT_ID, msg)
    driver.quit()


def start(update, context):
    msg = ("Welcome to BU Course Availability Bot! While the bot will ask for your BU credentials for 2FA,"
           f"it does not store them or use them for other purposes. Check out the code at {GITHUB_URL}")
    update.message.reply_text(msg)


def search(update, context):
    # TODO store user credentials and input and create corresponding Course object
    return


def add_course(update, context):
    # TODO store user input and create Course object
    return


def current_courses(update, context):
    if len(COURSES) == 0:
        update.message.reply_text("No courses are being searched")
        return

    msg = "Bot is currently searching for:"
    for course in COURSES:
        msg += f"\n{course}"
    update.message.reply_text(msg)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # updater = Updater(BOT_TOKEN, use_context=True)
    # dp = updater.dispatcher
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("search", search))
    # dp.add_handler(CommandHandler("add", add_course))
    # dp.add_handler(CommandHandler("courses", current_courses))
    # dp.add_error_handler(error)
    # updater.start_polling()
    # updater.idle()

    # Scrape website every minute
    while len(COURSES) != 0:
        search_courses()

        # Keep driver in this loop until 2FA succeeds
        while driver.current_url == AUTH_URL:
            time.sleep(60)
            driver.get(MAIN_REG_URL)
            try:
                wait.until(lambda driver: driver.title != LOGIN_TITLE)
            except Exception:
                # 2FA failed, restart loop
                continue

        while len(COURSES_TO_REMOVE) != 0:
            COURSES.remove(COURSES_TO_REMOVE.pop())

        time.sleep(60)

   # If COURSES is empty, quit webdriver and send message via Tele Bot
    quit_driver()


if __name__ == "__main__":
    main()
