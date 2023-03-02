# Footblal_outcomes
This repository uses the Selenium framework in order to scrap data from websites displaying football game scores. Given this data, forecasts outcomes according to a chosen method.

This repository contains several  python files. Some methods are not yet ready to use as Understat (website) does not provide data history. Every ready-to-use methods are tested in the test.py file.  	

league.py: creates a League class and contains the webdriver. 

club.py: creates a Club class

data.py: all of the class instances for the 2022/2023 season in football. 

main.py: calls methods from the Club or League class. 

test.py: uses Django to test different methods from the League and Club classes. 
