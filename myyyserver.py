#SEARCH GRAMMYS WON BY AN ARTIST

#need to figure out how the drop down menu allows user input 

@app.route('/searchGrammy', methods=['GET','POST'])
def searchGrammy():

  if request.method == 'POST':
        userInput = request.form['artist']

        cursor = g.conn.execute("SELECT award FROM awarded_to WHERE main_artist = userInput")
        award = []
        for a in cursor:
          award.append(a[0])

        cursor = g.conn.execute("SELECT year FROM awarded_to WHERE main_artist = userInput")
        year = []
        for y in cursor:
          year.append(y[0])

        cursor = g.conn.execute("SELECT genre FROM awarded_to WHERE main_artist = userInput")
        genre = []
        for g in cursor:
          genre.append(g[0])

        cursor = g.conn.execute("SELECT release_date FROM awarded_to WHERE main_artist = userInput")
        releasedate = []
        for rd in cursor:
          releasedate.append(rd[0])

	cursor = g.conn.execute("SELECT main_artist FROM awarded_to WHERE main_artist = userInput")
        mainartist = []
        for ma in cursor:
          mainartist.append(ma[0])

        cursor.close()

        context = {
                    "award": a[0],
                    "year": y[0],
                    "genre": g[0],
                    "releasedate": rd[0],
                    "mainartist": ma[0],
        }
        return render_template("searchGrammyResults.html", **context)

  return render_template("searchGrammy.html", **context)


#------------------------------------------------------------------------------------------------
#YOUR BOOKMARKED ARTISTS 
# how are we going to look it up -> they enter their username again? -> same goes for singles

@app.route('/searchBookmarkedArtists', methods=['GET','POST'])
def searchBookmarkedArtists():

  if request.method == 'POST':
        userInput = request.form['uid']

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
          "stagenameis": result[0],
          "birthdays": bdays[0],
          "realname": rn[0],
          "yearstarted": ys[0],
          "yearsactive": ya[0],
          "genre": genres[0],
          "role": r[0],
	  "since": s[0],
       }
        return render_template("searchBookmarkedArtistsResults.html", **context)

  return render_template("searchBookmarkedArtists.html", boolean = True)

#------------------------------------------------------------------------------------------------
#BOOKMARK AN ARTIST
#they enter an artist and we look for them in the artists table and then join it with their table
# or wtf are we doing with this -> the same for singles 
#------------------------------------------------------------------------------------------------
# YOUR BOOKMARKED SINGLES

@app.route('/searchBookmarkedSingles', methods=['GET','POST'])
def searchBookmarkedSingles():

  if request.method == 'POST':
        userInput = request.form['uid']

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
                  "title": result[0],
                  "releasedate": rd[0],
                  "main": main[0],
                  "genre": gs[0],
                  "album": a[0],
		  "since": s[0],
              }
        return render_template("searchBookmarkedSinglesResults.html", **context)

  return render_template("searchBookmarkedSingles.html", boolean = True)


#------------------------------------------------------------------------------------------------
#BOOKMARK A SINGLE



#------------------------------------------------------------------------------------------------
