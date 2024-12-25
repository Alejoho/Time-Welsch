# Time Welsch

#### Video Demo: \<URL HERE\>

#### Description:

TODO: Write the description asked for the cs50 stuff
---

#### How to test the app:

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

4. **Create the db**: Run the `db_script.py` file

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

Whit this you have sets up the db. And now to run the app just run the `run.py` file and test it out. But with this configuration you can just access the app through the demo users. To use the full functionality of the app like normal registration with confirmation email, normal login, contact me and reset password continue with the next steps.

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
