# Models

## [*] User: id, username, email, password, boolean:auth
### [*] User => UserMore: id, avatar, date_of_birth, location
### [] User => UserAlt: id, username, avatar, user_id


## [*] Post: id, title, timestamp, author
### [*] Category: e.g: Image, URL, Text

## [*] Comment: id, body, timestamp, post_id user_id, replies
## [*] reply: id, body, timestamp, user_id, parent, replies

## [*] Reaction: id, emote, parent_id    (works for post, comment and reply respectfully)



# Routes

## [] get /api/user    (current_user) (:user === some other user)
## [] get /api/:user     (:user or :id)
### [] get /api/:user/profile
### [] get /api/:user/history   etc..

## [] post /api/user/login
## [] post /api/user/register


## [] /api/user/settings
### [] /api/user/settings/delete_account


## [] get /api/users     returns all /users routes
### [] get /api/users/1/500  default by id  (500 being the limit)
#### [] get /api/users/1/500?sort=new   // newest users
#### [] get /api/users/1/500?sort=old   // oldest users    etc..
