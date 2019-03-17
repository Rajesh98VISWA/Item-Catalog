## By : N N V Viswanadha Rajesh

# item-catalog

 > Item-Catalog Project , One of the project belongs to Udacity[FULL STACK WEB DEVELOPER : NANO_DEGREE]
https://github.com/Rajesh98VISWA/Item-Catalog.git
### ANALYSIS FOR Catalog Project -:

<h1 align="center">
  <a href="https://github.com/Rajesh98VISWA/Item-Catalog"><img src="https://www.mapsofindia.com/worldmap/map-of-world.jpg"
   alt="Item-Catalog-icon" width="500"></a>
  <br>

 -  A Reporting page that is helpful to display the individual state information Within item catalog 
 - Parent - Child information is given and modified 
 - It is modified using CRUD operation (Create, Update, Delete, Retrive)
 - Currently OAuth2 implemented for Google Accounts. OAuth2 provides authentication for CRUD operations. 

## Tools Used :

* Python3
* VirtualBox
* Vagrant
* Git
* DB Browser( SQL Cipher )
* Text Editor(Sublime text)

### Python files with project :

 - main file - `stateflask.py` 
 - Database file - `db_set.py`
 - State information file - `state_info.py` 

### TO RUN PYTHON FILES :

 - pip install Flask
 - pip install SQLalchemy
 - pip install requests
 - pip install psycopg2
 - pip install OAuth2client

### Softwares for Item-Catalog :

 - (python3) - It is a general-purpose interpreted, interactive, object-oriented, and high-level programming language.(IDLE PYTHON 3.7-32bit)

 - (Git-Bash) - Git is a distributed version-control system for tracking changes in source code.
 - (Virtual-Box) - Oracle VM VirtualBox is a free and open-source hosted hypervisor.
 - (Vagrant) - It is an open-source softwarw product for building and maintaining portable virtual software development environmeants.
 - (DB browser -[SQL Cipher]) - Unlike client–server database management systems, the SQLite engine has no standalone processes with which the application program communicates. 
 - (Any Editor) - Editor used to develop project is Sublime text.

### Links for Different Softwares :

** Python3 ** - [https://www.python.org/downloads/] 
** Git-Bash ** - [https://git-scm.com/downloads] 
** Virtual-Box ** - [https://www.virtualbox.org/wiki/Downloads] 
** Vagrant ** - [https://www.vagrantup.com/downloads.html] 
** DB browser ** - [https://sqlitebrowser.org/dl/] 
** Sublime text ** - [https://www.sublimetext.com/3]

#### brief on project

-> This project is written in python 
-> using database (can be anything either software based or written format )
-> major requirement is DB browser - SQL cipher and flask modules
-> JSON is used to for read the data given  user logins 
-> This project is developed in windows 10 os
-> using sublime text application
-> operation and server reloads and restarts are made in gitbash

### Process for login through Google

-> Open Browser and go to [console.developers.google.com](https://console.developers.google.com/)
-> Create a new project based on your UDACITY-PROJECT-NAME.
-> Then click on Credentials, to create a new credentials, and after that there wiil be a dialogue box showing.
-> Click on OAuth client ID, then you will see a option format for application type.
-> Select on `Web-application`, and then click on create button.
-> Fill the given columns with appropriate `HTTP` URL's.
-> After completion of columns with appropriate details
-> Download the `JSON` file, renamed it as `client_secrets.json`
-> After complition of this process. You will be allowed used within your project.

## JSON Key-Points 

** localhost:8000/country/JSON

** localhost:8000/country/<int:country_id>/main/<int:state_id>/JSON
	
** localhost:8000/country/<int:state_id>/main/JSON

