README

author- Benjamin Martinson
repo- https://github.com/bmartinson5/proj5-mongo/
email- bmartin5@uoregon.edu

Terminal Command to run:

$ docker-compose up

This command runs the app on port 5000



Brevet Control Time Calculator:

This project updates the previous by adding submit and display buttons to the bottom of the calc.html page.

When submit is clicked on, it checks to see if any race times have been entered into the form. If so,
those times are submitted to the mongo database, and calc.html gets rendered again as a blank page. 
If no times have been submitted, an error is produced in red text under the button. An error is also
displayed when one of the control time fields has a km distance that exceeds the race distance.

When the display button is clicked, it renders a new page that displays all the documents in the mongodb
collection. If no documents were previously submitted, an error is displayed instead.

The database collection is deleted whenever calc.html is rendered, with one EXCEPTION; it is not deleted 
after clicking display, and then clicking 'back' in the browser (at least not in chrome). This is my design 
choice, so that the user can add submissions to the database and see the intermediate changes by clicking
display, and then resume their submission insertions going back one page and filling out the form again.

Note: Didn't find time to fix the errors from project 4; seconds are not displayed for open and close times.
