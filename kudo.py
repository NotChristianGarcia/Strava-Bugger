from getpass import getpass
from datetime import datetime
from selenium import webdriver


def main():
    date = datetime.today()
    curr_year = date[0]
    curr_month = date[1]
    athlete_num = 547181 #input("Athlete ID: ")
    driver = webdriver.Chrome()
    driver.get("https://www.strava.com/athletes/" + athelete_num +
               "#interval_type?chart_type=miles&interval_type=month" +
               "&interval=" + curr_year + curr_month + "&year_offset=0")


def get_init_iso():
    menu = driver.find_element_by_css_selector('.drop-down-menu.drop-down-sm.enabled')
    menu.click()
    options = menu.find_elements_by_tag_name('a')

    beg_date = options[-1:][0].text
    datetime.strptime(beg_date.split(' - ')[0], '%b %d, %Y')


def login():
    driver.get("https://www.strava.com/login")
    email_field = driver.find_element_by_xpath('//*[@id="email"]')
    password_field = driver.find_element_by_xpath('//*[@id="password"]')

    email = input("Email: ")
    password = getpass("Password: ")

    email_field.send_keys(email)
    password_field.send_keys(password)

    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    time.sleep(2)


def kudoer():
    time.sleep(2)
    athlete_rides = driver.find_elements_by_css_selector('.activity.entity-details.feed-entry')
    group_rides = driver.find_elements_by_css_selector('.list-entries')

    for ride in group_rides:
        athlete_rides.append(ride.find_element_by_css_selector('.entity-details.feed-entry'))

    for ride in athlete_rides:
        try:
            print(ride.find_element_by_css_selector('.btn.btn-default.btn-kudo.btn-xs.js-add-kudo'))
            #ride.find_element_by_css_selector('.btn.btn-default.btn-kudo.btn-xs.js-add-kudo').click()
        except:
            pass


if __name__ = "__main__":
    main()
