Django with Postgres, Nginx, and Gunicorn on Ubuntu 16.04 

1)Install the Packages from the Ubuntu Repositories

		type:

	    sudo apt-get update
	    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

2)Create the PostgreSQL Database and User

	Log into an interactive Postgres session

		    sudo -u postgres psql

	Create a database for project

	    CREATE DATABASE country;

	Create a database user, password

	    CREATE USER dbadmin WITH PASSWORD 'pAsToDb23';

	Set the default encoding to UTF-8, set the default transaction isolation scheme to "read committed", set the timezone

	    ALTER ROLE dbadmin SET client_encoding TO 'utf8';
	    ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';
	    ALTER ROLE dbadmin SET timezone TO 'UTC';
	
	Give user access to administer database

	    GRANT ALL PRIVILEGES ON DATABASE country TO dbadmin;

	Exit		

	    \q

	You can add countries and cities in the admin panel.(/admin)

3)Create a Python Virtual Environment for Project
	
		sudo -H pip3 install --upgrade pip
	    	sudo apt install python3-venv

	Create and move into a directory 

		    mkdir ~/country.com
		    cd ~/country.com
	
	Create a Python virtual environment	
	
		    pyvenv newvenv

	Put sorces into newvenv folder.
	
	Activate the virtual environment

	    	source newvenv/bin/activate

	Install Django, Gunicorn, psycopg2 and other requrements

		pip install django gunicorn psycopg2

		pip install -r requirements.txt

4)Configure a Django Project
	
		python manage.py makemigrations
	    	python manage.py migrate

	Create an administrative user for the project by typing:

	    	python manage.py createsuperuser

	You will have to select a username, provide an email address, and choose and confirm a password.

	Collect all of the static content into the directory location.

	     	python manage.py collectstatic

	Create an exception for port 8000 

	    sudo ufw allow 8000

	Test project by starting up the Django development server

	    python manage.py runserver 0.0.0.0:8000

	Visit your server's domain name or IP address followed by :8000

		http://server_domain_or_IP:8000

	If you append /admin to the end of the URL in the address bar, you will be prompted for the administrative username and password you created with the createsuperuser command

5)Create a Gunicorn systemd Service File

	Create and open a systemd service file for Gunicorn with sudo privileges in your text editor

		sudo gedit /etc/systemd/system/gunicorn.service
	
			Settings example:

				[Unit]
				Description=gunicorn daemon
				After=network.target

				[Service]
				User=usname
				Group=www-data
				WorkingDirectory=/home/usname/country.com/newvenv
				ExecStart=/home/usname/country.com/newvenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/usname/country.com/newvenv/country.sock task_soft.wsgi:application

				[Install]
				WantedBy=multi-user.target
	
	Start the Gunicorn service we created and enable it so that it starts at boot:

	    	sudo systemctl start gunicorn
		sudo systemctl enable gunicorn

	Check the status of the process to find out whether it was able to start:

		sudo systemctl status gunicorn

	If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing
	 
		sudo systemctl daemon-reload
		sudo systemctl restart gunicorn

6)Configure Nginx to Proxy Pass to Gunicorn

	sudo gedit /etc/nginx/sites-available/country.com

	Settings example:

		server {
		    listen 80;
		    server_name 0.0.0.0;

		    location = /favicon.ico { access_log off; log_not_found off; }
		    location /static/ {
			root /home/usname/country.com/nevwenv;
		    }

		    location / {
			include proxy_params;
			proxy_pass http://unix:/home/usname/country.com/newvenv/country.sock;
		    }
		}

	Type:
		sudo ln -s /etc/nginx/sites-available/country.com /etc/nginx/sites-enabled

	Test Nginx configuration for syntax errors
	If no errors are reported, restart Nginx 

	sudo nginx -t && sudo systemctl restart nginx

	Open up our firewall to normal traffic on port 80. 

	    sudo ufw delete allow 8000
	    sudo ufw allow 'Nginx Full'

	You should now be able to go to your server's domain or IP address to view your application.



