
* ###### Django development server
The steps to execute the app using Django development server:

1. Move to project version

    ```bash
    $ cd /<path>/<to>/<proyect>/
    ```

2. Activate virtual environment

    ```bash
    $ source hon_stats/bin/activate
    ```

3. Execute migrations

    ```bash
    $ python3 manage.py migrate
    ```

4. Create super user for the application

    ```bash
    $ python3 manage.py createsuperuser
    ```

5. Run developemnt server

    ```bash
    $ python3 manage.py runserver 0.0.0.0:8000
    ```



* ###### Apache

Steps to execute the app with apache2:

1. Install Apache and wsgi module for apache

    ```bash
   $ sudo apt install apache2 libapache2-mod-wsgi-py3 supervisor
    ```

2. Test if system if running as expected following these [simple steps](#django-development-server).

3. Set apache to deploy CandyApp as default website of teh server.

    ```bash
   $ sudo cp conf/apache_example.conf /etc/apache2/conf-available/candyapp.conf
   $ sudo vi /etc/apache2/conf-available/candyapp.conf
    ```
4. Edit content of the file with the values of the specific URL or FQDN to use as instance servername, serveradmin, documentroot with the route of the project and the virtual environment used. In this example is used *vi* but can be used any other like *nano*. Once made the changes only need to disable old default site and enble the new one.

    ```bash
    $ sudo a2dissite 000-default.conf
    $ sudo a2ensite candyapp.conf
