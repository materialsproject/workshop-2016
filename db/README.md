# Preliminaries

Before you start, make sure you have the latest pymatgen-db and flamyngo.

```shell
pip install -r requirements.txt --upgrade
```

# Building your own DB.

* Signup for an account at MongoLab (https://mlab.com).
* Create a free database (single-node, sandbox will do). For the database name, use "mpworkshop2016" to make it easier.
* Click on your created database. Add a database user. Use "mpworkshop2016", and "Hu!kSma5h" for the username and password.
* Write down your db host address and port. This comes from the connecting instructions, and should be the form "ds145245.mlab.com:45245". In this case, "ds145245.mlab.com" is the host and 45245 is the port number.
* Type
```shell
mgdb init
```
and setup your credentials. Use the same username and password for both admin and readonly for now.

* Insert the calculations using
```shell
mgdb insert -c db.json CuAu
```
* Do a test with the following:
```shell
mgdb query -c db.json --crit '{"pretty_formula": "CuAu"}' --props task_id energy_per_atom
```

# Using flamyngo

* Update your credentials in example.yaml based on your MongoLab settings.
* From a terminal, run
```shell
flm -c example.yaml
```
* The above will run a web server to the database. Open a browser and go to http://0.0.0.0:5000. 
* Type "Cu", "Au" or CuAu" in the search bar.
* Click on task ids to go to a document view.
* Mess around with the example.yaml and restart the web server (Ctrl-C and run command again) to see if you can get desired fields to appear for your own needs.