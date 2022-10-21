# Linked In Scrapper

<h2>Step 1:</h2>

<p><h3>Install the Django:</h3></p>

<h2>Step 2:</h2>

<p><h3>Install Selenium</h3></p>

<h5>pip install selenium==4.2.0 --force-reinstall</h5>

<h2>Step 3:</h2>

<p>clone the project using git and open project in terminal.</p>

<h2>Step 4:</h2>

<p>Change your email id and password in the </p>

1. "linkedin/bot/messages.py" -> Line 244 and 250
2. "linkedin/bot/profile.py" -> Line 114 and 119

<h2>Step 5:</h2>

<p><h3>Run the following command:</h3></p>

python manage.py runmigrations

python manage.py migrate

<h2>Step 6:</h2>

<p>Change page no according to your requirement in the file "profile.py" in the Line 74 and 76.</p>

<h2>Step 7:</h2>

<p>Change the limit of sending messages and profile visit in "messages.py" Line - 188</p>

<p>Note:- </p>
1. Limit of the profile visit must be less than 80.
2. Limit of the send message must be less than 40.

<h2>Step 8:</h2>
<p><h3>Run the server.</h3></p>

python manage.py runserver

<h2>Step 9:</h2>

<p>1 for Scrap the Linked In profile and 2 for the send message</p>

<h2>Step 10:</h2>

<p>Happy</p>