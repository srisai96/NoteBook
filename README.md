# NoteBook
A multi-user blog using webapp2-python and Bootstrap that can be readily deployed to Google App Engine.

Built with
==========
- Python
- Google App Engine
- webapp2
- Bootstrap3
- Jinja2

How to use
==========
This app can be deployed to GAE or run locally by Launcher Application.

Functionality
============
1. User Accounts:
  Users account activity is implemented using secured cookies. Usernames are maintained to be unique. The password is stored as Hash values with salted compound.
  User activities
  - Sign-up
  - Sign-in 
  - Sign-out 
2. Blog Posts:
  Registered users can post to the blog. That post can later be edited or deleted by the author.
3.  Commenting:
  Posts can be commented by any of registered user. Unregistered users can view the comments. Registered users can edit or delete their own comments.
4.  Like/Dislike:
  Each of the post can be like/disliked by other registered users (Not the Author). User can't dislike a post if they haven't already liked it.
5. Follow:
  A user can follow other user to quickly view all their posts.
6. Trending:
  A registered user can find top 5 trending posts in his home page. Using this section he can quickly catch up with all the latest content. 
  

The app is available on GAE at:https://iiitmsitcallouts.appspot.com
