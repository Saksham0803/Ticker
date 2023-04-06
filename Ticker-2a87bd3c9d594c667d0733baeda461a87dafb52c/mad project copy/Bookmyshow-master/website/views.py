from flask import render_template, url_for, request, Blueprint,  redirect, current_app, flash   #jsonify
from .models import Show, Movie, Ticket, Theaters  #RegisteredUser
import secrets
import os
from datetime import datetime
from . import db
from flask_login import current_user, login_required   #login_user,  logout_user


view = Blueprint('views', __name__)


@view.route('/')
def home():
    movie = Movie.query.all()
    show = Show.query.all()

    return render_template('home.html', user=current_user, movie=movie)


@view.route("/search", methods=['POST'])
def search():
    try:
        movie = Movie.query.all()
        print("done", movie[0].title)
        searched = request.form.get("searching")
        print(searched)
        movie_t = []
        for i in range(len(movie)):
            movie_t.append(movie[i].title)
        print(movie_t)
        moviess = []
        index = []
        for j in range(len(movie_t)):
            if searched.lower() in movie_t[j].lower():
                moviess.append(movie[j])
                index.append(j)
        print(moviess)
        print(movie)
        return render_template('home.html', user=current_user, movie=moviess)
    except Exception as e:
        print("No")
        movie = Movie.query.all()
        print(movie)
        return render_template('home.html', user=current_user, movie=movie)


@view.route('/movies')
@login_required
def movies():
    if current_user.is_admin:
        return render_template('movies.html', user=current_user)
    return redirect(url_for('views.home'))


@view.route('/add_movies', methods=['GET', 'POST'])
@login_required
def add_movies():
    if current_user.is_admin:
        if request.method == 'POST':
            title_m = request.form.get('title')
            #starring_m = request.form.get('starring')
            #production_m = request.form.get('production_house')
            no_watched_movie = 0
            #print(type(request.files['poster']))
            poster_m = save_images(request.files['poster'])
            rating = request.form.get('rating')
            genre = request.form.get('Genre')
            # check if all the fields are not empty
            if len(title_m) >= 1:   # and len(starring_m) >= 1 and len(production_m)
                print("movie in process")
                new_movie = Movie(title=title_m, poster=poster_m, times_watched=no_watched_movie, movie_admin_id=current_user.id, rating = rating, Genre = genre)   #   starring=starring_m, production_house=production_m

                db.session.add(new_movie)
                db.session.commit()

                #flash(movie_title + ' is being added', category='success')
                return redirect(url_for('views.movies'))
            else:
                flash('fill all fields', category='error') #Make sure all the fields are filled
                return render_template('add_movies.html', user=current_user)
        else:
            return render_template('add_movies.html', user=current_user)
    return redirect(url_for('views.home'))


@view.route('/update_movies/<int:id>', methods=['POST', 'GET'])
@login_required
def update_movies(id):
    if current_user.is_admin:
        update_m = Movie.query.get(int(id))
        if request.method == 'POST':
            update_m.poster = save_images(request.files['poster'])
            update_m.title = request.form.get('title')
            #update_m.starring = request.form.get('starring')
            #update_m.production_house = request.form.get('production_house')
            
            db.session.commit()

            #flash(movie_to_update.title + ' updated successfully', category='success')
            return redirect(url_for('views.movies'))
        else:
            if update_m:
                return render_template('update_movies.html', user=current_user, movie=update_m)
    else:
        return redirect(url_for('movies.home'))


@view.route('/my_theaters')
@login_required
def my_theaters():
    if current_user.is_admin:
        movie = Movie.query.all()
        return render_template('my_theaters.html', user=current_user, movies=movie)
    return redirect(url_for('views.home'))

@view.route('/select_theaters/<int:id>')
def select_theaters(id):

    show = Show.query.filter_by(screened_m=int(id)).all()
    print(show)
    movie = Movie.query.get(int(id))
    print(movie)
    print("line 90")
    if show:
        return render_template('select_theaters.html', user=current_user, shows=show, movie= movie)
    else:
        flash('There is no show for this movie', category='note')   #This movie has no shows currently
        return redirect(url_for('views.home'))

@view.route('/add_theaters', methods=['GET', 'POST'])
@login_required
def add_theaters():
    if current_user.is_admin:
        if request.method == 'POST':
            name_t = request.form.get('name')
            address_t = request.form.get('address')
            #theater_location = request.form.get('location')
            #theater_city = request.form.get('city')
            #theater_contact_no = request.form.get('contact_no')

            # check if all the fields are not empty
            if len(name_t) >= 1 and len(address_t) >= 1:
                # good to go
                new_t = Theaters(name=name_t, address=address_t, theater_admin_id=current_user.id)
                db.session.add(new_t)
                db.session.commit()
                print('theatre added')
                flash('Your Theater is being added', category='success')
                return redirect(url_for('views.my_theaters'))
            else:
                flash('Fill all the fields', category='error')    #Make sure all the fields are filled
                return render_template('add_theaters.html', user=current_user)
        else:
            return render_template('add_theaters.html', user=current_user)
    return redirect(url_for('views.home'))


@view.route('/update_theatre/<int:id>', methods=['POST', 'GET'])
@login_required
def update_theatre(id):
    if current_user.is_admin:
        update_t = Theaters.query.get(int(id))
        if request.method == 'POST':
            update_t.name = request.form.get('name')
            update_t.address = request.form.get('address')
            # update_m.starring = request.form.get('starring')
            # update_m.production_house = request.form.get('production_house')

            db.session.commit()

            # flash(movie_to_update.title + ' updated successfully', category='success')
            return redirect(url_for('views.my_theaters'))
        else:
            if update_t:
                return render_template('update_theatre.html', user=current_user, theater=update_t)
    else:
        return redirect(url_for('movies.home'))

@view.route('/my_tickets')
@login_required
def my_tickets():
    return render_template('my_tickets.html', user=current_user)

@view.route('/book_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def book_ticket(id):
    if current_user.is_admin == False:
        show = Show.query.get(int(id))
        
        if request.method == 'POST':
            t = Theaters.query.filter_by(name=str(show.t)).first()
            #print(theater.name)
            total_seats = request.form.get('no_of_seats')
            # update the number of seats
            show.available_seats = int(show.available_seats) - int(total_seats)
            # date = str(show.datetime)
            # print(date[0:10])
            new_ticket = Ticket(booked_show=show.id, booked_m=show.screened_m, booked_t=show.t_in, user=current_user.id, movie=show.movie, t=show.t, address_t=show.address_t, total_seats=total_seats, cost=int(show.cost) * int(total_seats), timinig_s=show.datetime)  # theater_address=theater.address, theater_address_link = theater.location,
            
            db.session.add(new_ticket)
            db.session.commit()

            #flash('Your Show is being added', category='success')
            return redirect(url_for('views.my_tickets'))
        else:
            return render_template('book_ticket.html', user=current_user, show=show)
    else:
        return redirect(url_for('views.select_theaters'))

@view.route('/add_shows', methods=['GET', 'POST'])
@login_required
def add_shows():
    print('reached 116')
    movie = Movie.query.all()
    t = Theaters.query.filter_by(theater_admin_id=int(current_user.id)).all()
    print(t)
    if current_user.is_admin:
        print('reached 120')
        if request.method == 'POST':
            print('reached 122')
            screened_m = Movie.query.filter_by(title=request.form.get('movie')).first().id

            if screened_m:
                t_in = int(request.form.get('t_in'))
                print(t_in)
                movie = request.form.get('movie')
                print(movie)
                t = Theaters.query.filter_by(id=request.form.get('t_in')).first()
                date_time = datetime.strptime(request.form.get('date_time'), '%Y-%m-%dT%H:%M')
                available_seats = int(request.form.get('available_seats'))
                print(available_seats)
                cost = request.form.get('cost')
                # rating = request.form.get('rating')
                # genre = request.form.get('Genre')
            else:
                flash('No movie', category='warning')  #Movie doesn\'t exist
                return render_template('add_shows.html', user=current_user, movies=movie, theaters=t)
            print(movie)

            if t_in >= 1 and available_seats >= 1: #movie>=1
                new_s = Show(screened_m=screened_m, t_in=t_in, movie=movie, t=t.name,address_t=t.address, datetime=date_time, t_admin_id=current_user.id, available_seats=available_seats, cost=cost)   #theater_address_link=t.location, , rating=rating, Genre=genre
                print(new_s)
                db.session.add(new_s)
                db.session.commit()
                flash('Your Show is being added', category='success')
                return redirect(url_for('views.my_theaters'))
            else:
                flash('Fill all the fields', category='error')   #Make sure all the fields are filled
                return render_template('add_shows.html', user=current_user, movies=movie, theaters=t)
        else:
            return render_template('add_shows.html', user=current_user, movies=movie)
    else:
        return render_template('home.html', user=current_user, movies=movie)


@view.route('show_tickets/<int:id>')
@login_required
def show_tickets(id):
    if current_user.is_admin:    # == True
        ti = Ticket.query.filter_by(booked_show=int(id)).all()
        show = Show.query.get(int(id))
        return render_template('show_tickets.html', user=current_user, tickets=ti, show=show, ticket_count=len(ti))
    else:
        return render_template('home.html', user=current_user, movies=movies)
        

def save_images(poster):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(poster.filename)
    image_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/movie_posters', image_name)
    poster.save(file_path)
    return image_name

