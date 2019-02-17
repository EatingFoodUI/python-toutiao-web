from app import app, login_manager, db
from .models import Wei_pit, Pit, Attention, ColleArticle
from .models import Comment, Wei_article, Article, User
from flask import jsonify, request
import pdb
from show_weather import get_weather, get_weather_page
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_
# import json


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
        return jsonify({'static': '-1'})
    if passwd != the_user.password:
        return jsonify({'static': '0'})
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
        return jsonify({"static": "0"})


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
        return jsonify({"static": "0"})


# 关注用户列表
@app.route('/getAttentions', methods=['GET', 'POST'])
def getAttentions():
    pdb.set_trace()
    the_id = request.json['id']
    page = request.json['page']
    if page is None:
        page = 1
    if the_id is None:
        the_id = current_user.id
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


# 发表文章

# 获取微头条列表

# 获取评论列表

# 删除评论

# 收藏文章列表

# 搜索文章

# 搜索用户

# 首页文章

# 热闻

# 推荐文章

# ----------------------------------------------------------

# 其他文章

# 收藏文章

# 取消收藏

# 举报文章

# 文章详情

# 获取评论

# 发表评论

# 发表回复

# 查看回复

# 点赞

# 取消点赞

# 举报用户

# 注册

# 验证

