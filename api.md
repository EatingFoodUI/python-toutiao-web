# 返回左侧菜单栏类型

### get   /getType

{

list1 = ['推荐', '热点', '科技', '娱乐', '游戏', '体育', '汽车', '财经', '搞笑',

​         '军事', '国际', '旅游', '历史', '养生', '美文', '探索', '育儿', '其他']

list2 = ['recomment', 'hot', 'tech', 'entertainment', 'game', 'sports',   'car', 'finance', 'funny',

​         'military', 'world', 'travel', 'hisroty', 'regimen', 'essay', 'discover', 'baby', 'other']

组成的json数据{ "推荐"："recomment"...}

}

# 返回天气信息

### post   /getWeather

{

"city": ""

}

return  返回信息参考中国天气网

{

'today': { 

​    'temp': , 'wind': , 'weather': }

}

'tomorrow':{

​    'temp': , 'wind': , 'weather': 

} 

'afterTwoDay':{

​    'temp': , 'wind': , 'weather': 

} 

# 用户登录

### post /userSignIn

{

​    "email":"",

​    "passwd": ""

}

return

用户不存在

{

​    "static":"0"

}

密码错误

{

​    "static":"2"

}

成功

{

​    'static': 1,

​    'id': id,

​    'username': username,

​    'pit_uri': pit_uri,

​    'attention': attention,

​    'fans': fans,

​    'motto': motto

}

# 用户登出

### get /userLoginOut?id=""

return 

没有此用户/id为空

{

​    "static":"0"

}

登出成功

{

​    'static': 1,

}

# 注册用户

### post /registered

{

​    "username":"",

​    "email":"",

​    "passwd":""，

​    "repasswd:""，

​    "ver":""

}

return

验证码错误

{

   "static":"0"

}

用户名重复/用户名为空

{

​    "static":"1"

}

email已注册/email为空

{

​    "static":"2"

}

两次密码不一致/密码为空

{

​    "static":"3"

}

注册成功

{

​    "static":"4"

}

# 发送验证码到邮箱

### post /ensureEmail

{

​	"email":""

}



返回

email已注册/email为空

{

​    "static":"0"

}

发送成功

{

​	"ver": "",

​	 "email": ""

}

# 更改用户名

### post /ChangeUsername

{

​    "id":'',

​    "rename":''

}

id为空

{

​    "static":'0'

}

用户不存在/重命名为空

{

​    "static":"1"

}

成功

{

​    "static":"2"

}

# 用户主页信息

### post /userpage

{

​    "id":""

}

没有此用户

{

​    "static":"0"

}

返回

{

​    'static': 1,

​    'id': id,

​    'username': username,

​    'pit_uri': pit_uri,

​    'attention': attention,

​    'fans': fans,

​    'motto': motto

}

# 关注用户

### post /userAttention

{

​    'id':''

}

没有此用户,用户为自己

static:0

已关注

static:2

关注成功

static:1

# 取消关注

### post /notAttention

{

​    'id':''

}

没有此用户,用户为自己

static:0

未关注

static:2

取关成功

static:1

# 关注的用户列表(每页20)

### post /getAttentions

{

​    'id':'',

​    'page':''

}

失败

static:0

成功

{'data': {

​    'static': 1,

​    'id': id,

​    'username': username,

​    'pit_uri': pit_uri,

​    'attention': attention,

​    'fans': fans,

​    'motto': motto

},

{

​    'static': 1,

​    'id': id,

​    'username': username,

​    'pit_uri': pit_uri,

​    'attention': attention,

​    'fans': fans,

​    'motto': motto

}

}

# 粉丝列表

### post /getFans

{

​    'id':'',

​    'page':''

}

失败

static:0

成功

{'data': {

​    'static': 1,

​    'id': id,

​    'username': username,

​    'pit_uri': pit_uri,

​    'attention': attention,

​    'fans': fans,

​    'motto': motto

},

{

​    'static': 1,

​    'id': id,

​    'username': username,

​    'pit_uri': pit_uri,

​    'attention': attention,

​    'fans': fans,

​    'motto': motto

}

}

# 发表/修改文章

### post /PublishArticle

{

​    "uuid":"",

​    "content": "",

​    "id":,

​    "title":

}

内容为空 static:0

uuid为空 发表文章

成功 static:1

uuid存在 修改文章

修改文章不存在 static:3

成功修改： static:2

# 获取微头条列表（每页20）

### post /GetWeiArList

{

​    'id':'',

​    'page':''

}

返回

{

​    {

​            'static': 1,

​            'id': self.id,

​            'title': self.title,

​            'read_sum': self.read_sum,

​            'good_sum': self.good_sum,

​            'updateTime': self.updateTime,

​            'author_id': self.author_id

​    },

​    ...

}

# 删除评论

### post /deleteComment

{

​    "cid":'',

}

失败

static:0

成功

static:1

# 发布/修改微头条

### post /PublicWei

{

​    "uuid":"",

​    "content": "",

​    "id":,

}

内容为空 static:0

uuid为空 发表文章

成功 static:1

uuid存在 修改文章

修改文章不存在 static:3

成功修改： static:2

# 删除微头条

### post /deleteWei

{

​    "id":,

​    "uuid":

}

不是当前用户 static:0

uuid为空 static:1

没有此文章 static：2

成功 static:3

# 收藏文章列表

### post /likeAr_list

id,page

不是当前用户 static:0

成功 

{

​    {

​            'static': 1,

​            'uuid': uuid,

​            'title': title,

​            'content': content,

​            'types': types,

​            'read_sum': read_sum,

​            'comment': comment,

​            'updateTime': updateTime,

​            'author_id': author_id

​        },

​        {

​            'static': 1,

​            'uuid': uuid,

​            'title': title,

​            'content': content,

​            'types': types,

​            'read_sum': read_sum,

​            'comment': comment,

​            'updateTime': updateTime,

​            'author_id': author_id

​        }...

}

# 搜索文章

### post /relateAr

content,page

无content static:0

无搜索内容 static:1

成功： 

{

​    {

​            'static': 1,

​            'uuid': uuid,

​            'title': title,

​            'content': content,

​            'types': types,

​            'read_sum': read_sum,

​            'comment': comment,

​            'updateTime': updateTime,

​            'author_id': author_id

​        }，

​        {

​            'static': 1,

​            'uuid': uuid,

​            'title': title,

​            'content': content,

​            'types': types,

​            'read_sum': read_sum,

​            'comment': comment,

​            'updateTime': updateTime,

​            'author_id': author_id

​        }...

​    }

# 搜索用户

### post /relateUser

content,page

无content static:0

无搜索内容 static:1

成功：

{

​    {

​            'static': 1,

​            'uuid': uuid,

​            'title': title,

​            'content': content,

​            'types': types,

​            'read_sum': read_sum,

​            'comment': comment,

​            'updateTime': updateTime,

​            'author_id': author_id

​        },

​        {

​            'static': 1,

​            'uuid': uuid,

​            'title': title,

​            'content': content,

​            'types': types,

​            'read_sum': read_sum,

​            'comment': comment,

​            'updateTime': updateTime,

​            'author_id': author_id

​        }...

}

**===============**

# 首页文章

# 热闻

# 推荐文章

**===============**

# 其他文章

### post /OtherArticle

{

​    "page":""

}

返回

此页没有文章

{

​    "static": "0"

}

成功返回

{

​    'data':

​    {

​        {

​            'static': 1,

​            'uuid': self.uuid,

​            'title': self.title,

​            'content': self.content,

​            'types': self.types,

​            'read_sum': self.read_sum,

​            'comment': self.comment,

​            'updateTime': self.updateTime,

​            'author_id': self.author_id

​        }，

​        {

​            'static': 1,

​            'uuid': self.uuid,

​            'title': self.title,

​            'content': self.content,

​            'types': self.types,

​            'read_sum': self.read_sum,

​            'comment': self.comment,

​            'updateTime': self.updateTime,

​            'author_id': self.author_id

​        }...

​    } 

​    

}

# 收藏文章

### post /CollectArticles

{

​    "uuid":"",

​    "id":""

}

没有uuid

{

​    "static":"0"

}

id不是当前用户

{

​    "static":"1"

}

没有此文章

{

​    "static":"2"

}

成功收藏

{

​    "static":"3"

}

# 取消收藏

### post /DeleteCollectArticles

{

​    "uuid":"",

​    "id":""

}

没有uuid

{

​    "static":"0"

}

id不是当前用户

{

​    "static":"1"

}

没有收藏

{

​    "static":"2"

}

取消收藏成功

{

​    "static":"3"

}

# 文章详情

### post /show_article

{

​    "uuid":""

}

没有uuid

{

​    "static":"0"

}

没有此文章

{

​    "static":"1"

}

成功返回

{

​    'data':

​    {

​        {

​            'static': 1,

​            'uuid': self.uuid,

​            'title': self.title,

​            'content': self.content,

​            'types': self.types,

​            'read_sum': self.read_sum,

​            'comment': self.comment,

​            'updateTime': self.updateTime,

​            'author_id': self.author_id

​        }，

​        {

​            'static': 1,

​            'uuid': self.uuid,

​            'title': self.title,

​            'content': self.content,

​            'types': self.types,

​            'read_sum': self.read_sum,

​            'comment': self.comment,

​            'updateTime': self.updateTime,

​            'author_id': self.author_id

​        }...

​    } 

​    

}

# 获取评论

### post /get_comment

{

​    "uuid":"",

​    "page":""

}

没有uuid

{

​    "static":"0"

}

没有此文章

{

​    "static":"1"

}

成功返回

{

​    'data':

​    {

​        {

​            'static': 1,

​            'cid': self.cid,

​            'article_uuid': self.article_uuid,

​            'comment': self.comment,

​            'reply_sum': self.reply_sum,

​            'good_sum': self.good_sum,

​            'CommentTime': self.CommentTime

​        },

​        {

​            'static': 1,

​            'cid': self.cid,

​            'article_uuid': self.article_uuid,

​            'comment': self.comment,

​            'reply_sum': self.reply_sum,

​            'good_sum': self.good_sum,

​            'CommentTime': self.CommentTime

​        }...

​    } 

​    

}

# 发表评论/回复

### post /public_comment

{

​    "id":"", 

​    "uuid":"", 

​    "content":'", 

​    "is_toPerson":"" # 是否为回复(有为回复的评论的uuid，没有为空字符串)

}

id为空/id不是当前用户

{

​    "static":"0"

}

没有uuid

{

​    "static":"1"

}

没有此文章

{

​    "static":"2"

}

是回复但是没有此评论

{

​    "static":"3"

}

评论为空

{

​    "static":"4"

}

发表评论/回复成功

{

​    "static":"5"

}

# 查看回复

### post /show_reply

{

​    "article_id":"",

​    "cid":""

}

article_id为空/cid为空

{

​    "static":"0"

}

没有此评论

{

​    "static":"1"

}

成功返回

{

​    'data':

​    {

​        {

​            'static': 1,

​            'cid': self.cid,

​            'article_uuid': self.article_uuid,

​            'comment': self.comment,

​            'reply_sum': self.reply_sum,

​            'good_sum': self.good_sum,

​            'CommentTime': self.CommentTime

​        },

​        {

​            'static': 1,

​            'cid': self.cid,

​            'article_uuid': self.article_uuid,

​            'comment': self.comment,

​            'reply_sum': self.reply_sum,

​            'good_sum': self.good_sum,

​            'CommentTime': self.CommentTime

​        }...

​    } 

​    

}

# 点赞

### post /give_good

{

​    "user_id":"",

​    "comment_id":"",

​    "article_uuid":""

}



user_id 不为当前用户id:

{	

​	"static":"0"

}

没有此评论/已经点过赞:

{

​	"static":"1"

}

成功点赞

{

​	"static":"2"

}



# 取消点赞

### post  /delete_good

{

​	"user_id":"",

​	"cid":""

}



user_id 不为当前用户id:

{	

​	"static":"0"

}

没有此评论/没有点过赞:

{

​	"static":"1"

}

成功取消点赞

{

​	"static":"2"

}



# 查看点赞状态

### post /is_alreadyGood

{

​    "user_id":"",

​    "article_uuid":""

}



user_id 不为当前用户id:

{	

​	"static":"0"

}

没有此文章:

{

​	"static":"1"

}

返回成功

{

​	'data':{

​            'user_id': "",

​            'comment_cid': "",

​            'article_uuid':""

​        },

{

​            'user_id': "",

​            'comment_cid': "",

​            'article_uuid':""

​        }....

}

# 举报文章

### post /report_article

{
	"user_id":"",
	"article_uuid":"",
	"reason_id":""
}



返回

user_id为空/article_uuid为空/reason_id为空

{

​	"static":"0"

}

没有此用户

{

​	"static":"1"

}

没有此文章

{

​	"static":"2"

}

举报成功
{

​	"static":"3"

}



# 举报用户

### post /report_user

{
	"user_id":"",
	"report_id":"",
	"reason_id":""
}



返回

user_id为空/report_id为空/reason_id为空

{

​	"static":"0"

}

没有此用户

{

​	"static":"1"

}

没有此文章

{

​	"static":"2"

}

举报成功
{

​	"static":"3"

}



# 上传图片(统一)

### post    /Photo/<string:pitFrom>

### {

​	"img":"",(file)

​	"uuid":""

### }



返回

照片为空

{

​	"static":"0"

}

没有指明图片类型

{

​	"static":"1"

}

没有uuid

{

​	"static":"2"

}

没有此路径

{

​	"static":"3"

}

成功返回

{

​	'static': "5", 

​	'src': file_path, 

​	'filename': filename

}



# 获取图片信息

### post /Photo

{

​	"pitFrom":"",

​	"uuid":""

}

### 

返回

如果pitFrom/uuid为空

{

​	"static":"0"

}

pitFrom == "article_pit",没有此文章的图片

{

​	"static":"1"

}

pitFrom == "user_pit",没有此用户的图片

{

​	"static":"2"

}

pitFrom == "weiarticle_pit",没有此微头条的图片

{	

​	"static":"3"

}

成功返回

{

​	data:

​        # 如果是文章图片

​	{

​            'pit_name': self.pit_name,

​            'article_uuid': self.article_uuid,

​            'pit_uri': self.pit_uri

​        }..

​        # 如果是微头条图片

​	{

​            'pit_name': self.pit_name,

​            'article_uuid': self.article_uuid,

​            'pit_uri': self.pit_uri

​        }..

​	# 如果是用户头像

​	{

​            'pit_name': self.pit_name,

​            'user_id': self.user_id,

​            'pit_uri': self.pit_uri

​        }

}



# 获取图片

### post /GetPhoto

{

​	"pitFrom":"",

​	"pit_uri":""

}



pitFrom/pit_uri为空:

{

​	"static":"0"

}

没有此图片/图片路径有错

{

​	"static":"1"

}

成功返回

return response   response.headers['Content-Type'] = 'file'