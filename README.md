This is my final project for cs50 course. It is a simple web application
with a flask (python) backend and SQLite database. In the front end
no Javascript is used. Only pure CSS for styling purpose.

The name of the web app is Diary as it acts as a personal diary for the user.

Main Functions:

    1. Sign Up : User can sign up for an account with an unique username and password.
                 For security purpose I used bcrypt hashing function to
                 generate the hash of the user's password and the hash only
                 stored in the database.

    2. Login : Once an user signed up s/he can login into her account and add posts
               which are only visible to herself.

    3. Add Post : Only after logging in one can access this route. In this route
                  user could add posts. The posts could be entirely text based or
                  s/he could add only image per post. There is no limit for the
                  number of posts, one can posts as many as s/he wants.

    4. Home : In the home route user would able to see the posts sorted in decending
              order according to the date. There is also a bit of styling at hovering
              the mouse pointer on any post. Also posts could be deleted by clicking
              on the delete icon at the bottom of each post. There is no option to
              edit the posts, nor any option to delete in bulk.
