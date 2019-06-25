from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

import json #Added for JSON validation.




app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ColmCleryCS",
    password="new_password",
    hostname="ColmCleryCS.mysql.pythonanywhere-services.com",
    databasename="ColmCleryCS$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'dev key'#os.environ.get('SECRET_KEY') or 'you-will-never-guess'
db = SQLAlchemy(app)
migrate = Migrate(app, db)




class Countries(db.Model):

    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    population = db.Column(db.Integer)
    capital = db.Column(db.String(128))


    def get_name(self):
        return self.name

    def get_population(self):
        return self.population

    def get_capital(self):
        return self.capital


class CountryForm(FlaskForm):
    name = StringField('Country Name', validators=[DataRequired()])
    capital = StringField('Country Capital', validators=[DataRequired()])
    population =IntegerField('Population', validators=[DataRequired()])
    submit = SubmitField('Add Country')


@app.route('/new_country',methods = ['POST', 'GET'])
@app.route('/',methods = ['POST', 'GET'])
def new_country():
    form = CountryForm()
    if form.validate_on_submit():
        new_country = Countries(name=form.country.data,population=form.population.data,capital=form.capital.data)
        db.session.add(new_country)
        db.session.commit()
        return redirect(url_for('countries'))
    return render_template('add_country.html',form=form)

@app.route('/countries')
def countries():
    countries_details=Countries.query.all()
    date=datetime.now()
    return render_template('countries.html', title='Proposals', countries=countries_details)




@app.route('/country_change',methods=['GET', 'POST'])
def handle_country_change():
    if request.method == 'POST':
        data = json.loads(request.data)
        country = Countries.query.filter_by(name=(data['country'])).first()
        if country == None:
            return json.dumps({'country_status':"OK"});
        else:
            return json.dumps({'country_status':'The country has already been registered'});


if __name__ == '__main__':
   app.run(debug = True)


if __name__ == '__main__':
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run()