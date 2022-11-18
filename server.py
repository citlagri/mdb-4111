
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
from types import GetSetDescriptorType
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, flash, url_for, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#------------------------------------------------------------------------------------------------

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@34.75.94.195/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.75.94.195/proj1part2"
#
DATABASEURI = "postgresql://cg3236:4602@34.75.94.195/proj1part2"
#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#------------------------------------------------------------------------------------------------


#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

#------------------------------------------------------------------------------------------------

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """


  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
#------------------------------------------------------------------------------------------------

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#------------------------------------------------------------------------------------------------
#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")

#------------------------------------------------------------------------------------------------

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')

@app.route('/home', methods=['GET', 'POST'])
def home():
  #show them all of their reviews
  if request.method == 'POST':
    uid = request.form.get['userid']
    cursor = g.conn.execute("SELECT content, title_name, rating, since FROM writes_a WHERE uid = %s", uid)
    reviews = []
    for thesereviews in reviews:
      reviews.appaend(thesereviews[0])
    cursor.close()
    review = dict(r = thesereviews)
    return render_template("home.html", **review)
  return render_template("home.html", boolean=True) 

#signup page
@app.route('/signup', methods=['GET','POST'])
def signup():
  if request.method == 'POST':
    username = request.form.get['username']
    login = request.form.get['login']
    name = request.form.get['name']
    email = request.form.get['email']
    g.conn.execute('INSERT INTO users(username, login, name, email) VALUES (%s, %s, %s, %s)', username, login, name, email)
    cursor = g.conn.execute("SELECT uid FROM users WHERE username = %s AND login=%s AND name=%s AND email = %s", username, login, name, email)
    ##HOW IS USERID BEING GENERATED?
    uids = []
    for userids in cursor:
      uids.append(userids[0]) 
    cursor.close()
    context = dict(data = userids)
    return render_template("home.html", **context)

  return render_template("signup.html", boolean=True)

#------------------------------------------------------------------------------------------------
#lOGIN PAGE 

@app.route('/login', methods=['GET','POST'])
def login():
  try:
    if request.method == 'POST':
      userid = request.form.get('userid')
      login = request.form.get('login')
      cursor = g.conn.execute("SELECT uid FROM users WHERE uid = %s AND login = %s", (userid, login))
      users = []
      for usersid in cursor:
        users.append(usersid)
        cursor.close()
        context = dict(data = users)
        if(len(users) != 0):
          return render_template("home.html", **context)
        else:
          #have message that says you don't an account, create one please!
          #try and error?_?_?_?
          return render_template("login.html", boolean=True)
  except exc.SQLAlchemyError as e:
    flash("unsuccessful login")
    print(e)
  except Exception as err:
    flash("error occured")
    print(err)
      
  return render_template("login.html", boolean=True)
    #abort(401)
    #this_is_never_executed()


#------------------------------------------------------------------------------------------------

@app.route('/writereview', methods=['GET','POST'])
def writereview():
  if request.method == 'POST':
    content = request.form.get['review']
    title = request.form.get['title']
    rating =  request.form.get['rating']
    since = request.form.get['since']
    userid = request.form.get['userid']
    g.conn.execute('INSERT INTO writes_a (content, title_name, rating, since, uid) VALUES (%s, %s, %d, %s, %s)', content, title, rating, since, userid)
    #don't know how to enter date
    #automatically picks out rid? it's a primary key
    #flash that their review has been received
    #how to take care of cases where it's rejected?

  return render_template("writereview.html", boolean = True)

#------------------------------------------------------------------------------------------------
#SEARCH ARTISTS PAGE

@app.route('/searchArtists', methods=['GET','POST'])
def searchArtists():

  if request.method == 'POST':
        userInput = request.form.get['stage_name']

#HOW DO I DEAL WITH SQL INJECTION VULNERABILITY WITH THE USERINPUT
        cursor = g.conn.execute("SELECT stage_name FROM artists WHERE stage_name = %s", userInput)
        stage_names = []
        for result in cursor:
          stage_names.append(result[0])  # can also be accessed using result[0]

        cursor = g.conn.execute("SELECT birthday FROM artists WHERE stage_name = %s", userInput)
        birthdays = []
        for bdays in cursor:
          birthdays.append(bdays[0])

        cursor = g.conn.execute("SELECT real_name FROM artists WHERE stage_name = %s", userInput)
        real_name = []
        for rn in cursor:
          real_name.append(rn[0])

        cursor = g.conn.execute("SELECT year_started FROM artists WHERE stage_name = %s", userInput)
        year_started = []
        for ys in cursor:
          year_started.append(ys[0])

        cursor = g.conn.execute("SELECT years_active FROM artists WHERE stage_name = %s", userInput)
        years_active = []
        for ya in cursor:
          years_active.append(ya[0])

        cursor = g.conn.execute("SELECT genre FROM artists WHERE stage_name = %s", userInput)
        genre = []
        for genres in cursor:
          genre.append(genres[0])

        cursor = g.conn.execute("SELECT role FROM artists WHERE stage_name = %s", userInput)
        role = []
        for result in cursor:
          role.append(result[0])

        cursor.close()

        context = {
          "stage_name": result[0],
          "birthday": bdays[0],
          "real_name": rn[0],
          "year_started": ys[0],
          "years_active": ya[0],
          "genre": genres[0],
          "role": result[0],
       }
        return render_template("searchArtistsResults.html", **context)
    
  return render_template("searchArtistsResults.html", boolean = True)

#------------------------------------------------------------------------------------------------
#SEARCH SINGLES PAGE
@app.route('/searchSingles', methods=['GET','POST'])
def searchSingles():

  if request.method == 'POST':
        userInput = request.form['title']

        cursor = g.conn.execute("SELECT title FROM singles WHERE title = %s", userInput)
        title = []
        for result in cursor:
          title.append(result[0])

        cursor = g.conn.execute("SELECT release_date FROM singles WHERE title = %s", userInput)
        release_date = []
        for rd in cursor:
          release_date.append(rd[0])

        cursor = g.conn.execute("SELECT genre FROM singles WHERE title = %s", userInput)
        genre = []
        for gs in cursor:
          genre.append(GetSetDescriptorType[0])

        cursor = g.conn.execute("SELECT role FROM singles WHERE title = %s", userInput)
        role = []
        for roles in cursor:
          role.append(roles[0])
        cursor.close()

        context = {
                  "title": result[0],
                  "release_date": rd[0],
                  "genre": gs[0],
                  "role": roles[0],
              }
        return render_template("searchSinglesResults.html", **context)

  return render_template("searchSinglesResults.html", boolean = True)

#------------------------------------------------------------------------------------------------
#SEARCH GRAMMYS WON BY AN ARTIST
"""

@app.route('/searchGrammy', methods=['GET','POST'])
def searchGrammy():

  if request.method == 'POST':
        userInput = request.form['artist']

#HOW DO I DEAL WITH SQL INJECTION VULNERABILITY WITH THE USERINPUT 



        cursor = g.conn.execute("SELECT award FROM awarded_to WHERE main_artist = userInput")
        award = []
        for result in cursor:
          award.append(result['award'])

        cursor = g.conn.execute("SELECT year FROM awarded_to WHERE main_artist = userInput")
        year = []
        for result in cursor:
          year.append(result['year'])

        cursor = g.conn.execute("SELECT genre FROM awarded_to WHERE main_artist = userInput")
        genre = []
        for result in cursor:
          genre.append(result['genre'])

        cursor = g.conn.execute("SELECT release_date FROM awarded_to WHERE main_artist = userInput")
        release_date = []
        for result in cursor:
          release_date.append(result['release_date'])

        cursor = g.conn.execute("SELECT main_artist FROM awarded_to WHERE main_artist = userInput")
        main_artist = []
        for result in cursor:
          main_artist.append(result['main_artist'])

        cursor.close()

        context = {
                    "award": award[0],
                    "year": year[0],
                    "genre": genre[0],
                    "release_date": release_date[0],
                    "main_artist_": main_artist[0],
        }
        return render_template("searchGrammyResults.html", **context) 

  return render_template("searchGrammyResults.html", **context)
        
"""

#------------------------------------------------------------------------------------------------
#YOUR BOOKMARKED ARTISTS
# how are we going to look it up -> they enter their username again? -> same goes for singles


#------------------------------------------------------------------------------------------------
#BOOKMARK AN ARTIST
#they enter an artist and we look for them in the artists table and then join it with their table
# or wtf are we doing with this -> the same for singles

#------------------------------------------------------------------------------------------------
# YOUR BOOKMARKED SINGLES


#------------------------------------------------------------------------------------------------
#BOOKMARK A SINGLE


#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, threaded=threaded)
    app.debug = debug

  run()
