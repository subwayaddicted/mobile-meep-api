# mobile-meep-api
 Project for university with main target here to bring up API that will use meep package

### API setup for dev

 Install Anaconda
 
 Run the app
 ```
 // Creating new venv
 conda create -n mobile-meep-api -c conda-forge flask pymeep flask-restplus imageio
 // Clone this repo
 git clone ...
 // Export flask vars
 export FLASK_APP=mobile_meep_api.py
 export FLASK_ENV=development
 // Run the API
 flask run
```

Example json:
```
	{
	  "data": {
		"cell": {
		  "x": 16,
		  "y": 8,
		  "z": 0
		},
		"geometry": {
		  "coordinates": {
			"x": 20,
			"y": 1,
			"z": 0
		  },
		  "center": {
			"x": 0,
			"y": 0
		  },
		  "material": 12
		},
		"sources": {
		  "frequency": 0.15,
		  "center": {
			"x": -7,
			"y": 0
		  }
		},
		"simulation_time": {
		  "between": 0.6,
		  "until": 200
		},
		"pml_layers": 1.0,
		"resolution": 10
	  }
	}
```
