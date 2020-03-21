# sports



## 环境准备

1. python 3.7

   安装依赖

   pip install -i "https://pypi.tuna.tsinghua.edu.cn/simple" -r requirements.txt



2. mysql

   在config.yaml中设置相应的mysql配置

   ```
   # 数据库连接
   SQLALCHEMY_DATABASE_URI: 'mysql+pymysql://用户名:密码@主机名:3306/数据库名?charset=utf8mb4'
   ```

# 运行

linux环境下：

```
sh ./run.sh
```



接口说明：

POST  http://localhost:80/api/add_user 

body: {

"用户名":"密码"

}

创建一个用户

GET http://localhost:80/api/getSports

获取所有sports数据