from app import app, login_manager, db
from .models import Wei_pit, Pit, Attention, ColleArticle
from .models import Comment, Wei_article, Article, User
from flask import jsonify, request, current_app
import pdb
from show_weather import get_weather, get_weather_page
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_
import shortuuid
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
# import json



# 生成令牌函数(未写)
def generate_token(user, opration, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': opration}
    data.update(**kwargs)
    return s.dumps(data)


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
@app.route('/getWeather', methods=['GET', 'POST'])
def return_weather():
    city = request.json['city']
    page = get_weather_page(city)
    weather = get_weather(page)
    return weather


# 用户登录
@app.route('/userSignIn', methods=['GET', 'POST'])
def SignIn():
    email = request.json['email']
    passwd = request.json['passwd']
    # pdb.set_trace()
    the_user = User.query.filter(User.email == email).first()
    if the_user is None:
        return jsonify({'static': '0'})
    if passwd != the_user.password:
        return jsonify({'static': '2'})
    if passwd == the_user.password:
        login_user(the_user, remember=True)
        return jsonify(the_user.UserInfo())


# 用户登出
@app.route('/userLoginOut', methods=['GET'])
@login_required
def LoginOut():
    id = request.args.get('id')
    if id is None:
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
    repasswd = request.json['']
    if User.query.filter(User.username == username).first() is not None:
        return jsonify({"static": "0"})
    if User.query.filter(User.email == email).first() is not None:
        return jsonify({"static": "1"})
    if passwd != repasswd:
        return jsonify({"static": "2"})
    new_user = User(username=username, password=passwd, email=email)  
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"static": "3"})


# 验证邮箱(未写)
@app.route('/ensureEmail', methods=['GET', 'POST'])


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
        and_(Attention.user_id == to_follow_userId, Attention.attention_id == id)).first()
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
    pdb.set_trace()
    the_id = request.json['id']
    page = request.json['page']
    if page == "":
        page = 1
    if the_id == "":
        the_id = current_user.id
        if the_id is None:
            return jsonify({"static":"0"})
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
    uuid = request.json['uuid']
    content = request.json['content']
    user_id = request.json['id']
    title = request.json['title']
    article_id = shortuuid.uuid(pad_length=20)
    the_user = User.query.filter(User.id == user_id).first()
    if the_user is None or content == "":
        return jsonify({"static": "0"})
    if uuid == "":
        new_article = Article(uuid=article_id, title=title, content=content, author_id=user_id)
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
        one_comment = Comment.query.filter(Comment.uuid == comment.is_toPerson).first()
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
        new_article = Wei_article(uuid=article_id, content=content, author_id=user_id)
        db.session.add(new_article)
        db.session.commit()
        return jsonify({"static": "1"})
    else:
        the_article = Wei_article.query.filter(Wei_article.uuid == uuid).first()
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
    the_article = Article.query.filter(Article.title.like('%'+content+'%')).all()
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

# 热闻(机器学习)

# 推荐文章(机器学习)

# 其他文章
@app.route('/OtherArticle', methods=['GET', 'POST'])
def OtherArticle():
    page = request.json['page']
    if page == "":
        page = 1
    otherArticles = Article.query.order_by(Article.updateTime.desc()).paginate(page=int(page), per_page=20, error_out=False)
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
    the_collect = ColleArticle.query.filter(and_(ColleArticle.article_uuid == uuid, ColleArticle.user_id == id)).first()
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
    comment_list = Comment.query.filter(and_(Comment.article_uuid == uuid, Comment.is_toPerson == "")).order_by(Comment.CommentTime.desc()).paginate(page=int(page), per_page=20, error_out=False).items    
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
    if is_toPerson != "" and Comment.query.filter(Comment.cid == is_toPerson).first() is None:
        return jsonify({"static": "3"})
    if content == "":
        return jsonify({"static": "4"})
    cid = shortuuid.uuid(pad_length=20)
    comment = Comment(cid=cid, article_uuid=uuid, user_id=current_user.id, comment=content, is_toPerson=is_toPerson, CommentTime=datetime.date.today())
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
    if Comment.query.filter(and_(Comment.cid == cid, Comment.article_uuid == article_id)).first() is None:
        return jsonify({"static": "1"})
    # 回复排序
    the_comment_list = Comment.query.filter(Comment.is_toPerson == cid).order_by(Comment.CommentTime.desc()).all()
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

# ---------------------------------------

# 点赞

# 取消点赞
# =========================
# 举报文章

# 举报用户


