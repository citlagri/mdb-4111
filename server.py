
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
#@app.route('/')
#def index():

  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """


  # DEBUG: this is debugging code to see what request looks like
  #print(request.args)


  #
  # example of a database query
  #
 # cursor = g.conn.execute("SELECT name FROM test")
 # names = []
 # for result in cursor:
  #  names.append(result['name'])  # can also be accessed using result[0]
 # cursor.close()
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
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #return render_template("index.html", **context)

#------------------------------------------------------------------------------------------------
#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
#@app.route('/another')
#def another():
 # return render_template("another.html")

#------------------------------------------------------------------------------------------------

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


#------------------------------------------------------------------------------------------------
#ESME'S HOME PAGE 
def generator(keys, record):
  return {key:record for key, record in zip(keys, record)}

@app.route('/home', methods=['GET', 'POST'])
def home():
  #try:
    #show them all of their reviews
  if request.method == 'POST':
    uid = request.form.get('userid')
    labels = ['content','titlename','rating', 'since', 'title']
    cursor = g.conn.execute("SELECT content, title_name, rating, since, title  FROM writes_a NATURAL JOIN has_a WHERE uid = %s", uid)
    reviews = cursor.fetchall() #has all tupeless
    infos = list()
    for review in reviews:
      infos.append(generator(labels, review))
   
    #print(infos) #madde for debugging
    return render_template("home.html", infos=infos)
#except exc.SQLAlchemyError as e:
  #flash("unsuccessful login")
  #print(e)
#except Exception as err:
  #flash("error occured")
  #print(err)
  return render_template("home.html", boolean=True)  

#------------------------------------------------------------------------------------------------
#CIT'S HOME PAGE
@app.route('/', methods=['GET', 'POST'])
def homepage():
   return render_template("homepage.html", boolean=True)

#------------------------------------------------------------------------------------------------

#signup page
@app.route('/signup', methods=['GET','POST'])
def signup():
  #try:
  if request.method == 'POST':
    userid = request.form.get('userid')
    username = request.form.get('username')
    login = request.form.get('login')
    name = request.form.get('name')
    email = request.form.get('email')
    #check first that this user doesnt exist already with their userid
    cursor = g.conn.execute("SELECT uid FROM users WHERE uid = %s ", userid)
    tuples = cursor.rowcount
    cursor.close()
    
    #making sure login is unique and not empty
    cursor = g.conn.execute("SELECT login FROM users WHERE login = %s ", login)
    loginrows = cursor.rowcount
    cursor.close()
    #print(tuples) #for error checking
    if not login:
      return render_template("signup.html", boolean = True)
    elif loginrows == 1:
      return render_template("signup.html", boolean = True)
    #making sure username, name, and email arent empty
    if not username:
      return render_template("signup.html", boolean = True)
    if not name:
      return render_template("signup.html", boolean = True)
    if not email:
      return render_template("signup.html", boolean = True)
    
    #makinf sure user doesn't already exist
    if(tuples == 1):
      return render_template("signup.html", boolean = True)
    else:
      g.conn.execute('INSERT INTO users(uid, username, login, name, email) VALUES (%s, %s, %s, %s, %s)', (userid, username, login, name, email))
      cursor = g.conn.execute("SELECT uid FROM users WHERE username = %s AND login=%s AND name=%s AND email = %s", (username, login, name, email))
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
  #try:
  if request.method == 'POST':
    userid = request.form.get('userid')
    login = request.form.get('login')
    if not userid:
      return render_template("login.html", boolean=True)
    if not login:
      return render_template("login.html", boolean=True)
    cursor = g.conn.execute("SELECT uid FROM users WHERE uid = %s AND login = %s", (userid, login))
    tuples = cursor.rowcount
    #cursor.close()
    print(tuples)
    if(tuples != 1):
      return render_template("login.html", boolean=True)
    else:
      users = []
      for usersid in cursor:
        users.append(usersid)
        cursor.close()
        context = dict(data = users)
        return render_template("home.html", **context)
      
  return render_template("login.html", boolean=True)


#------------------------------------------------------------------------------------------------

@app.route('/writereview', methods=['GET','POST'])
def writereview():
  if request.method == 'POST':
    content = request.form.get('review')
    title = request.form.get('title')
    rating =  request.form.get('rating')
    since = request.form.get('since')
    userid = request.form.get('userid')
    songtitle = request.form.get('songtitle')
    reviewid = 27
    print(reviewid)# debugging
    print(request.form)
    print(songtitle)
    print(rating)

    #check if null
    if not content:
      render_template("writereview.html", boolean = True)
    if not title:
      render_template("writereview.html", boolean = True)
    if not rating:
      render_template("writereview.html", boolean = True)
    if not since:
      render_template("writereview.html", boolean = True)
    if not userid:
      render_template("writereview.html", boolean = True)
    if not songtitle:
      render_template("writereview.html", boolean = True)

    #make sure uid exists
    cursor = g.conn.execute("SELECT uid FROM users WHERE uid = %s", userid)
    tuples = cursor.rowcount
    if (tuples != 1):
      render_template("error.html", boolean = True)

    #making sure single exists
    cursor = g.conn.execute("SELECT title FROM singles WHERE LOWER(title) = LOWER(%s)", songtitle)
    singletup = cursor.rowcount
    print(cursor)#debugging
    cursor.close()
    if singletup != 1:
      render_template("error.html", boolean = True)

    #selecting max rid toincrement by one and create new rid and cast it as char again
    cursor = g.conn.execute("SELECT MAX(CAST(rid AS INTEGER)) FROM writes_a")
    newrid = []
    for result in cursor:
      newrid.append(result[0]) 
    newrids = newrid[0] + 1
    print("Line 346 when it's a int")
    print(newrids)
    
    newrids = str(newrids)
    print("Line 350 when its a sstring")
    print(newrids)#error checking

    #insert tuple to writes_a

    # (newrid, content, title, rating, since, userid, songtitle))
    #g.conn.execute('INSERT INTO writes_a (rid, rating, content, title_name, since, uid) VALUES (%s, %s, %s, %s, %s, %s)',\
      # str(newrids), str(rating), str(content), str(title), str(since), str(userid))

    g.conn.execute('INSERT INTO writes_a (rid, content, title_name, rating, since, uid) VALUES (%s, %s, %s, %s, %s, %s)',\
       str(newrids), str(content), str(title), str(rating), str(since), str(userid))
    #get release_date of the single
    cursor = g.conn.execute("SELECT release_date FROM singles WHERE title = %s", songtitle)
    st = []
    for t in cursor:
      st.append(t[0])
    

    #get main artist of the single
    cursor = g.conn.execute("SELECT main_artist FROM singles WHERE title = %s", songtitle)
    ma = []
    for m in cursor:
      ma.append(m[0])
    print(len(st))
    print(len(ma))
    print(st)
    print(ma)
    g.conn.execute('INSERT INTO has_a (uid, rid, title, release_date, main_artist, since) VALUES (%s, %s, %s, %s, %s, %s)',\
       (userid, newrids, songtitle, st[0], ma[0], since))
    return render_template("home.html", boolean = True)


  return render_template("writereview.html", boolean = True)

#------------------------------------------------------------------------------------------------
#SEARCH ARTISTS PAGE

@app.route('/searchArtists', methods=['GET','POST'])
def searchArtists():

  if request.method == 'POST':
        userInput = request.form.get('stagename')

        if not userInput:
               cursor = g.conn.execute("SELECT stage_name FROM artists")
               stagenames = []
               for result in cursor:
                 stagenames.append(result[0])  # can also be accessed using result[0]

               cursor = g.conn.execute("SELECT birthday FROM artists")
               birthdays = []
               for bdays in cursor:
                 birthdays.append(bdays[0])

               cursor = g.conn.execute("SELECT real_name FROM artists")
               realname = []
               for rn in cursor:
                 realname.append(rn[0])

               cursor = g.conn.execute("SELECT year_started FROM artists")
               yearstarted = []
               for ys in cursor:
                 yearstarted.append(ys[0])

               cursor = g.conn.execute("SELECT years_active FROM artists")
               yearsactive = []
               for ya in cursor:
                 yearsactive.append(ya[0])

               cursor = g.conn.execute("SELECT genre FROM artists")
               genre = []
               for genres in cursor:
                 genre.append(genres[0])

               cursor = g.conn.execute("SELECT role FROM artists")
               role = []
               for r in cursor:
                 role.append(r[0])

               cursor.close()

               context = {
                 "stagenameis": stagenames,
                 "birthdays": birthdays,
                 "realname": realname,
                 "yearstarted": yearstarted,
                 "yearsactive": yearsactive,
                 "genre": genre,
                 "role": role,
               }
               return render_template("searchArtistsResults.html", **context)

            #-------------------------
        cursor = g.conn.execute("SELECT stage_name FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        stagenames = []
        for result in cursor:
          stagenames.append(result[0])  # can also be accessed using result[0]

        if not stagenames:
              return render_template("error.html", boolean = True)

        cursor = g.conn.execute("SELECT birthday FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        birthdays = []
        for bdays in cursor:
          birthdays.append(bdays[0])

        cursor = g.conn.execute("SELECT real_name FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        realname = []
        for rn in cursor:
          realname.append(rn[0])

        cursor = g.conn.execute("SELECT year_started FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        yearstarted = []
        for ys in cursor:
          yearstarted.append(ys[0])

        cursor = g.conn.execute("SELECT years_active FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        yearsactive = []
        for ya in cursor:
          yearsactive.append(ya[0])

        cursor = g.conn.execute("SELECT genre FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        genre = []
        for genres in cursor:
          genre.append(genres[0])

        cursor = g.conn.execute("SELECT role FROM artists WHERE LOWER(stage_name) = LOWER(%s)", userInput)
        role = []
        for r in cursor:
          role.append(r[0])

        cursor.close()

        context = {
          "stagenameis": stagenames,
          "birthdays": birthdays,
          "realname": realname,
          "yearstarted": yearstarted,
          "yearsactive": yearsactive,
          "genre": genre,
          "role": role,
       }
        return render_template("searchArtistsResults.html", **context)

  return render_template("searchArtists.html", boolean = True)

#------------------------------------------------------------------------------------------------
#SEARCH SINGLES PAGE

@app.route('/searchSingles', methods=['GET','POST'])
def searchSingles():

  if request.method == 'POST':
        userInput = request.form['title']

        if not userInput:

              cursor = g.conn.execute("SELECT title FROM singles")
              title = []
              for result in cursor:
                title.append(result[0])

              cursor = g.conn.execute("SELECT release_date FROM singles")
              releasedate = []
              for rd in cursor:
                releasedate.append(rd[0])

              cursor = g.conn.execute("SELECT main_artist FROM singles")
              mainartist = []
              for main in cursor:
                mainartist.append(main[0])

              cursor = g.conn.execute("SELECT genre FROM singles")
              genre = []
              for gs in cursor:
                genre.append(gs[0])

              cursor = g.conn.execute("SELECT part_of_album FROM singles")
              album = []
              for a in cursor:
                album.append(a[0])

              cursor.close()
              context = {
                "title": title,
                "releasedate": releasedate,
                "main": mainartist,
                "genre": genre,
                "album": album,
              }
              return render_template("searchSinglesResults.html", **context)

    #-------------------------------------
        cursor = g.conn.execute("SELECT title FROM singles WHERE LOWER(title) = LOWER(%s)", userInput)
        title = []
        for result in cursor:
          title.append(result[0])

        if not title:
              return render_template("error.html", boolean = True)

        cursor = g.conn.execute("SELECT release_date FROM singles WHERE LOWER(title) = LOWER(%s)", userInput)
        releasedate = []
        for rd in cursor:
          releasedate.append(rd[0])

        cursor = g.conn.execute("SELECT main_artist FROM singles WHERE LOWER(title) = LOWER(%s)", userInput)
        mainartist = []
        for main in cursor:
          mainartist.append(main[0])

        cursor = g.conn.execute("SELECT genre FROM singles WHERE LOWER(title) = LOWER(%s)", userInput)
        genre = []
        for gs in cursor:
          genre.append(gs[0])

        cursor = g.conn.execute("SELECT part_of_album FROM singles WHERE LOWER(title) = LOWER(%s)", userInput)
        album = []
        for a in cursor:
          album.append(a[0])
        cursor.close()
        context = {
                  "title": title,
                  "releasedate": releasedate,
                  "main": mainartist,
                  "genre": genre,
                  "album": album,
              }
        return render_template("searchSinglesResults.html", **context)

  return render_template("searchSingles.html", boolean = True)


#------------------------------------------------------------------------------------------------
#SEARCH GRAMMYS WON BY AN ARTIST
#need to figure out how the drop down menu allows user input 

@app.route('/searchGrammy', methods=['GET','POST'])
def searchGrammy():

  if request.method == 'POST':
    userInput = request.form['artist']

    if not userInput:
      return render_template("error.html", boolean = True)

    cursor = g.conn.execute("SELECT award FROM awarded_to WHERE LOWER(main_artist) = LOWER(%s)", userInput)
    award = []
    for a in cursor:
      award.append(a[0])

    if not award:
      return render_template("error.html", boolean = True)

    cursor = g.conn.execute("SELECT year FROM awarded_to WHERE LOWER(main_artist) = LOWER(%s)", userInput)
    year = []
    for y in cursor:
      year.append(y[0])

    cursor = g.conn.execute("SELECT release_date FROM awarded_to WHERE LOWER(main_artist) = LOWER(%s)", userInput)
    releasedate = []
    for rd in cursor:
      releasedate.append(rd[0])

    cursor = g.conn.execute("SELECT title FROM awarded_to WHERE LOWER(main_artist) = LOWER(%s)", userInput)
    title = []
    for ma in cursor:
      title.append(ma[0])

    cursor = g.conn.execute("SELECT main_artist FROM awarded_to WHERE LOWER(main_artist) = LOWER(%s)", userInput)
    mainartist = []
    for ma in cursor:
      mainartist.append(ma[0])
    cursor.close()

    context = {
                "award": award,
                "year": year,
                "title": title,
                "releasedate": releasedate,
                "mainartist": mainartist,
    }
    return render_template("searchGrammyResults.html", **context)

  return render_template("searchGrammy.html", boolean = True)

#------------------------------------------------------------------------------------------------
#YOUR BOOKMARKED ARTISTS

@app.route('/searchBookmarkedArtists', methods=['GET','POST'])
def searchBookmarkedArtists():

  if request.method == 'POST':
        userInput = request.form['uid']

        if not userInput:
              return render_template("error.html", boolean = True)

        cursor = g.conn.execute("SELECT users FROM users  WHERE uid = %s", userInput)
        check = []
        for ch in cursor:
          check.append(ch[0])  # can also be accessed using result[0]

        if not check:
              return render_template("error.html", boolean = True)


        cursor = g.conn.execute("SELECT stage_name FROM artists NATURAL JOIN bookmarks_artist  WHERE uid = %s", userInput)
        stagenames = []
        for result in cursor:
          stagenames.append(result[0])  # can also be accessed using result[0]

        cursor = g.conn.execute("SELECT birthday FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        birthdays = []
        for bdays in cursor:
          birthdays.append(bdays[0])

        cursor = g.conn.execute("SELECT real_name FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        realname = []
        for rn in cursor:
          realname.append(rn[0])

        cursor = g.conn.execute("SELECT year_started FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        yearstarted = []
        for ys in cursor:
          yearstarted.append(ys[0])

        cursor = g.conn.execute("SELECT years_active FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        yearsactive = []
        for ya in cursor:
          yearsactive.append(ya[0])

        cursor = g.conn.execute("SELECT genre FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        genre = []
        for genres in cursor:
          genre.append(genres[0])

        cursor = g.conn.execute("SELECT role FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        role = []
        for r in cursor:
          role.append(r[0])

        cursor = g.conn.execute("SELECT since FROM artists NATURAL JOIN bookmarks_artist WHERE uid = %s", userInput)
        sincedate = []
        for s in cursor:
          sincedate.append(s[0])
        cursor.close()

        context = {
          "stagenameis": stagenames,
          "birthdays": birthdays,
          "realname": realname,
          "yearstarted": yearstarted,
          "yearsactive": yearsactive,
          "genre": genre,
          "role": role,
          "since": sincedate,
       }
        return render_template("searchBookmarkedArtistsResults.html", **context)

  return render_template("searchBookmarkedArtists.html", boolean = True)

#------------------------------------------------------------------------------------------------
#BOOKMARK AN ARTIST

@app.route('/addBookmarkArtist', methods=['GET','POST'])
def addBookmarkArtist():
    if request.method == 'POST':
      userid = request.form.get('userid')
      artist = request.form.get('artist')
      since = request.form.get('since')

      if not userid:
            return render_template("error.html", boolean = True)

      if not artist:
            return render_template("error.html", boolean = True)

      if not since:
            return render_template("error.html", boolean = True)

      cursor = g.conn.execute("SELECT users FROM users  WHERE uid = %s", userid)
      check = []
      for ch in cursor:
        check.append(ch[0])  # can also be accessed using result[0]

      if not check:
            return render_template("error.html", boolean = True)

      cursor = g.conn.execute("SELECT artist_id FROM artists WHERE LOWER(stage_name) = LOWER(%s)", artist)
      mainartist = []
      for ma in cursor:
        mainartist.append(ma[0])

      if not mainartist:
            return render_template("error.html", boolean = True)

      cursor = g.conn.execute("SELECT uid, artist_id FROM bookmarks_artist WHERE uid = %s AND artist_id = %s",(userid, mainartist[0]))
      reviews = cursor.rowcount
      print(reviews)
      cursor.close() 
      if (reviews == 1):
        return render_template("error.html", boolean = True)
      else:
        g.conn.execute('INSERT INTO bookmarks_artist(uid, artist_id, since) VALUES (%s, %s, %s)', (userid, mainartist[0], since))
        return render_template("home.html", boolean = True)
    return render_template("addBookmarkArtist.html", boolean = True)

#------------------------------------------------------------------------------------------------
# YOUR BOOKMARKED SINGLES
#they enter their username and it asks postgre for where the id matches userid in bookmars_singles
#returns a table of their results 

@app.route('/searchBookmarkedSingles', methods=['GET','POST'])
def searchBookmarkedSingles():

  if request.method == 'POST':
        userInput = request.form['uid']

        if not userInput:
              return render_template("error.html", boolean = True)

        cursor = g.conn.execute("SELECT users FROM users  WHERE uid = %s", userInput)
        check = []
        for ch in cursor:
          check.append(ch[0])  # can also be accessed using result[0]

        if not check:
              return render_template("error.html", boolean = True)


        cursor = g.conn.execute("SELECT title FROM singles NATURAL JOIN bookmarks_singles WHERE uid = %s", userInput)
        title = []
        for result in cursor:
          title.append(result[0])

        cursor = g.conn.execute("SELECT release_date FROM singles NATURAL JOIN bookmarks_singles WHERE uid = %s", userInput)
        releasedate = []
        for rd in cursor:
          releasedate.append(rd[0])

        cursor = g.conn.execute("SELECT main_artist FROM singles NATURAL JOIN bookmarks_singles WHERE uid = %s", userInput)
        mainartist = []
        for main in cursor:
          mainartist.append(main[0])

        cursor = g.conn.execute("SELECT genre FROM singles NATURAL JOIN bookmarks_singles WHERE uid = %s", userInput)
        genre = []
        for gs in cursor:
          genre.append(gs[0])

        cursor = g.conn.execute("SELECT part_of_album FROM singles NATURAL JOIN bookmarks_singles WHERE uid = %s", userInput)
        album = []
        for a in cursor:
          album.append(a[0])

        cursor = g.conn.execute("SELECT since FROM singles NATURAL JOIN bookmarks_singles WHERE uid = %s", userInput)
        since = []
        for s in cursor:
          since.append(s[0])
        cursor.close()

        context = {
                  "title": title,
                  "releasedate": releasedate,
                  "main": mainartist,
                  "genre": genre,
                  "album": album,
                  "since": since,
              }
        return render_template("searchBookmarkedSinglesResults.html", **context)

  return render_template("searchBookmarkedSingles.html", boolean = True)


#------------------------------------------------------------------------------------------------
#BOOKMARK A SINGLE

@app.route('/addBookmarkSingle', methods=['GET','POST'])
def addBookmarkSingle():
    if request.method == 'POST':
      userid = request.form.get('userid')
      title = request.form.get('single')
      since = request.form.get('since')

      if not userid:
            return render_template("error.html", boolean = True)

      if not title:
            return render_template("error.html", boolean = True)

      if not since:
            return render_template("error.html", boolean = True)

      cursor = g.conn.execute("SELECT users FROM users  WHERE uid = %s", userid)
      check = []
      for ch in cursor:
        check.append(ch[0])  # can also be accessed using result[0]

      if not check:
            return render_template("error.html", boolean = True)

      cursor = g.conn.execute("SELECT title FROM singles WHERE LOWER(title) = LOWER(%s)", title)
      title = []
      for t in cursor:
        title.append(t[0])
      
      if not title:
            return render_template("error.html", boolean = True)

      cursor = g.conn.execute("SELECT release_date FROM singles WHERE LOWER(title) = LOWER(%s)", title)
      releasedate = []
      for rd in cursor:
        releasedate.append(rd[0])

      cursor = g.conn.execute("SELECT main_artist FROM singles WHERE LOWER(title) = LOWER(%s)", title)
      mainartist = []
      for ma in cursor:
        mainartist.append(ma[0])
    
      cursor = g.conn.execute("SELECT uid, title, release_date, main_artist FROM bookmarks_singles WHERE uid = %s AND title = %s AND release_date = %s AND main_artist = %s",(userid, title[0], releasedate[0], mainartist[0]))
      reviews = cursor.rowcount
      print(reviews)
      cursor.close() 
      if (reviews == 1):
        return render_template("error.html", boolean = True)
      else:
        g.conn.execute('INSERT INTO bookmarks_singles(uid, title, release_date, main_artist, since) VALUES (%s, %s, %s, %s, %s)', (userid, title[0], releasedate[0], mainartist[0], since))
        return render_template("home.html", boolean = True)

     # g.conn.execute('INSERT INTO bookmarks_single(uid, title, release_date, main_artist, since) VALUES (%s, %s, %s, %s, %s)', (userid, title[0], releasedate[0], mainartist[0], since))
      #return render_template("homepage.html", boolean = True)

    return render_template("addBookmarkSingle.html", boolean = True)

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
    app.run(host=HOST, port=PORT, threaded=threaded, debug = True)
    app.debug = True

  run()
