# encoding=utf8

from . import db
from flask_login import UserMixin
import datetime


# 用户
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # __table_args__ = {'extend_existing': True}
    # ### 设置默认pit_uri,attention,fans,motto
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    pit_uri = db.Column(db.String(200))
    attention = db.Column(db.Integer, default=0)
    fans = db.Column(db.Integer, default=0)
    # 格言
    motto = db.Column(db.String(100), default="no motto")

    # fans = db.relationship('Attention', back_populates="user1")
    # attentions = db.relationship('Attention', back_populates="user2")

    # 传递用户信息 
    def UserInfo(self):
        userinfo = {
            'static': 1,
            'id': self.id,
            'username': self.username,
            'pit_uri': self.pit_uri,
            'attention': self.attention,
            'fans': self.fans,
            'motto': self.motto
        }
        return userinfo

    def __repr__(self):
        return '<User %r>' % self.email


# 文章
class Article(db.Model):
    __tablename__ = 'article'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    title = db.Column(db.String(100), unique=True, default='no title')
    content = db.Column(db.Text)
    types = db.Column(db.String(20), default='其他')
    read_sum = db.Column(db.Integer, default=0)
    comment = db.Column(db.Integer, default=0)
    updateTime = db.Column(db.Date, default=datetime.date.today())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    User = db.relationship('User', backref=db.backref('Article'))

    def Info(self):
        info = {
            'static': 1,
            'uuid': self.uuid,
            'title': self.title,
            'content': self.content,
            'types': self.types,
            'read_sum': self.read_sum,
            'comment': self.comment,
            'updateTime': self.updateTime,
            'author_id': self.author_id
        }
        return info

    def __repr__(self):
        return '<Article %r>' % self.title


# 微头条
class Wei_article(db.Model):
    __tablename__ = 'wei_article'
    # __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100))
    title = db.Column(db.String(100), unique=True, default='no title')
    content = db.Column(db.Text)
    read_sum = db.Column(db.Integer, default=0)
    comment = db.Column(db.Integer, default=0)
    good_sum = db.Column(db.Integer, default=0)
    updateTime = db.Column(db.Date, default=datetime.date.today())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('Wei_article'))

    def Info(self):
        info = {
            'static': 1,
            'id': self.id,
            'title': self.title,
            'read_sum': self.read_sum,
            'good_sum': self.good_sum,
            'updateTime': self.updateTime,
            'author_id': self.author_id
        }
        return info


    def __repr__(self):
        return '<Wei_article %r>' % self.title
    

# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    # __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.String(100))
    article_uuid = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.String(500))
    reply_sum = db.Column(db.Integer, default=0)
    good_sum = db.Column(db.Integer, default=0)
    CommentTime = db.Column(db.Date)

    # 是否是回复别人的评论，是添加回复的评论的id
    is_toPerson = db.Column(db.String(100))

    # article = db.relationship('Article', backref=db.backref('Comment'))
    user = db.relationship('User', backref=db.backref('Comment'))
    
    def Info(self):
        info = {
            'static': 1,
            'cid': self.cid,
            'article_uuid': self.article_uuid,
            'comment': self.comment,
            'reply_sum': self.reply_sum,
            'good_sum': self.good_sum,
            'CommentTime': self.CommentTime
        }
        return info

    def __repr__(self):
        return '<Comment %r>' % self.id


# 收藏文章
class ColleArticle(db.Model):
    __tablename__ = 'collearticle'
    # __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_uuid = db.Column(db.String(100))
    colle_time = db.Column(db.Date, default=datetime.date.today())
    
    # user = db.relationship('User', backref=db.backref('Collearticle'))
    # article = db.relationship('Article', backref=db.backref('Collearticle'))
    
    def __repr__(self):
        return '<ColleArticle %r>' % self.user_id


# 关注用户
class Attention(db.Model):
    __tablename__ = 'attention'
    # __table_args__ = {'extend_existing': True} 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    attention_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # user1 = db.relationship('User', back_populates="fans", foreign_keys=user_id)
    # user2 = db.relationship('User', back_populates="attentions", foreign_keys=attention_id)
    user1 = db.relationship('User', foreign_keys=user_id)
    user2 = db.relationship('User', foreign_keys=attention_id)
    # User = db.relationship('User', backref=db.backref('Attention'))

    def __repr__(self):
        return '<Attention %r>' % self.user_id


# 文章图片
class Pit(db.Model):
    __tablename__ = 'pit'
    # __table_args__ = {'extend_existing': True}
     
    pit_id = db.Column(db.Integer, primary_key=True)
    pit_name = db.Column(db.String(100))
    article_uuid = db.Column(db.String(100))
    pit_uri = db.Column(db.String(200))

    # article = db.relationship('Article', backref=db.backref('Pit'))

    def Info(self):
        info = {
            'pit_name': self.pit_name,
            'article_uuid': self.article_uuid,
            'pit_uri': self.pit_uri
        }
        return info


    def __repr__(self):
        return '<Pit %r>' % self.pit_id


# 微头条图片
class Wei_pit(db.Model):
    __tablename__ = 'wei_pit'
    # __table_args__ = {'extend_existing': True} 

    pit_id = db.Column(db.Integer, primary_key=True)
    pit_name = db.Column(db.String(200))
    article_uuid = db.Column(db.String(100))
    pit_uri = db.Column(db.String(200))

    # wei_article = db.relationship('Wei_article', backref=db.backref('Wei_pit'))
    
    def Info(self):
        info = {
            'pit_name': self.pit_name,
            'article_uuid': self.article_uuid,
            'pit_uri': self.pit_uri
        }
        return info

    def __repr__(self):
        return '<Wei_pit %r>' % self.pit_id


# 用户图片
class User_pit(db.Model):
    __tablename__ = 'user_pit'

    pit_id = db.Column(db.Integer, primary_key=True)
    pit_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    pit_uri = db.Column(db.String(200))

    def Info(self):
        info = {
            'pit_name': self.pit_name,
            'user_id': self.user_id,
            'pit_uri': self.pit_uri
        }
        return info

    def __repr__(self):
        return '<User_pit %r>' % self.pit_id


# 天气
class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    Weather_id = db.Column(db.String(10))
    name = db.Column(db.String(10))

    def __repr__(self):
        return '<Weather %r>' % self.id


# 点赞记录
class Good(db.Model):
    __tablename__ = 'good'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    comment_cid = db.Column(db.String(100))
    article_uuid = db.Column(db.String(100))

    def Info(self):
        info = {
            'user_id': self.user_id,
            'comment_cid': self.comment_cid,
            'article_uuid': self.article_uuid
        }
        return info

    def __repr__(self):
        return '<Good %r>' % self.id