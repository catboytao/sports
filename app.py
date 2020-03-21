import logging

from flask import Flask, jsonify,abort,request,g,url_for
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# 输出时间
from spider.crawler import Crawler
from spider.load_data import Loader
from factory import create_app
from models.model import User,Sports
from utils.core import db
app = create_app(config_name="PRODUCTION")
app.app_context().push()
auth = HTTPBasicAuth()
db.create_all()
# celery -A app:celery_app worker -l info -P gevent


logging.basicConfig(
    level=logging.INFO,
    filename="logs/log.txt",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    html = Crawler.get_html()
    data = Crawler.parse_html(html)
    loader.insert_data(data)


@app.route('/')
def hello_world():
    return 'Hello World!'


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token,app)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/add_user/',methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/api/getSports')
@auth.login_required
def get_sports():

    resp = {'data':None,'msg':'Success','code':0}
    try:
        all_data = Sports.query.all()
        data = list(map(Sports.user_to_dict, all_data))
        resp['data'] = data
        resp['count'] = len(data)
    except Exception as e:
        print(e)
        resp['msg'] = 'Fail'
        resp['code'] = -1
    rts = jsonify(resp)
    return rts


#api.add_resource(SportsResource,'/getSports')

if __name__ == '__main__':
    # loader = Loader()
    # #print(len(loader.ids))
    # html = Crawler.get_html()
    # data = Crawler.parse_html(html)
    # loader.insert_data(data)
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=10)
    scheduler.start()
    app.run()
