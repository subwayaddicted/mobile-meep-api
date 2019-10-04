# mobile-meep-api
 Project for university with main target here to bring up API that will use meep package

# API setup for dev

 Install Anaconda
 ```
 // Creating new venv
 conda create -n mobile-meep -c conda-forge flask pymeep
 // Clone this repo
 git clone ...
 // Export flask vars
 export FLASK_APP = mobile_meep_api.py
 export FLASK_ENV = development
 // Run the API
 flask run
```
