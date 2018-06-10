import json
import requests
from lxml import html
from bs4 import BeautifulSoup
from utilities import util

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as session_requests:
    # First need to make a call to get the CSRF token
    base_url = "https://www.sugarwod.com/login"
    token = util.get_csrf_token(base_url, session_requests)

    # Fill in your details here to be posted to the login form.
    payload = {
        "username": "timcoyle.purchases@gmail.com",
        "password": "cet5583#4",
        "_csrf": token,
        "_method": "post"
    }

    login_url = 'https://www.sugarwod.com/public/api/v1/login'
    session_requests.post(
        login_url,
        data=payload,
        headers=dict(referer=base_url))

    # An authorised request.
    ath_url = "https://www.sugarwod.com/athletes/me"
    ath = session_requests.get(
        ath_url,
        headers=dict(referer=base_url)
    )

    tree = html.fromstring(ath.text)
    # Set up the variables to query the logbook
    ath_id = util.get_ath_id(tree)
    # joined = util.get_joined_date(tree)

    start_date = "20180527"
    end_date = "20180701"

    # Set up the query to the calendar page
    cal_url = "https://www.sugarwod.com/api/athletes/<ath_id>/results?fromDate=<begin>&toDate=<end>&_csrf=<token>"
    cal_url = cal_url.replace("<ath_id>", ath_id)
    cal_url = cal_url.replace("<begin>", start_date)
    cal_url = cal_url.replace("<end>", end_date)
    cal_url = cal_url.replace("<token>", token)

    logbook = session_requests.get(
        cal_url,
        headers=dict(referer=ath_url)
    )

    # Read the data result out of the HTML <p> tag
    soup = BeautifulSoup(logbook.text, "lmxl")
    for p in soup.find_all('p'):
        log = json.loads(p.text)
        data = log['data']
        for workout in data:
            # Here is a distinct workout logged.  This could be more than one on the same day, so check the createdAt
            for k, v in workout.items():
                print("Key {} - Value {}".format(k, v))
            print()

    bar_bell_pr = "https://www.sugarwod.com/api/results/athletes/<ath_id>/barbellprs?_csrf=<token>"
    bar_bell_pr = bar_bell_pr.replace("<ath_id>", ath_id)
    bar_bell_pr = bar_bell_pr.replace("<token>", token)

    barbell = session_requests.get(
        bar_bell_pr,
        headers=dict(referer=ath_url)
    )

    # Read the data result out of the HTML <p> tag
    soup = BeautifulSoup(barbell.text)
    for p in soup.find_all('p'):
        log = json.loads(p.text)
        data = log['data']
        for movement in data:
            # Here is a distinct workout logged.  This could be more than one on the same day, so check the createdAt
            for k, v in movement.items():
                print("Key {} - Value {}".format(k, v))
            print()
