from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_set import Country, Base, State, User
from flask import session as login_session
import random
import string
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Country State item-catalog"
engine = create_engine(
    'sqlite:///stateslist.db', connect_args={'check_same_thread': False},
    echo=True)
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()


# For User login
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))

    login_session['state'] = state
    country = session.query(Country).all()
    state = session.query(State).all()
    return render_template('login.html', STATE=state,
                           country=country, state=state)


# If User already logged
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                 json.dumps(
                                            'Current user already connected'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<center><h2><font color="green">Welcome '
    output += login_session['username']
    output += '!</font></h2></center>'
    output += '<center><img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; -webkit-border-radius: 200px;" '
    output += ' " style = "height: 200px;border-radius: 200px;" '
    output += ' " style = "-moz-border-radius: 200px;"></center>" '
    flash("you are now logged in as %s" % login_session['username'])
    print("Done")
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user


# Getting Information of user
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Getting User email address
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


# To read country JSON data on web server
@app.route('/country/JSON')
def countryJSON():
    country = session.query(Country).all()
    return jsonify(country=[c.serialize for c in country])


# To read country wise of bike JSON
@app.route('/country/<int:country_id>/main/<int:state_id>/JSON')
def countryListJSON(country_id, state_id):
    state_list = session.query(State).filter_by(id=state_id).one()
    return jsonify(State_List=state_list.serialize)


# To read states JSON
@app.route('/country/<int:state_id>/main/JSON')
def stateListJSON(state_id):
    country = session.query(Country).filter_by(id=state_id).one()
    state = session.query(State).filter_by(state_id=country.id).all()
    return jsonify(StateList=[i.serialize for i in state])


# This is the home page of entire project
@app.route('/country/')
def showCountry():
    country = session.query(Country).all()
    return render_template('country.html', country=country)


# Create New Country
@app.route('/country/new/', methods=['GET', 'POST'])
def newCountry():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'],
                             user_id=login_session['user_id'])
        session.add(newCountry)
        session.commit()
        return redirect(url_for('showCountry'))
    else:
        return render_template('newCountry.html')


# To edit existing country name
@app.route('/country/<int:country_id>/edit/', methods=['GET', 'POST'])
def editCountry(country_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCountry = session.query(Country).filter_by(id=country_id).one()
    creater_id = getUserInfo(editedCountry.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot edit this country"
              "this belongs to %s" % (creater_id.name))
        return redirect(url_for('showCountry'))
    if request.method == 'POST':
        if request.form['name']:
            editedCountry.name = request.form['name']
            flash("Country Successfully Edited %s" % (editedCountry.name))
            return redirect(url_for('showCountry'))
    else:
        return render_template('editCountry.html', country=editedCountry)


# To Delete existing country
@app.route('/country/<int:country_id>/delete/', methods=['GET', 'POST'])
def deleteCountry(country_id):
    if 'username' not in login_session:
        return redirect('/login')
    countryToDelete = session.query(Country).filter_by(id=country_id).one()
    creater_id = getUserInfo(countryToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot delete this country"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showCountry'))
    if request.method == 'POST':
        session.delete(countryToDelete)
        flash("Successfully Deleted %s" % (countryToDelete.name))
        session.commit()
        return redirect(url_for('showCountry', country_id=country_id))
    else:
        return render_template('deleteCountry.html', country=countryToDelete)


# It Shows Total State list of a country
@app.route('/country/<int:country_id>/states/')
def showStates(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    state = session.query(State).filter_by(state_id=country_id).all()
    return render_template('main.html', country=country, state=state)


# Creating New State
@app.route('/country/<int:country_id>/new/', methods=['GET', 'POST'])
def newStateList(state_id):
    if 'username' not in login_session:
        return redirect('login')
    country = session.query(Country).filter_by(id=state_id).one()
    creater_id = getUserInfo(country.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot add this state"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showCountry', country_id=state_id))
    if request.method == 'POST':
        newList = State(
            name=request.form['name'],
            about=request.form['about'],
            State_capital=request.form['State_capital'],
            State_culture=request.form['State_culture'],
            State_population=request.form['State_population'],
            State_language=request.form['State_language'],
            State_area=request.form['State_area'],
            districts=request.form['districts'],
            state_id=state_id,
            user_id=login_session['user_id']
            )
        session.add(newList)
        session.commit()
        flash("New State List %s is created" % (newList))
        return redirect(url_for('showStates', country_id=state_id))
    else:
        return render_template('newstate.html', state_id=state_id)


# Editing to particular country - state
@app.route('/country/<int:country_id>/<int:b_id>/edit/',
           methods=['GET', 'POST'])
def editStateList(country_id, b_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedList = session.query(State).filter_by(id=b_id).one()
    country = session.query(Country).filter_by(id=country_id).one()
    creater_id = getUserInfo(editedList.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot edit this country"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showStatees', country_id=country_id))
    if request.method == 'POST':
        editedList.name = request.form['name']
        editedList.about = request.form['about']
        editedList.class_strength = request.form['class_strength']
        editedList.labs = request.form['labs']
        editedList.faculties = request.form['faculties']
        editedList.place = request.form['place']
        session.add(editedList)
        session.commit()
        flash("State List has been edited!!")
        return redirect(url_for('showStatees', country_id=country_id))
    else:
        return render_template(
            'editstate.html',
            country=country, state=editedList
            )


# Deleting particular country of state
@app.route('/country/<int:state_id>/<int:list_id>/delete/',
           methods=['GET', 'POST'])
def deleteStateList(state_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    country = session.query(Country).filter_by(id=state_id).one()
    listToDelete = session.query(State).filter_by(id=list_id).one()
    creater_id = getUserInfo(listToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot edit this country"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showStatees', country_id=state_id))
    if request.method == 'POST':
        session.delete(listToDelete)
        session.commit()
        flash("State list has been Deleted!!!")
        return redirect(url_for('showStatees', country_id=state_id))
    else:
        return render_template('deletestate.html', lists=listToDelete)


# Logout from application
@app.route('/disconnect')
def logout():
    access_token = login_session['access_token']
    print("In gdisconnect access_token is %s", access_token)
    print("User name is:")
    print(login_session['username'])

    if access_token is None:
        print("Access Token is None")
        response = make_response(
            json.dumps('Current user not connected.'),
            401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(uri=url, method='POST', body=None,
                       headers={'Content-Type':
                                'application/x-www-form-urlencoded'})[0]
    print(result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out")
        return redirect(url_for('showStatees'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
