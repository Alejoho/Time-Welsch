# Time Welsch

## Video Demo: https://youtu.be/2pJ7SCmXtAA

## Description:

### What is this app about?

My CS50 final project is a book converted into a web app, which you can register in and read all the different chapters of the book and it keeps track of what chapters you already read and when you completed each chapter.

The book is called "La Guía de los Tiempos Verbales: Aprende más inglés" written by Daniel Welsch. I contact him and ask him for permision to use the content of its book for my project. The UI of the app is in spanish because this is a book oriented at a Spanish-speaking audience.

### Project Hierarchy

```
Root Directory
│
├── app
│   ├── forms
│   │   ├── __init__.py
│   │   └── [other form files]
│   ├── models
│   │   ├── __init__.py
│   │   └── [other model files]
│   ├── routes
│   │   ├── __init__.py
│   │   └── [other route files]
│   ├── static
│   │   ├── Bootstrap
│   │   ├── css
│   │   ├── favicon
│   │   ├── images
│   │   └── js
│   ├── templates
│   │   ├── layout.html
│   │   ├── account_management
│   │   ├── chapters
│   │   ├── commons
│   │   ├── errors
│   │   ├── home
│   │   └── main
│   ├── __init__.py
│   ├── config.py
│   └── scheduled_jobs.py
│
├── migrations
│   ├── versions
│   └── [other migration-related files]
│
├── .env
├── .gitignore
├── chapters_script.py
├── chapters.json
├── db_script.py
├── README.md
├── requirements.txt
└── run.py
```

I like to have things well organize so I decided to use this structure. Let's break this a little bit

### forms

I use Flask-WTF and WtForms to manage my forms and validations.

I put every form I use in a separate file and then I include them in the \_\_init\_\_.py to treat the forms folder as a module and not have to dive into each file to reach the piece of code I needed. I did this for the models and the routes folders too, more on those later.

Inside I have a file called custom_validators.py in which I put all my custom validators in the form of classes and then just use them in the form files that need them passing them to the validators parameter of the different fields of WTForms. Doing things this way, in my routes I only have to call the validate_on_submit function and all my validation were executed under the hood. It should be noted that the only validation I didn't this way was the reCaptcha server side validation, because the reCaptchaField of WTForms was implemented with reCaptcha v2 and I used reCaptcha v3.

### models

I use Flask-SQLAlchemy and SQLAlchemy for my models.

I use the model property of the db variable(created in the factory pattern) as a base class and Declarative Mapping style to create my models. I use the \_\_table_args\_\_ to give proper names to my indexes, constraints and foreign keys to give them some semantic meaning in the db and if someone looks the db could understand what going on. I also add some property and functionality inside my models to make the work easy. Some examples are:

- I include a setter in the User model to generate the password hash and a function to verify passwords
- I include a setter and a getter in the same model to access directly a property from a related model
- In the CompletedChapter model I include a property to convert a date from the db into the ISO format

### routes

I separate my routes by its functionality in different files and I use blueprints in each of them. I create the Blueprint variable under the name of `bp` on all of them and them import them with an alias in the \_\_init\_\_.py to avoid conflicts when registering them. I also have two others files in this folder a `complements.py` and `decorators.py`.

I created 4 decorators for different functionalities. For example only give access to certain pages to the unconfirmed users or only give access to other page to the confirm ones. In the main_routes.py all the routes have been decorated with the same 2 decorators `login_required` and `block_unconfirmed_users` so to keep my code DRY I use the `before_request` decorator with a little trick to avoid an error.

```python
@bp.before_request
@login_required
@block_unconfirmed_users
# This is just a function to avoid and error
def bypass_error():
    pass
```

In the `complements.py` I have helper functions to help to do some tasks, like the verification of the reCaptcha, the sending of confirmation emails, the creation of demo users and so on and so forth.

### static

I use local Bootstrap in my project because I have a really bad internet connection and blackout problems, so I put the Bootstrap files in a folder with the same name. I also have a css file for custom styles and images folder for 3 images and a favicon folder to store several favicons. In the js folder I have two scripts one to dinamically generate the links for the navigation index of the chapters and other to convert the date and time to the locale of the user.

### templates

I also separated the templates by functionality in the <ins>home</ins> folder goes the pages to show to unregister users, in the <ins>main</ins> the pages for register ones, I have a folder for the error pages too, another to store the content of the chapters and a <ins>commons</ins> folder to store common content for several pages. In the <ins>account_managment</ins> I put all related pages to accounts like login, register, reset password and other. And I can't forget the `layout.html` which is the base for all the templates.

I want to mention one thing. In the main_routes I use the `context_processor` decorator to inject the chapters details in all the rendered templates.

### Factory pattern

I use the factory pattern to create my app and then run it. I have a `.env` with some needed enviromental variables, then I have a `config.py` file that holds a base config class and other extended classes that loads the enviromental variables in it and then I use the `from_object` function to load all the configuration. Then I init all the extension, configure the ones that need it and register the blueprints

One thing I debated a lot was if I query the db every time I need some info about some chapter or I preload all the chapter's info in memory and I went for the latter because the book only have 32 chapters so it was not so much memory allocated for them.

### Implemented functionalities

I use reCaptcha v3 in all the form that can be accessed without needing to be logged in, and in the change password account because it is a sensible process.

In my register process I use the <ins>Hunter.io</ins> API to check if the email introduced in fact exists, I made checks for unique username and email. Then I send a confirmation email to activate the account, the user can't read any chapter until it confirms its account.

In the login page the check of the user and the check of the match of the password with the user are done also with WTForms custom validators. I include a Remember Me checkbox that allows the user to stay logged in for a month. And if the user forgot its password there a link to reset it.

The functionality I feel most proud of it's the demo user functionality. If someone just want to test my app and view how it works, it has to register and check it's email to confirm it's account, and it's a hassle to do that so at a distance of a few clicks it can create a demo user of one of three types:

- a just registered user with no chapter completed
- a user with the chapters completed until almost the middle
- and a user with only one chapter left to complete the book

The last 2 demo users will have the creation date of its account in the past and the completed chapters will have they completed date accordingly. But I didn't want to have my db filled out of demo users so using Flask-APScheduler and APScheduler I set a daily basis job to delete all demo users with more then day of created. This mean that the last 2 types of demo users always will be deleted when this task is executed and the first one depending on the time could last a little more in the db.

Another interesting functionality it's the blocking of chapter depending of the progress of the user. The user can't access a chapter that is after the one it is currently reading. I achive this with the `check_chapter` decorator.

The web app is fully implemented but I the content is not complete, that is to say, the proccess of take a chapter and convert it into html is a tedious boilerplate task, someone would say use AI for it. I can't. I live in Cuba and most of the AI solutions are blocked for my country. The AI that I have access to it's the Copilot AI of Bing which is limited for some tasks like this one. So I just converted the first 4 chapters, but one was a the page "Why this book?", and the last one because when it is completed the user is shown the completed course page.

Let's talk about a little of how to navigate the chapters and mark them as completed. To access a chapter you can go to the "Mi ruta" page and select a chapter, you can write it's URL or you can navigate through the bottom links back and forth. When you are in the current chapter you're reading the next chapter link won't appear, and a blue button will be at the end. When you click it the chapter will be completed the date will be recorded and you'll be redirect to the next chapter.

Another functionality is the multiple checks when a user is going to delete its account. First a modal appears and the users have to confirm the model and then other model appears and the user needs to type its username and hit delete in order to delete its account.

### Something to mention

I develop this app in my own VSCode using 2 machine a Windows machine and a MacBook Air, and storing my project in a USB drive. Why this?. Well because of the repetitive blackouts that my country(Cuba) is suffering. And why to mention this? Well becuase I have to figured out to keep sync my 2 develop enviroments. In my project folder I had 2 virtual enviroments one called `.venv_win` and the other called `.venv_mac`. So when a blackout arrived I shut down my windows pc and change to my macbook that give me more or less 5 hours of autonomy. I needed to disable the functionalities of my app that needed internet, like the reCaptcha or the Hunter.io API by comment them. And also keep sync my db. But after lots of work I adapted to a moderate productive workflow.

### How to test the app

Note: The major part of this setup is assuming that you are using MySql to manage your db's

1. **Create a virtual enviroment**:

   In Windows run this to create the vm

   ```sh
   python -m venv myenv
   ```

   Then this to activate it

   ```sh
   myenv\Scripts\activate
   ```

   <br>
   <br>

   In macOS or Linux run this to create the vm

   ```sh
   python3 -m venv myenv
   ```

   Then this to activate it

   ```sh
   source myenv/bin/activate
   ```

   <br>

2. **Install the needed packages**:

   Run this command in the terminal:

   ```sh
   pip install -r requirements.txt
   ```

   <br>

3. **Create a `.env` File**:

   In the root directory of your project, create a file named `.env` and add these environment variables to this file:

   ```sh
    CONNECTION_USERNAME=<The username of your connection>
    CONNECTION_PASSWORD=<The password of your connection>
    DB_NAME=<The name of the db>
    APP_SETTINGS=app.config.ProductionConfig
    SECRET_KEY=<A secret key>
   ```

   Note: I recommend to use the same name of the app in the name of the db "time_welsch_db", but the name don't makes any difference.

   <br>

4. **Create the db**:

Run the `db_script.py` file

   <br>

5. **Create the tables**:

   Run this command in the terminal:

   ```sh
   flask db upgrade
   ```

   <br>

6. **Insert the chapters details**:

   Run the `chapters_script.py` file to insert the chapter details in the chapters table of the db.

   <br>

   With this you have sets up the db. And now to run the app just run the `run.py` file and test it out. But with this configuration you can just access the app through the demo users. To use the full functionality of the app like normal registration with confirmation email, normal login, contact me and reset password continue with the next step.

7. **Add others enviromental variables need it for the app**:

   To the '.env' created earlier add these other variables:

   ```sh
    SECURITY_PASSWORD_SALT=<Another secret key>
    HUNTER_API_KEY=<An API key of hunter.io>
    RECAPTCHA_PUBLIC_KEY=<A public key of google reCaptcha service>
    RECAPTCHA_PRIVATE_KEY=<A private key of google reCaptcha service>
    MAIL_USERNAME=<An email account>
    MAIL_PASSWORD=<The password of the email account>
    MAIL_DEFAULT_SENDER=<The email address that will send the confirmation emails>
    MAIL_CONTACT_ME_RECEIVER=<The email address that will receive the messages of contact>
   ```

   <br>

With all this sets up your have access to all the functionality of the **Time Welsch** web app.
