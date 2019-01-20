"""
Author: Christian R. Garcia
Uses Selenium to go through a Strava athlete's complete history of activities in Chrome.
Goes month by month and gives a kudo to all athlete activities. If the athlete
participated in a group event then only the specified athlete will receive a kudo, not
all activities on the page.

Note: Strava will soft-ban your from kudo at around 200 kudos. Random wait times are in
place to fight against that.
"""
import time
import random
from getpass import getpass
from datetime import datetime
from selenium import webdriver


def main():
    athlete_num = input("Athlete ID: ")

    driver = strava_init()
    beg_year, beg_month = get_init_cond(driver, athlete_num)
    iterate_months(driver, athlete_num, beg_year, beg_month)

def strava_init():
    email = input("Email: ")
    password = getpass("Password: ")

    driver = webdriver.Chrome()
    driver.get("https://www.strava.com/login")
    email_field = driver.find_element_by_xpath('//*[@id="email"]')
    password_field = driver.find_element_by_xpath('//*[@id="password"]')
    
    email_field.send_keys(email)
    password_field.send_keys(password)

    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    time.sleep(2)
    return driver


def get_init_cond(driver, athlete_num):
    driver.get('https://www.strava.com/athletes/' + athlete_num)
    menu = driver.find_element_by_css_selector('.drop-down-menu.drop-down-sm.enabled')
    menu.click()
    options = menu.find_elements_by_tag_name('a')

    beg_string = options[-1:][0].text.split(' - ')[0]
    beg_month = beg_string[:3]
    beg_month = int(time.strptime(beg_month, '%b').tm_mon)
    beg_year = int(beg_string[-4:])
    return beg_year, beg_month


def iterate_months(driver, athlete_num, beg_year, beg_month):
    year = beg_year
    month = beg_month
    
    date = datetime.today()
    curr_year = date.year
    curr_month = date.month
    
    while year <= curr_year:
        offset = curr_year - year - 1
        if year == curr_year:
            while month <= curr_month:
                driver.get('https://www.strava.com/athletes/' + athlete_num +
                           '#interval_type?chart_type=miles&interval_type=month' +
                           '&interval=' + str(year) + "{0:0=2d}".format(month) + 
                           '&year_offset=' + str(offset))
                print("Year: " + str(year) + " Month: " + str(month))
                kudoer(driver)
                month += 1
        
        else:
            while month <= 12:
                driver.get('https://www.strava.com/athletes/' + athlete_num +
                           '#interval_type?chart_type=miles&interval_type=month' +
                           '&interval=' + str(year) + "{0:0=2d}".format(month) + 
                           '&year_offset=' + str(offset))
                print("Year: " + str(year) + " Month: " + str(month))
                kudoer(driver)
                month += 1
        month = 1
        year += 1


def kudoer(driver):
    time.sleep(3)
    athlete_rides = driver.find_elements_by_css_selector('.activity.entity-details.feed-entry')
    group_rides = driver.find_elements_by_css_selector('.list-entries')

    for ride in group_rides:
        athlete_rides.append(ride.find_element_by_css_selector('.entity-details.feed-entry'))

    for ride in athlete_rides:
        try:
            #print(ride.find_element_by_css_selector('.btn.btn-default.btn-kudo.btn-xs.js-add-kudo'))
            ride.find_element_by_css_selector('.btn.btn-default.btn-kudo.btn-xs.js-add-kudo').click()
            print("Kudoed")
            time.sleep(int(random.uniform(3, 6)))
        except:
            pass


if __name__ == "__main__":
    main()
