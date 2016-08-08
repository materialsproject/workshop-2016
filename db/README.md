# Preliminaries

Before you start, make sure you have the latest pymatgen-db and flamyngo.

```shell
pip install -r requirements.txt --upgrade
```

# Building your own DB.

1. Signup for an account at https://mlab.com.
2. Create a free database (single-node, sandbox will do). For the database name, use "mpworkshop2016" to make it easier.
3. Click on your created database. Add a database user. Use "mpworkshop2016", and "Hu!kSma5h" for the username and password.
4. Write down your db host address and port. This comes from the connecting instructions, and should be the form "ds145245.mlab.com:45245". In this case, "ds145245.mlab.com" is the host and 45245 is the port number.
5. Type
```bash
mgdb init
```
and setup your credentials.
6. Insert the calculations using
```shell
mgdb insert -c db.json CuAu
```

# Using flamyngo

1. Update your credentials in example.yaml.
2. Explore using
```shell
flm -c example.yaml
```
3. Open a browser and go to http://0.0.0.0:5000. Type "Cu", "Au" or CuAu" in the search bar.
4. Click on task ids to go to a document view.