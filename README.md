# Deploy Django project to AWS EC2 instance

1. Create an EC2 instance
2. Create RDS PostgreSQL instance
3. Login to the instance
4. Clone our repository to the instance
5. Configure ubuntu server
6. Complete the project setup
7. Create systemd Socket and Service files for Gunicorn
8. Configure Nginx to Proxy to Gunicorn
9. Configure permissions for files.

## 4

Clone using either ssh or git token

## 5

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt install python3-venv nginx curl postgresql

psql --host=<DB instance endpoint> --port=<Port> --username=<master username> --password
```

## 6

```shell
#Activate the virtual environment and install required libraries
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
pip install python-dotenv
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py creatuperuser


#Test the local dev server using gunicorn binding
gunicorn --bind 0.0.0.0:8000 mysite.wsgi
```

## 7

```shell
#Create a socket file
sudo vi /etc/systemd/system/gunicorn.socket
```

```bash
#Add contents of socket file
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

```shell
#Create a service file
sudo vi /etc/systemd/system/gunicorn.service
```

```bash
#Service file contents
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/todo_project
ExecStart=/home/ubuntu/todo_project/todo_env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock mysite.wsgi:application

[Install]
WantedBy=multi-user.target
```

```shell
#Add file permissions for ubuntu user
sudo chown ubuntu:ubuntu /etc/systemd/system/gunicorn.socket
sudo chown ubuntu:ubuntu /etc/systemd/system/gunicorn.service

#Start and enable the gunicorn socket
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

## 8

```shell
#creating and opening a new server block in Nginx’s sites-available directory:
sudo vi /etc/nginx/sites-available/demo
```

```bash
#contents of server block
server {
    listen 80;
    server_name 3.68.75.0;

    location = /favicon.ico {access_log off; log_not_found off; }
    location /static/ {
        alias /home/ubuntu/todo_project/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```shell
#disable the default nginx server configuration.
sudo rm /etc/nginx/sites-enabled/default

#create a symbolic link between the default config and the server block created earlier:
sudo ln -s /etc/nginx/sites-available/demo /etc/nginx/sites-enabled/

#Restart nginx:
sudo systemctl restart nginx

#Test your Nginx configuration for syntax errors:
sudo nginx -t
```