from flask import *
from data import db_session
from data.db_session import global_init, create_session
from data.news import News
from data.users import User
from forms.user import RegisterForm
from forms.meal import MealOrder
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)


@app.route("/")
def index():
    global_init("db/news.sqlite")
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/meal", methods=['GET', 'POST'])
def meal():
    data = session.get("data", "!")
    form = MealOrder()
    if form.validate_on_submit():
        form.klass = session["data"].split()[0]
        form.bufet = session["data"].split()[1]
        form.hot_meal = session["data"].split()[2]
        res = make_response(render_template("meal.html", form=form))
        return res
    return render_template('meal.html', title='Заказ питания', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 1))
    res = make_response(render_template("enter_count.html", count=request.cookies.get("visits_count", 0)))
    res.set_cookie("visits_count", str(visits_count + 1),
                   max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
        days=365
    )
    return make_response(render_template("enter_count.html", count=visits_count))


def main():
    app.run()


if __name__ == "__main__":
    main()
