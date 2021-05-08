A final project is a part of the famous CS50 course curriculum. This is my final project. It works as a personal diary. 

The tech stack HTML, CSS, Python, Flask, Sqlite

Here is how it looks,




A basic demonstration of the web app can be found in this link https://youtu.be/-wCyZu21gFU


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
