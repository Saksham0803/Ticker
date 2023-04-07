from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class RegisteredUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    pas = db.Column(db.String(100))
    name = db.Column(db.String(100))
    #is_theatre_admin = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)
    theater = db.relationship('Theaters')
    movie = db.relationship('Movie')
    show = db.relationship('Show')
    booked_ti = db.relationship('Ticket')

class Theaters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    #location = db.Column(db.String(150))
    #city =  db.Column(db.String(150))
    #contact_no = db.Column(db.String(10))
    theater_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    show = db.relationship('Show')
    booked_ti = db.relationship('Ticket')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String(255))
    title = db.Column(db.String(100))
    #starring = db.Column(db.String(250))
    #production_house = db.Column(db.String(150))
    times_watched = db.Column(db.Integer)
    movie_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    show = db.relationship('Show')
    booked_ti = db.relationship('Ticket')
    rating = db.Column(db.Float)
    Genre = db.Column(db.String(100))

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screened_m = db.Column(db.Integer, db.ForeignKey('movie.id'))
    t_in = db.Column(db.Integer, db.ForeignKey('theaters.id'))
    movie = db.Column(db.String(100))
    t = db.Column(db.String(100))
    address_t = db.Column(db.String(100))
    #theater_address_link = db.Column(db.String(150))
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    t_admin_id = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    available_seats = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    booked_ti = db.relationship('Ticket')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booked_show = db.Column(db.Integer, db.ForeignKey('show.id'))
    booked_m = db.Column(db.Integer, db.ForeignKey('movie.id'))
    booked_t = db.Column(db.Integer, db.ForeignKey('theaters.id'))
    user = db.Column(db.Integer, db.ForeignKey('registered_user.id'))
    movie = db.Column(db.String(100))
    t = db.Column(db.String(100))
    address_t = db.Column(db.String(100))
    #theater_address_link = db.Column(db.String(150))
    total_seats = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    timinig_s = db.Column(db.DateTime(timezone=True), default=func.now())

