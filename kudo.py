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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

def main():
    athlete_list = input("Athlete ID(s): ").split()
    start_inp = input("Start time ('2016 6'): ")
    end_inp = input("End time ('2019 4'): ")
    
    driver = strava_init() 
    for athlete_num in athlete_list:
        print(f'\nWorking on athlete number: {athlete_num}')
        start_cond, end_cond = get_param(driver, athlete_num, start_inp, end_inp)
        iterate_months(driver, athlete_num, start_cond, end_cond)
        print('\n')

def strava_init():
    #email = input("Email: ")
    #password = getpass("Password: ")
    
    email = 'christian.g21@gmail.com'
    password = 'H//u6)Gu2z>je2r47P283mCJ6Pf:N7y'

    driver = webdriver.Chrome()
    driver.get("https://www.strava.com/login")
    email_field = driver.find_element_by_xpath('//*[@id="email"]')
    password_field = driver.find_element_by_xpath('//*[@id="password"]')
    
    email_field.send_keys(email)
    password_field.send_keys(password)

    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    time.sleep(2)
    return driver


def get_param(driver, athlete_num, start_inp, end_inp):
    driver.get('https://www.strava.com/athletes/' + athlete_num)
    menu = driver.find_element_by_css_selector('.drop-down-menu.drop-down-sm.enabled')
    menu.click()
    options = menu.find_elements_by_tag_name('a')

    # Getting starting point
    start_string = options[-1:][0].text.split(' - ')[0]
    start_month = start_string[:3]
    start_month = int(time.strptime(start_month, '%b').tm_mon)
    start_year = int(start_string[-4:])

    if start_inp:
        inp_starty, inp_startm = map(int, start_inp.split())
        if not ((inp_starty < start_year) or (inp_starty == start_year and inp_startm < start_month)):
            start_month = inp_startm
        if inp_starty > start_year:
            start_year = inp_starty
    start_cond = [start_year, start_month]
   
    # Getting ending point
    date = datetime.today()
    end_year = date.year
    end_month = date.month
    
    if end_inp:
        inp_endy, inp_endm = map(int, end_inp.split())
        if not ((inp_endy > end_year) or (inp_endy == end_year and inp_endm > end_month)):
            end_month = inp_endm
        if inp_endy < end_year:
            end_year = inp_endy
    end_cond = [end_year, end_month]

    # Checks that end > start
    if start_cond[0] > end_cond[0]:
        driver.quit()
        raise ValueError(f'Start year postdates end year: {start_cond[0]} > {end_cond[0]}')
    elif start_cond[0] == end_cond[0] and start_cond[1] > end_cond[1]:
        driver.quit()
        raise ValueError(f'Start month postdates end month: {start_cond[1]} > {end_cond[1]}')
    
    return start_cond, end_cond


def iterate_months(driver, athlete_num, start_cond, end_cond):
    year = start_cond[0]
    month = start_cond[1]
    end_year = end_cond[0]
    end_month = end_cond[1]

    while year <= end_year:
        offset = end_year - year - 1
        if year == end_year:
            loop_end_month = end_month
        else:
            loop_end_month = 12

        while month <= loop_end_month:
            print(f"Year: {year} Month: {month}")
            driver.get('https://www.strava.com/athletes/' + athlete_num +
                       '#interval_type?chart_type=miles&interval_type=month' +
                       '&interval=' + str(year) + "{0:0=2d}".format(month) + 
                       '&year_offset=' + str(offset))
            time.sleep(random.uniform(2.5, 5))
            wait_for_ajax(driver)
            kudoer(driver)
            month += 1
        time.sleep(random.uniform(2.5, 5))
        month = 1
        year += 1


def kudoer(driver):
    kudoable_items = []
    solo_rides = driver.find_elements_by_css_selector('.activity.entity-details.feed-entry')
    group_rides = driver.find_elements_by_css_selector('.list-entries')
    challenges = driver.find_elements_by_css_selector('.challenge.feed-entry')

    if True:
        for ride in solo_rides:
            kudoable_items.append(ride)
    if True:
        for ride in group_rides:
            kudoable_items.append(ride.find_element_by_css_selector('.entity-details.feed-entry'))
    if True:
        for challenge in challenges:
            kudoable_items.append(challenge)

    for item in kudoable_items:
        try:
            item.find_element_by_css_selector('.btn.btn-default.btn-kudo.btn-xs.js-add-kudo').click()
            print("✓", end='', flush=True)
            time.sleep(random.uniform(2.5, 5))
        except NoSuchElementException:
            print(".", end='', flush=True)
    
    if kudoable_items:
        print('')


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass


if __name__ == "__main__":
    main()
    print('\nSleeping')
    time.sleep(60)
