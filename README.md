# List of doctors from the CSIOZ database

#### Description
This is my first web application written in python using the django framework.

The application displays a list of doctors. At the end of the list there is a button to load more doctors to the list.
After clicking on the doctor, he goes to the subpage with his detailed data.

The list of doctors can be modified in the django admin panel. The available models in django admin are:
- associates - modifying the list of partners
- addresses - modifying the list of addresses
- settings - modifying application settings:
-- off_set - the value next to this option indicates the number of downloaded doctors (50 by default)
- uploadFiles - upload of wspolnicy.csv files and adresy_swiadczen.csv generated from the website  https://rpwdl.ezdrowie.gov.pl/Registry/DownloadRegistries (selected options: Rodzaj działalności: praktyki lekarskie; Rozszerzenie: CSV; Zakres ksiąg w pliku: wyłącznie aktywne księgi )
-- uploading the file wspolnicy.csv results INSERT or UPDATE on the associates model
-- uploading the file adresy_swiadczen.csv results INSERT on an empty model addresses (starts by removing everything from addresses model)

### Build and run
All you need to run the application is a docker and a web browser.

```sh
$ git clone https://github.com/JaroslawSlabik/associate-base-csioz.git
$ cd associate-base-csioz
$ ./build.bash # Build docker image based on Dockerfile. On Windows not working, please make bat 
$ ./run.bash # Run docker image, run serwvr, run database forward ports. On Windows not working, please make bat
```

Fill the login, e-mail, password and repeat the password.

When you see the message:
```sh
System check identified no issues (0 silenced).
December 04, 2020 - 20:01:22
Django version 1.8, using settings 'first_project.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```
This means the application is working.

To open the application in a web browser, go to the address at http://127.0.0.1:8111/


### Technologies used:
- Python 3.3
- django 1.8
- jQuery 3.5
- PostgreSQL x.x.x
- HTML 5
- CSS 3

