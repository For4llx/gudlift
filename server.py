import json
from club import Club
from competition import Competition
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

competitions = loadCompetitions()
clubs = loadClubs()

def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html', clubs=clubs)

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition_data = [[c, i] for i, c in enumerate(competitions) if c['name'] == request.form['competition']][0]
        club_data = [[c, i] for i, c in enumerate(clubs) if c['name'] == request.form['club']][0]
        competition = Competition(**competition_data[0])
        club = Club(**club_data[0])
        competition_index = competition_data[1]
        club_index = club_data[1]
        places_required = int(request.form['places'])

        if not competition.name in club.places_booked:
            club.places_booked[competition.name] = 0

        if club.places_booked[competition.name] + places_required > competition.max_places_required:
            flash("Sorry, you can't book more than 12 places for this competition.")
            return render_template('welcome.html', club=club, competitions=competitions)
        elif places_required > competition.numberOfPlaces:
            flash("Sorry, you have selected more places than available.")
            return render_template('welcome.html', club=club, competitions=competitions)
        elif club.points < places_required:
            flash("Sorry, you don't have enough points.")
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            club.remove_points(places_required)
            club.add_places_to_competition(places_required, competition.name)
            club.save(clubs, club_index)
            competition.remove_places(places_required)
            competition.save(competitions, competition_index)

        flash(f'You have successfully booked {places_required} places for the {competition.name}')
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))
    
    return app
