from app import app, login_manager, db, mail
from .models import Wei_pit, Pit, Attention, ColleArticle
from .models import Comment, Wei_article, Article, User
from .models import Good, User_pit, Report_AR, Report_USER
from flask import jsonify, request, current_app, session, make_response
from flask import redirect, url_for
import pdb
from show_weather import get_weather, get_weather_page
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_
import shortuuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from flask_mail import Message
import os
# import json


# 图片配置
ARTICLE_PIT_PATH = '/home/liyongli/下载/今日头条/app/templates/article_pit/'
USER_PIT_PATH = '/home/liyongli/下载/今日头条/app/templates/user_pit/'
COMMENT_PIT_PATH = '/home/liyongli/下载/今日头条/app/templates/comment_pit/'
WEIARTICLE_PIT_PATH = '/home/liyongli/下载/今日头条/app/templates/weiarticle_pit/'


# 跨域请求
@app.after_request
def af_request(resp):
    """
    # 请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


# 生成令牌函数(未写)
def generate_token(user, opration, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': opration}
    data.update(**kwargs)
    return s.dumps(data)


# 发送邮件
def send_email(email):
    msg = Message('欢迎注册', recipients=[email])
    verification = shortuuid.uuid(pad_length=5)
    msg.body = '密码是' + str(verification)
    mail.send(msg)
    return verification


# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


# 返回左侧菜单栏类型
@app.route('/getType', methods=['GET'])
def return_type():
    # pdb.set_trace()
    list1 = ['推荐', '热点', '科技', '娱乐', '游戏', '体育', '汽车', '财经', '搞笑',
             '军事', '国际', '旅游', '历史', '养生', '美文', '探索', '育儿', '其他']
    list2 = ['recomment', 'hot', 'tech', 'entertainment', 'game', 'sports', 'car', 'finance', 'funny',
             'military', 'world', 'travel', 'hisroty', 'regimen', 'essay', 'discover', 'baby', 'other']
    dict1 = dict(zip(list1, list2))
    # a = json.dumps(dict1, ensure_ascii=False)
    return jsonify(dict1)


# 返回天气信息
@app.route('/getWeather', methods=['POST'])
def return_weather():
    city = request.json['city']
    if city == "":
        city = "重庆"
    page = get_weather_page(city)
    weather = get_weather(page)
    return weather


# 用户登录
@app.route('/userSignIn', methods=['POST'])
def SignIn():
    if current_user.id is not None:
        return redirect(url_for('homepage'))
    email = request.json['email']
    passwd = request.json['passwd']
    if email == "" or passwd == "":
        email = request.cookies.get('email')
        passwd = request.cookies.get('passwd')
    # pdb.set_trace()
    the_user = User.query.filter(User.email == email).first()
    if the_user is None:
        return jsonify({'static': '0'})
    if passwd != the_user.password:
        return jsonify({'static': '2'})
    if passwd == the_user.password:
        login_user(the_user, remember=True)
        resp = make_response(jsonify(the_user.UserInfo()))
        outdate = datetime.datetime.today() + datetime.timedelta(days=30)
        resp.set_cookie('email', email, expires=outdate)
        resp.set_cookie('passwd', passwd, expires=outdate)
        return resp
        # return jsonify(the_user.UserInfo())


# 用户登出
@app.route('/userLoginOut', methods=['GET'])
@login_required
def LoginOut():
    id = request.args.get('id')
    if id is None or id != current_user.id:
        return jsonify({'static': '0'})
    the_user = User.query.filter(User.id == id).first()
    if the_user is None:
        return jsonify({'static': '0'})
    logout_user()
    return jsonify({'static': '1'})


# 注册用户
@app.route('/registered', methods=['GET', 'POST'])
def registered():
    username = request.json['username']
    email = request.json['email']
    passwd = request.json['passwd']
    repasswd = request.json['repasswd']
    verification = request.json['ver']
    if verification != session['verdifacation']:
        return jsonify({"static": "0"})
    if User.query.filter(User.username == username).first() is not None or username == "":
        return jsonify({"static": "1"})
    if User.query.filter(User.email == email).first() is not None or email == "" or email != session['email']:
        return jsonify({"static": "2"})
    if passwd != repasswd or passwd == "" or repasswd == "":
        return jsonify({"static": "3"})
    new_user = User(username=username, password=passwd, email=email)
    db.session.add(new_user)
    db.session.commit()
    session.pop('email', None)
    session.pop('verdifacation', None)
    return jsonify({"static": "4"})


# 向邮箱发送验证码
@app.route('/ensureEmail', methods=['GET', 'POST'])
def ensureEmail():
    email = request.json['email']
    if User.query.filter(User.email == email).first() is not None or email == "":
        return jsonify({"static": "0"})
    verdifacation = send_email(email)
    session['email'] = email
    session['verdifacation'] = verdifacation
    return jsonify({"ver": verdifacation, "email": email})


# 更改用户名
@app.route('/ChangeUsername', methods=['GET', 'POST'])
@login_required
def change_name():
    id = request.json['id']
    rename = request.json['rename']
    # pdb.set_trace()
    if id == "":
        return jsonify({'static': '0'})
    the_user = User.query.filter(User.id == id).first()
    if the_user is None or rename == "":
        return jsonify({'static': '0'})
    the_user.username = rename
    db.session.commit()
    return jsonify({'static': '1'})


# 用户主页信息
@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    id = request.json['id']
    the_user = User.query.filter(User.id == id).first()
    if the_user is None:
        return jsonify({"static": "0"})
    return jsonify(the_user.UserInfo())


# 关注用户
@app.route('/userAttention', methods=['GET', 'POST'])
@login_required
def userAttention():
    # pdb.set_trace()
    id = request.json['id']
    # 关注的用户
    the_user = User.query.filter(User.id == id).first()
    # 已关注，未关注，没有此用户 , 自己
    if the_user is None or id == current_user.id:
        return jsonify({"static": "0"})
    to_follow_userId = current_user.id
    # 是否关注了此用户
    has_follow_user = Attention.query.filter(
        and_(Attention.user_id == to_follow_userId, Attention.attention_id == id)).first()
    if has_follow_user is None:
        new_follow = Attention(user_id=to_follow_userId, attention_id=id)
        db.session.add(new_follow)
        to_follow_user = User.query.filter(User.id == current_user.id).first()
        to_follow_user.attention = to_follow_user.attention + 1
        the_user.fans = the_user.fans + 1
        db.session.commit()
        return jsonify({"static": "1"})
    else:
        return jsonify({"static": "2"})


# 取消关注
@app.route('/notAttention', methods=['GET', 'POST'])
def notAttention():
    # pdb.set_trace()
    id = request.json['id']
    # 关注的用户
    the_user = User.query.filter(User.id == id).first()
    # 已关注，未关注，没有此用户 , 自己
    if the_user is None or id == current_user.id:
        return jsonify({"static": "0"})
    to_follow_userId = current_user.id
    # 是否关注了此用户
    has_follow_user = Attention.query.filter(
        and_(Attention.user_id == to_follow_userId, Attention.attention_id
             == id)).first()
    if has_follow_user is not None:
        db.session.delete(has_follow_user)
        to_follow_user = User.query.filter(User.id == current_user.id).first()
        to_follow_user.attention = to_follow_user.attention - 1
        the_user.fans = the_user.fans - 1
        db.session.commit()
        return jsonify({"static": "1"})
    else:
        return jsonify({"static": "2"})


# 关注的用户列表
@app.route('/getAttentions', methods=['GET', 'POST'])
def getAttentions():
    # pdb.set_trace()
    the_id = request.json['id']
    page = request.json['page']
    if page == "":
        page = 1
    if the_id == "":
        the_id = current_user.id
        if the_id is None:
            return jsonify({"static": "0"})
    attention_list = Attention.query.filter(
        and_(Attention.user_id == the_id)).all()
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            user = attention_list[(int(page)-1)*20 + i]
            # the_json = user.User.UserInfo()
            the_json = user.user2.UserInfo()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 粉丝列表
@app.route('/getFans', methods=['GET', 'POST'])
def getFans():
    the_id = request.json['id']
    page = request.json['page']
    if page is None:
        page = 1
    if the_id is None:
        the_id = current_user.id
    attention_list = Attention.query.filter(
        and_(Attention.attention_id == the_id)).all()
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            user = attention_list[(int(page)-1)*20 + i]
            # the_json = user.User.UserInfo()
            the_json = user.user1.UserInfo()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 发表/修改文章
@app.route('/PublishArticle', methods=['GET', 'POST'])
@login_required
def PublishArticle():
    # pdb.set_trace()
    # 把uuid当成文章id
    uuid = request.json['uuid']
    content = request.json['content']
    user_id = request.json['id']
    title = request.json['title']
    article_id = shortuuid.uuid(pad_length=20)
    the_user = User.query.filter(User.id == user_id).first()
    if the_user is None or content == "":
        return jsonify({"static": "0"})
    if uuid == "":
        new_article = Article(uuid=article_id, title=title, content=content,
                              author_id=user_id)
        db.session.add(new_article)
        db.session.commit()
        return jsonify({"static": "1"})
    else:
        the_article = Article.query.filter(Article.uuid == uuid).first()
        if the_article is not None:
            the_article.title = title
            the_article.content = content
            db.session.commit()
            return jsonify({"static": "2"})
        return jsonify({"static": "3"})


# 获取微头条列表
@app.route('/GetWeiArList', methods=['GET', 'POST'])
def GetWeiArList():
    the_id = request.json['id']
    page = request.json['page']
    if page == "":
        page = 1
    if the_id is None:
        the_id = current_user.id
    weiArList = Wei_article.query.filter(Wei_article.author_id == the_id).all()
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            weiAr = weiArList[(int(page)-1)*20 + i]
            the_json = weiAr.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 删除评论 未测试
@app.route('/deleteComment', methods=['GET', 'POST'])
@login_required
def deleteComment():
    # user_id = request.json['user_id']
    cid = request.json['cid']
    # article_id = request.json['article_id']
    comment = Comment.query.filter(Comment.cid == cid).first()
    if comment is None:
        return jsonify({"static": "0"})
    db.session.delete(comment)
    db.session.commit()
    # 它评论其他评论
    if comment.is_toPerson is not None:
        one_comment = Comment.query.filter(Comment.uuid ==
                                           comment.is_toPerson).first()
        one_comment.reply_sum = one_comment.reply_sum-1
    # 评论它的评论
    comments = Comment.query.filter(Comment.is_toPerson == cid).all()
    if comments is not None:
        for i in range(0, len(comments)):
            comments[i].is_toPerson = ""
        db.session.commit()
    comment.article.comment = comment.article.comment-1
    return jsonify({"static": "1"})


# 发布/修改微头条
@app.route('/PublicWei', methods=['GET', 'POST'])
@login_required
def PublicWei():
    # pdb.set_trace()
    uuid = request.json['uuid']
    content = request.json['content']
    user_id = request.json['id']
    # 图片处理商议
    article_id = shortuuid.uuid(pad_length=20)
    the_user = User.query.filter(User.id == user_id).first()
    if the_user is None or content == "":
        return jsonify({"static": "0"})
    if uuid == "":
        new_article = Wei_article(uuid=article_id, content=content,
                                  author_id=user_id)
        db.session.add(new_article)
        db.session.commit()
        return jsonify({"static": "1"})
    else:
        the_article = Wei_article.query.filter(Wei_article.uuid ==
                                               uuid).first()
        if the_article is None:
            return jsonify({"static": "3"})
        the_article.content = content
        db.session.commit()
        return jsonify({"static": "2"})


# 删除微头条
@app.route('/deleteWei', methods=['GET', 'POST'])
@login_required
def deleteWei():
    # pdb.set_trace()
    id = request.json['id']
    uuid = request.json['uuid']
    if id != str(current_user.id):
        return jsonify({"static": "0"})
    if uuid == "":
        return jsonify({"static": "1"})
    the_wei = Wei_article.query.filter(Wei_article.uuid == uuid).first()
    if the_wei is None:
        return jsonify({"static": "2"})
    comments = Comment.query.filter(Comment.article_uuid == uuid).all()
    if comments is not None:
        for i in range(0, len(comments)):
            db.session.delete(comments[i])
        db.session.commit()
    db.session.delete(the_wei)
    db.session.commit()
    return jsonify({"static": "3"})


# 收藏文章列表(未测试)
@app.route('/likeAr_list', methods=['GET', 'POST'])
@login_required
def likeAr_list():
    id = request.json['id']
    page = request.json['page']
    if id != str(current_user.id):
        return jsonify({"static": "0"})
    Ar_list = ColleArticle.query.filter(
        and_(ColleArticle.user_id == id)).all()
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            Ar = Ar_list[(int(page)-1)*20 + i]
            the_colle_time = Ar.colle_time
            ar_uuid = Ar.article_uuid
            the_article = Article.query.filter(Article.uuid == ar_uuid).first()
            the_json = the_article.Info()
            the_json["colle_time"] = the_colle_time
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 搜索文章
@app.route('/relateAr', methods=['GET', 'POST'])
def relateAr():
    content = request.json['content']
    page = request.json['page']
    if page == "":
        page = "1"
    if content == "":
        return jsonify({"static": "0"})
    the_article = Article.query.filter(
        Article.title.like('%'+content+'%')).all()
    if the_article is None:
        return jsonify({"static": "1"})
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            article = the_article[(int(page)-1)*20 + i]
            the_json = article.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 搜索用户
@app.route('/relateUser', methods=['GET', 'POST'])
def relateUser():
    content = request.json['content']
    page = request.json['page']
    if page == "":
        page = "1"
    if content == "":
        return jsonify({"static": "0"})
    the_user = User.query.filter(User.username.like('%'+content+'%')).all()
    if the_user is None:
        return jsonify({"static": "1"})
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            user = the_user[(int(page)-1)*20 + i]
            the_json = user.UserInfo()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 首页文章(机器学习)
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return 'haha'

# 热闻
@app.route('/hot_news', methods=['GET', 'POST'])
def hot_news():
    page = request.json['page']
    if page == "":
        page = 1
    otherArticles = Article.query.order_by(Article.read_sum.desc()).paginate(
        page=int(page), per_page=20, error_out=False)
    # pdb.set_trace()
    if otherArticles is None:
        return jsonify({"static": "0"})
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            article = otherArticles.items[i]
            the_json = article.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 推荐文章(机器学习)


# 其他文章
@app.route('/OtherArticle', methods=['GET', 'POST'])
def OtherArticle():
    page = request.json['page']
    if page == "":
        page = 1
    otherArticles = Article.query.order_by(Article.updateTime.desc()).paginate(
        page=int(page), per_page=20, error_out=False)
    # pdb.set_trace()
    if otherArticles is None:
        return jsonify({"static": "0"})
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            article = otherArticles.items[i]
            the_json = article.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 收藏文章
@app.route('/CollectArticles', methods=['GET', 'POST'])
@login_required
def ColleArticles():
    uuid = request.json['uuid']
    id = request.json['id']
    if uuid == "":
        return jsonify({"static": "0"})
    if id != str(current_user.id):
        return jsonify({"static": "1"})
    if Article.query.filter(Article.uuid == uuid).first() is None:
        return jsonify({"static": "2"})
    to_collect = ColleArticle(user_id=id, article_uuid=uuid)
    db.session.add(to_collect)
    db.session.commit()
    return jsonify({"static": "3"})


# 取消收藏
@app.route('/DeleteCollectArticles', methods=['GET', 'POST'])
@login_required
def DeleteCollectArticles():
    uuid = request.json['uuid']
    id = request.json['id']
    if uuid == "":
        return jsonify({"static": "0"})
    if id != str(current_user.id):
        return jsonify({"static": "1"})
    the_collect = ColleArticle.query.filter(and_(ColleArticle.article_uuid
                                                 == uuid, ColleArticle.user_id
                                                 == id)).first()
    if the_collect is None:
        return jsonify({"static": "2"})
    db.session.delete(the_collect)
    db.session.commit()
    return jsonify({"static": "3"})


# 文章详情
@app.route('/show_article', methods=['GET', 'POST'])
def show_article():
    uuid = request.json['uuid']
    if uuid == "":
        return jsonify({"static": "0"})
    article = Article.query.filter(Article.uuid == uuid).first()
    if article is None:
        return jsonify({"static": "1"})
    return jsonify(article.Info())


# 获取评论
@app.route('/get_comment', methods=['GET', 'POST'])
def get_comment():
    uuid = request.json['uuid']
    page = request.json['page']
    if page == "":
        page = 1
    if uuid == "":
        return jsonify({"static": "0"})
    if Article.query.filter(Article.uuid == uuid).first() is None:
        return jsonify({"static": "1"})
    comment_list = Comment.query.filter(and_(Comment.article_uuid == uuid,
                                             Comment.is_toPerson == "")).order_by(
        Comment.CommentTime.desc()).paginate(
        page=int(page), per_page=20,
        error_out=False).items
    l0 = list()
    # 每页返回20
    for i in range(0, 20):
        try:
            comment = comment_list[i]
            the_json = comment.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 发表评论/回复
@app.route('/public_comment', methods=['GET', 'POST'])
@login_required
def public_comment():
    user_id = request.json['id']
    uuid = request.json['uuid']
    content = request.json['content']
    is_toPerson = request.json['is_toPerson']
    if user_id == "" or int(user_id) != current_user.id:
        return jsonify({"static": "0"})
    if uuid == "":
        return jsonify({"static": "1"})
    if Article.query.filter(Article.uuid == uuid).first() is None:
        return jsonify({"static": "2"})
    if is_toPerson != "" and Comment.query.filter(Comment.cid ==
                                                  is_toPerson).first() is None:
        return jsonify({"static": "3"})
    if content == "":
        return jsonify({"static": "4"})
    cid = shortuuid.uuid(pad_length=20)
    comment = Comment(cid=cid, article_uuid=uuid, user_id=current_user.id,
                      comment=content, is_toPerson=is_toPerson,
                      CommentTime=datetime.date.today())
    db.session.add(comment)
    db.session.commit()
    if is_toPerson != "":
        the_comment = Comment.query.filter(Comment.cid == is_toPerson).first()
        the_comment.reply_sum = the_comment.reply_sum + 1
        db.session.commit()
    return jsonify({"static": "5"})


# 查看回复
@app.route('/show_reply', methods=['GET', 'POST'])
def show_reply():
    # pdb.set_trace()
    article_id = request.json['article_id']
    cid = request.json['cid']
    if article_id == "" or cid == "":
        return jsonify({"static": "0"})
    if Comment.query.filter(and_(Comment.cid == cid,
                                 Comment.article_uuid ==
                                 article_id)).first() is None:
        return jsonify({"static": "1"})
    # 回复排序
    the_comment_list = Comment.query.filter(Comment.is_toPerson ==
                                            cid).order_by(
        Comment.CommentTime.desc()).all()
    l0 = list()
    # 每页返回20
    for i in range(0, len(the_comment_list)):
        try:
            comment = the_comment_list[i]
            the_json = comment.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 点赞
@app.route('/give_good', methods=['GET', 'POST'])
@login_required
def give_good():
    user_id = request.json['user_id']
    comment_id = request.json['cid']
    article_uuid = request.json['article_uuid']
    if int(user_id) != current_user.id:
        return jsonify({"static": "0"})
    if Comment.query.filter(Comment.cid == comment_id).first() is None or Good.query.filter(and_(Good.user_id == int(user_id), Good.comment_cid == comment_id)).first() is not None:
        return jsonify({"static": "1"})
    the_good = Good(user_id=user_id, comment_cid=comment_id,
                    article_uuid=article_uuid)
    db.session.add(the_good)
    the_comment = Comment.query.filter(Comment.cid == comment_id).first()
    the_comment.good_sum = the_comment.good_sum + 1
    db.session.commit()
    return jsonify({"static": "2"})


# 取消点赞
@app.route('/delete_good', methods=['GET', 'POST'])
@login_required
def delete_good():
    user_id = request.json['user_id']
    comment_id = request.json['cid']
    if int(user_id) != current_user.id:
        return jsonify({"static": "0"})
    if Comment.query.filter(Comment.cid == comment_id).first() is None or Good.query.filter(and_(Good.user_id == int(user_id), Good.comment_cid == comment_id)).first() is None:
        return jsonify({"static": "1"})
    the_good = Good.query.filter(and_(Good.user_id == user_id,
                                      Good.comment_cid == comment_id)).first()
    db.session.delete(the_good)
    db.session.commit()
    the_comment = Comment.query.filter(Comment.cid == comment_id).first()
    the_comment.good_sum = the_comment.good_sum - 1
    db.session.commit()
    return jsonify({"static": "2"})


# 查看点赞状态
@app.route('/is_alreadyGood', methods=['GET', 'POST'])
@login_required
def is_alreadyGood():
    user_id = int(request.json['user_id'])
    article_uuid = request.json['article_uuid']
    if user_id != current_user.id:
        return jsonify({"static": "0"})
    if Article.query.filter(Article.uuid == article_uuid).first() is None:
        return jsonify({"static": "1"})
    where_good = Good.query.filter(and_(Good.article_uuid == article_uuid,
                                        Good.user_id == user_id)).all()
    # pdb.set_trace()
    if where_good is None:
        return jsonify({"static": "2"})
    l0 = list()
    for i in range(0, len(where_good)):
        try:
            good = where_good[i]
            the_json = good.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 上传图片(统一)
@app.route('/Photo/<string:pitFrom>', methods=['POST'])
def essayPhoto(pitFrom):
    # pdb.set_trace()
    img = request.files.get('img')    # 获取上传的文件
    uuid = request.form['uuid']

    if img is None:
        return jsonify({"static": "0"})

    if pitFrom == "":
        return jsonify({"static": "1"})
    pitName = img.filename
    if uuid == "":
        return jsonify({"static": "2"})
    filename = str(shortuuid.uuid(pad_length=20)) + pitName

    UPLOAD_FOLDER = os.path.join('/home/liyongli/下载/今日头条/app/templates/',
                                 '%s/%s' % (pitFrom, pitName))
    file_path = UPLOAD_FOLDER+filename

    try:
        img.save(file_path)
    except FileNotFoundError:
        print("没有此路径")
        return jsonify({"static": "3"})

    if pitFrom == "article_pit":
        the_pit = Pit(pit_name=filename, article_uuid=uuid, pit_uri=file_path)
    if pitFrom == "user_pit":
        the_pit = User_pit(pit_name=filename, user_id=uuid, pit_uri=file_path)
    if pitFrom == "weiarticle_pit":
        the_pit = Wei_pit(pit_name=filename, article_uuid=uuid,
                          pit_uri=file_path)
    db.session.add(the_pit)
    db.session.commit()

    return jsonify({'static': "5", 'src': file_path, 'filename': filename})


# 获取图片信息
@app.route('/Photo', methods=['GET', 'POST'])
def Photo():
    pitFrom = request.json['pitFrom']
    uuid = request.json['uuid']
    the_list = list()

    if pitFrom == "" or uuid == "":
        return jsonify({"static": "0"})
    if pitFrom == "article_pit":
        if Article.query.filter(Article.uuid == uuid).first() is None:
            return jsonify({"static": "1"})
        the_list = Pit.query.filter(Pit.article_uuid == uuid).all()
    if pitFrom == "user_pit":
        if User.query.filter(User.id == uuid).first() is None:
            return jsonify({"static": "2"})
        the_list = User_pit.query.filter(User_pit.user_id == uuid).all()
    if pitFrom == "weiarticle_pit":
        if Wei_article.query.filter(Wei_article.uuid == uuid).first() is None:
            return jsonify({"static": "3"})
        the_list = Wei_pit.query.filter(Wei_pit.article_uuid == uuid).all()
    l0 = list()
    for i in range(0, len(the_list)):
        try:
            pit = the_list[i]
            the_json = pit.Info()
            l0.append(the_json)
        except IndexError:
            print('')
    return jsonify({'data': l0})


# 获取图片
@app.route('/GetPhoto', methods=['GET', 'POST'])
def GetPhoto():
    pitFrom = request.json['pitFrom']
    pit_uri = request.json['pit_uri']

    if pitFrom == "" or pit_uri == "":
        return jsonify({"static": "0"})
    try:
        image_data = open(str(pit_uri), "rb").read()
    except FileNotFoundError:
        print("没有此图片")
        return jsonify({"static": "1"})
    response = make_response(image_data)
    response.headers['Content-Type'] = 'file'
    return response


# 举报文章
@app.route('/report_article', methods=['GET', 'POST'])
@login_required
def report_article():
    user_id = str(request.json['user_id'])
    article_uuid = request.json['article_uuid']
    reason_id = request.json['reason_id']
    if user_id == "" or article_uuid == "" or reason_id == "":
        return jsonify({"static": "0"})
    if User.query.filter(User.id == user_id).first() is None:
        return jsonify({"static": "1"})
    if Article.query.filter(Article.uuid == article_uuid).first() is None:
        return jsonify({"static": "2"})
    the_report = Report_AR(user_id=user_id, article_uuid=article_uuid,
                           reason_id=reason_id)
    db.session.add(the_report)
    db.session.commit()
    return jsonify({"static": "3"})


# 举报用户
@app.route('/report_user', methods=['GET', 'POST'])
@login_required
def report_user():
    user_id = request.json['user_id']
    report_id = request.json['report_id']
    reason_id = request.json['reason_id']
    if user_id == "" or report_id == "" or reason_id == "":
        return jsonify({"static": "0"})
    if User.query.filter(User.id == user_id).first() is None:
        return jsonify({"static": "1"})
    if User.query.filter(User.id == report_id).first() is None:
        return jsonify({"static": "2"})
    the_report = Report_USER(user_id=user_id, report_id=report_id,
                             reason_id=reason_id)
    db.session.add(the_report)
    db.session.commit()
    return jsonify({"static": "3"})


# 给所有文章添加uuid
def uuid_get():
    ar = Article.query.all()
    for i in range(0, len(ar)):
        i1 = str(i)
        ar[i].uuid = i1
        db.session.commit()
