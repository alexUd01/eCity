# eCity  -  Assessing students on the go has never been this hassle-free.
### Easily create quizes, set examination questions, as well as other assessments for your students ON THE GO!

## Introduction
[eCity](https://ecity.xandex.tech) is a Computer Based Test (CBT) platform that
was designed to provide teachers at various of education, with advanced tools
that will enable them to easily create quizzes or examinations with the aim
of remotely assessing their  students anywhere around the world.

Checkout [eCity's blog post](https://www.linkedin.com/pulse/my-first-attempt-creating-computer-based-test-cbt-app-ikpeama) for more information.

[Reachout to me on linkedin](https://www.linkedin.com/in/alexander-ikpeama-442296244)


## Installation
First things first. Run the command bellow to update your linux apps database.
> `$ sudo apt-get update`
>
Before attempting to spin eCity's web server ensure that you have the
following software packages installed on your linux machine:

 - Python3:  `$ sudo apt-get install python3`
 - MySQL:  `$ sudo apt-get install mysql-client mysql-community-server mysql-server`
 - Flask Framework:  `$ pip install flask`
 - Flask_Sqlalchemy:  `$ pip install flask_sqlalchemy`

### Installation is simple and easy.
First clone this repository.
> ```
> $ git clone https://github.com/alexud01/eCity.git
> $
> $ cd eCity/
> $
> ```

The next thing to do is to setup your MySQL database and populate it with data. 
For new mysql users follow the steps provided in [this guide](https://phoenixnap.com/kb/install-mysql-ubuntu-20-04) 
or [this other giude](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) to set-up your database. 
After MySQL setup is successful, fire-up your mysql terminal and create a new
database with the name `ecity`, a new user with the name `User3` with password set to `password`
and grant the user permission to view and manipulate tables in the database named `ecity` _(which you just created)_.
> ```
> $ sudo systemctl start mysql  # Starts mysql server
> $ sudo systemctl enable mysql  # Enables auto start-up whenever the system is rebooted
> $ mysql -p
> Enter password:
>     ...
>     ...
> mysql> CREATE DATABASE ecity;         -- Create database
> Query OK, 1 row affected (0.308 sec)
> mysql> CREATE USER 'User3' identified by 'password';  -- Create User3
> Query OK, 0 rows affected (0.743 sec)
> mysql> GRANT ALL PRIVILEGES ON ecity.* TO User3;     -- Grant User3 permission
> Query OK, 0 rows affected (0.155 sec)
> mysql> exit
> Bye
> ```

After creating this database run the following command to populate it with data;
> ```
> $ sudo mysql ecity < ecity/models/ecity-bak-3.sql
> $
> ```

After all the steps above, installation setup is finished just run the following commands to start eCity's web server
> ```
> $ python3 -m ecity.app.ecity_app
> ```
