#!/usr/bin/env bash
# 后台启动Celery
echo "开始启动"
#nohup celery -A app:celery_app worker -f ./logs/celery.log -l INFO &
# 启动FlaskAPP
nohup gunicorn -c ./config/gun.conf app:app &
# windows 下测试
# celery -A run:celery_app worker --pool=solo -l info

# docker run -d --name flask_redis --network appnet --network-alias flask-redis redis
# docker run -d --name flask_mysql --network appnet --network-alias flask-mysql -e MYSQL_ROOT_PASSWORD=199786 mysql
# docker run -it --name flask-restful-example -p 3131:80 --network appnet flask-restful-example sh