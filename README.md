# rushi_login
登录测试使用

启动方式：直接运行main.py

1.注意安全的可能性
(1)失败5次自动锁定15分钟，防止暴力破解。
(2)密码加密（Hash方式存储，避免明文存储）。
(3)JWT使用HS256进行签名,确保token不被篡改。
(4)token有效时长设置为30分钟，过期后必须重新登录。
(5)如果不希望用户频繁登录，可以通过access_token(有效期短)与refresh_token(有效期长)结合的方式，
在access_token失效后通过refresh_token获取新的access_token,避免频繁登录。
(6)登录过程中密码需要加密，避免名称传输。
(7)使用https协议，避免用户信息(账号密码等)及token被窃取。
(8)token中不要存储客户敏感信息。


2.注意权限验证的便捷性，使得其他地方也能使用
(1)JWT是无状态的，无需维护session状态，全部信息存储到token,方便其他地方使用

3.考虑性能、可扩展性，说明如何达到的
(1)使用async实现异步数据库和Redis访问，提升性能
(2)通过mvc模式，利于维护与升级

4.注意选择的技术栈，说明为什么这样选择
fastapi+asyncio+aioredis+mysql+pyjwt
(1)fastapi是异步框架，性能高，开发效率高
(2)sqlalchemy是异步ORM，性能高，开发效率高
(3)redis是内存数据库，性能高，开发效率高
(4)aioredis是异步redis客户端，性能高，开发效率高
(5)pyjwt通过jwt，有利于性能及扩展