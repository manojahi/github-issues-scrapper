#Importing all the necessary packages

from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

"""
To fetch the number of issues, i am using BeautifulSoup to scrap the webpage data and processing according to the need
"""

def fetch_total_issues(url):
    """
    input param: url - Github repository link
    output param: Number of total issues
    
    Passing github repo url and adding github suffix url to get on issues page

    Fetch issues values based on issue frontend CSS class using select_one beautifulSoup method.
    """
    issue_url = url+"/issues?q=is%3Aopen+is%3Aissue"    
    issue_raw  = requests.get(issue_url)

    iss_data = issue_raw.text
    iss_soup = BeautifulSoup(iss_data, 'html.parser')
    issue_data = iss_soup.select_one(".table-list-header-toggle a")

    open_issues = issue_data.get_text()
    return open_issues.strip().split()[0]


def fetch_period_issues(url, timeframe):
    """
    input param: url - Github repository url
                 timeframe - daily/weekly/monthly (these are the github query params to fetch the insights values)
    output param: Number of open issue in certain timeframe

    Scrapping the values based on CSS classes
    """
    insights_url = url+"/pulse/"+timeframe
    ins_raw = requests.get(insights_url)

    ins_data = ins_raw.text
    ins_soup = BeautifulSoup(ins_data, 'html.parser')
    insights_data = ins_soup.select(".summary-stats li")[3]

    open_issues = insights_data.get_text()
    return open_issues.strip().split()[0]


def fetch_period_7_issues(url, timeframe):
    """
    input param: url - Github repository url
                 timeframe - daily/weekly/monthly (these are the github query params to fetch the insights values)
    output param: Number of open issue in certain timeframe

    Scrapping the values based on CSS classes
    """
    insights_url = url+"/pulse/"+timeframe
    ins_raw = requests.get(insights_url)

    ins_data = ins_raw.text
    ins_soup = BeautifulSoup(ins_data, 'html.parser')
    insights_data = ins_soup.select(".simple-conversation-list")[3]

    open_issue_list = insights_data.select("li relative-time")

    return open_issue_list

