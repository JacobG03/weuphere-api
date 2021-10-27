from app import app


@app.get('/api')
def api():
  return {
    'message': 'Greetings! The API seems to be working..',
    'routes': []
  }

#! get /api/user    (current_user) (:user === some other user)
#? post /api/user/login
#? post /api/user/register
#* get /api/:user     (:user or :id)
#* /api/:user/profile
#* /api/:user/history   etc..


#! /api/user/settings
#* /api/user/settings/delete_account


#! get /api/users     returns all /users routes
#* get /api/users/1/500  default by id  (500 being the limit)
#* get /api/users/1/500?sort=new   // newest users
#* get /api/users/1/500?sort=old   // oldest users    etc..


