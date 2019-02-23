# 建立实例
from flask import Flask
# 建立数据库
from flask_sqlalchemy import SQLAlchemy
# 配置信息
from flask_script import Manager
# 数据库迁移
from flask_migrate import Migrate
# 管理用户登录
from flask_login import LoginManager
# 发送邮件
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = "jinritoutiao"
app.debug = True

app.config.from_pyfile('config.py', silent=True)

# 建立数据库实例 
db = SQLAlchemy(app)

# 让flask-migrate能查询到数据库变化
from app import models

# 数据库迁移实例
migrate = Migrate(app, db)

# 管理用户实例
login_manager = LoginManager(app)

manager = Manager(app)

# 邮件实例
mail = Mail(app)

from . import views