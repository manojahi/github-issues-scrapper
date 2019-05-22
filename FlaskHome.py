#Importing required packages 

from flask import Flask, request, render_template
from scrapper import fetch_total_issues, fetch_period_issues, fetch_period_7_issues
import time
from datetime import datetime

application = Flask(__name__)
application.config["DEBUG"] = True

@application.route("/", methods=["POST", "GET"])
def index():
    """
    This app is created using Flask.

    On loading of the app, index method will get called.
    In templates/index.html - form code is present which will render basic form to
    enter github repository url and a button to fetch issues from that repository.

    On click of Find issues below If will get trigger and will fetch all the values accordingly.

    All the method calls below are inside Try/Except to avoid the invalid url/response from the github.

    Link entered by user should contain https://
    """
    if request.method == "POST":
        url = request.form["link"]
        try:    
            number_of_total_issues = fetch_total_issues(url) #Method to fetch number of total issues
        except:
            number_of_total_issues = 0

        try:
            number_of_daily_issues = fetch_period_issues(url, "daily") #Method to fetch number of issues in 24 hours
        except:
            number_of_daily_issues = 0

        try:    
            number_of_weekly_issues = fetch_period_issues(url, "") 
        except:
            number_of_weekly_issues = 0

        try:
            last_7_days = fetch_period_7_issues(url, "") #Method to fetch number of issues in last 7 days
            issue_in_7_count = 0
            for one in last_7_days: #last_7_days is a list of all the issues created date
                newdate1 = datetime.strptime(one.text, "%b %d, %Y") #converting string date to datetime for subtracting
                newdate2 = datetime.now() #getting current time

                difference = newdate2 - newdate1 #finding difference between dates
                #print(difference.days)

                if difference.days > 0 and difference.days < 7: #if issue date is after 24 hours and less than 7 days, increase the issue counter
                    issue_in_7_count = issue_in_7_count + 1
        except:
            issue_in_7_count = 0

        try:
            #To get issues created more than 7 days, subtracting total issues with the last 7 days issues
            number_of_more_issues = int(number_of_total_issues.replace(',','')) - int(number_of_weekly_issues.replace(',','')) 
        except:
            number_of_more_issues = 0

        #return all the data to html file to populate the results
        return render_template('index.html', total_issues=number_of_total_issues,
                               last_24_hours=number_of_daily_issues,
                               in_24_and_7=str(issue_in_7_count),
                               more_than_7=str(number_of_more_issues),
                               url = url)
    else:
        return render_template('index.html', total_issues="",
                               last_24_hours="",
                               in_24_and_7="",
                               more_than_7="",
                               url = "")

if __name__ == "__main__":
    application.run()
