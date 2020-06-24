# Train_Ticket_System

***

# 《使用手册》

------

### 下载安装

* 需要python、MINGW或其他C/C++编译器
* pip install flask以及相关第三方库
* git clone
* 编译运行backend文件夹中所有cpp
* 在master目录下打开终端，输入flask run
* 打开浏览器（推荐Chrome）进入网页 "http://127.0.0.1:5000/"

### 注册与登录

* 由于未登录，第一次进入网页会路由至tourist page

![avatar](/img/tourist.png)

* 刷新一下，页面上有关火车的图片会随机发生变化

![avatar](/img/tourist2.png)

* 点击sidebar上的各种操作，系统会提示你“无权限访问”

![avatar](/img/tourist_fail.png)

* 点击login，跳转至登陆界面

![avatar](/img/login.png)

* 点击Signup，跳转至注册界面

![avatar](/img/register.png)

* 若输入不合规范，会在表单上方通过flash进行提示

![avatar](/img/register_invalid.png)

* 若输入无误，且注册的Username尚未使用，则注册成功，跳转至登陆界面

![avatar](/img/register_success.png)

* 若Username已经存在，注册失败

![avatar](/img/register_fail.png)

* 登录成功后进入主页，发现New User的数量加一

![avatar](/img/index.png)


### 火车操作

* 点击sidebar中的Train->添加，进入add_train页面

![avatar](/img/add_train.png)

* 按照提示输入火车信息，如果输入不合法，同样会通过flash进行提示

![avatar](/img/add_train_invalid.png)

* 点击sidebar中的Train->查询，进入query_train页面

![avatar](/img/query_train.png)

* 查询的火车如果尚未发布，可以在该页面快捷发布/删除

![avatar](/img/query_train_result.png)

* 发布火车操作的确认环节

![avatar](/img/query_train_release_ing.png)
 
* 发布之后的火车状态显示为Released

![avatar](/img/query_train_released.png)

* 也可以通过点击sidebar中的Train->发布，进入release_train页面

![avatar](/img/release.png)

* 点击sidebar中的Train->删除，进入delete_train页面

![avatar](/img/delete.png)

### 用户操作

* 点击sidebar中的User->添加新用户，进入add_user页面

![avatar](/img/add_user.png)

* 若输入不合规范，会在表单上方通过flash进行提示

![avatar](/img/add_user_invalid.png)

* 点击sidebar中的User->查询/修改，进入query_user页面

![avatar](/img/query_user.png)

* 若查询用户存在且权限不大于当前用户，成功查询，并可进行修改操作

![avatar](/img/query_user_result.png)

* 点击Modify，进入修改页面

![avatar](/img/modify.png)

### 票务操作

* 点击sidebar中的Tickets->票务查询，进入query_tickets页面

![avatar](/img/query_ticket.png)

* 可以通过'time','cost','transfer one and only'三种不同的优先方式输出结果，若有符合查询请求的火车票，可直接进行购买
 
![avatar](/img/query_ticket_result.png)

* 点击Buy，跳转至buy_tickets页面，车站名自动填充，日期可选范围更改为该旅程可行的时间范围（也可以通过点击sidebar中的Tickets->买票，自主进入buy_tickets页面）

![avatar](/img/query_to_buy.png)

* 根据候补意愿的选择和车辆情况提示购买结果

![avatar](/img/buy_success.png)

###其他操作

* 点击sidebar中的My Order，进入我的订单，可进行退票操作

![avatar](/img/my_order.png)

* 退票成功后的订单显示为Refunded

![avatar](/img/my_order_refunded.png)

* 点击sidebar中的Clear，进入清库界面

![avatar](/img/clear_all.png)

* 点击Clear all data，系统会向用户再三确认

![avatar](/img/clear_warning.png)

* 确认清空后，重新回到tourist page，所有数据清除

![avatar](/img/clear.png)
