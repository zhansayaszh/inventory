# Bass Holding Inventory Project
## Introduction
*The project was uploaded with agreement of the company.
Inventory Project is a comprehensive inventory management system for a company, leveraging Django and PostgreSQL. This
solution streamlines authorization, offers tailored admin, moderator, and user interfaces, and features robust item
management (CRUD, search, sort, filter) including QR code scanning. Enhanced efficiency by automating data
integration from 1C accounting files for over 900 items, addressing previous issues of manual errors, data loss, and theft.
## Skills
- Python
- Django
- Pandas
## Requirements
Please see requirements.txt
## What Have Done
- I Made an Authorization and Authentication for users.
There are three types of users(superuser, moderator, and
ordinary user).
- SuperUser is Django Admin, so he/she has all permissions
to do CRUD operations in Django.
- The moderator could register ordinary users and assign them
as moderators, if it is necessary, and also do CRUD
operations, but he/she cannot delete SuperUser, whereas
SuperUser can.
- The ordinary user, when entering his/her dashboard, can see
only an item assigned to him/her.
The moderator, while registering the ordinary user,
automatically sends a random password via email to that
user.
- All users can restore passwords.
The User can enter via the Login Page as admin, moderator,
or user; all three will be redirected to personal dashboards.
## Models
- There are overall 4 models: the built-in User model with
UserProfile model, CompanyModel, RoleModel, and
ItemModel. UserProfile is connected via foreign keys to User,
Company Model, and RoleModel. 
- ItemModel is connected
via foreign keys to the User and Company Model. When I
delete one of them, the field is_active turns to False, which
means that the record is not deleted, but not active anymore.
## Features
- Implemented CRUD method
- Authorization
- Authentication
- QR scanner
- Excal uploader
## Demonstration
![image](https://github.com/zhansayaszh/inventory_project/assets/28733943/df734045-a3db-46fe-89a4-6861ddcbee39)
![image](https://github.com/zhansayaszh/inventory_project/assets/28733943/75f9fa8f-4d11-451a-91e7-076b55dc037d)
![Снимок экрана 2024-03-13 175807](https://github.com/zhansayaszh/inventory_project/assets/28733943/d283b799-6653-4757-b9b9-216046ea90af)
![Снимок экрана 2024-03-13 180112](https://github.com/zhansayaszh/inventory_project/assets/28733943/1959bfe1-61a7-4f70-8e9e-5bb26219e7f8)
![Снимок экрана 2024-03-13 180540](https://github.com/zhansayaszh/inventory_project/assets/28733943/adca5a3b-ef2e-4469-922b-110a1cf84448)
![image](https://github.com/zhansayaszh/inventory_project/assets/28733943/a1b8d847-16b3-4430-a603-fa60961fd0f9)










