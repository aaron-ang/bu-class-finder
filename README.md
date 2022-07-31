# bu-class-finder

A Python Selenium script which scrapes BU's course portal for specific classes and sends a notification via Telegram bot when a class is open.

Deployed to Heroku.

## Existing issues
1. Heroku refreshes the dyno every day and I need to manually authenticate 2FA via Duo Mobile (security feature by BU) everytime this occurs
    - Need to determine if cookies passed during authentication is identical. If so, store the cookie and pass it into the Chrome Webdriver during login
