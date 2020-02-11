# OAuth

[语雀允许申请创建OAuth应用](https://www.yuque.com/yuque/developer/about-oauth-apps)，从而让第三方可以通过用户授权的方式获取access_token。

语雀支持两种OAuth授权方式，一种是web应用方式，一种是非web应用方式。这两种模式的区别是，web应用方式在用户授权后，会把access token以redirect回uri的方式通知第三方的服务器；而非web应用方式则是通过client secret对访问进行签名，在用户授权后根据第三方生成的之前生成code来主动获取access token。从便捷性上来说，非web应用方式更适合在命令行中进行，比如由开发人员开完成一些统计工作等。

在pyuque中，既可以在代码中结合开发者自己应用使用pyuque.oauth模块来管理access token，也可以以命令行的方式来后去access token。首先，我们在命令行下，分别就web应用方式和非web应用方式来说明pyuque的OAuth认证流程。

## 命令行

### web应用方式

在命令行中执行如下命令:

```
python -m pyuque.cli --client_id <YOUR_CLIENT_ID>\
                     --client_secret <YOUR_CLIENT_SECRET>\
                     --redirect_uri <YOUR_REDIRECT_URI>\
                     oauth-web
```

执行上面的命令，把生成授权网址粘贴到浏览器中进行授权，然后在命令行中粘贴redirect url中的code参数的值后继续，就可以获得access token了。



### 非web应用方式

和web应用方式类似，通过pyuque.cli执行下面的命令，就可以执行非web应用方式的OAuth授权

```
python -m pyuque.cli --client_id <YOUR_CLIENT_ID>\
                     --client_secret <YOUR_CLIENT_SECRET>\
                     oauth-nonweb
```

非web应用方式的优点在于，不需要提供redirect url，也不需要在授权后从这个网址的参数中提取code参数的值。


## 在代码中使用pyuque.oauth模块

可以调用pyuque.oauth模块来集成OAuth的授权到自己的项目中，这主要是分成两个步骤:

- 调用authorize函数获取语雀的授权网址
- 调用get_access_token函数，根据前一步使用或者得到的code同语雀服务器换取access token

对于这两个函数的具体说明如下:

__authorize(client_id, scope="", redirect_uri="", state="", code="", client_secret='', mode="")__

- mode: OAuth授权的方式，web应用方式为"web"，非web应用方式为"non-web"，默认为非web应用方式。
- client_id: 第三方应用的client_id。
- scope: 授权的权限范围，详见[语雀的相关文档](https://www.yuque.com/yuque/developer/understanding-scopes-for-oauth-apps)，pyuque提供了两个额外的权限的shortcut，即"all"和"all:read"，分别代表除了"attach_upload"之外的全部权限和全部只读权限。
- redirect_uri: 只在web应用方式下需要，为用户在语雀网站授权后的跳转地址，必须和语雀后台申请OAuth应用的域名一致。
- state: 只在web应用方式下需要，为跳转地址可以携带的第三方应用的自定义参数。
- code: 只在非web应用方式下需要，是用户提供的client code，可以使用pyuque.oauth.gen_code()函数生成
- client_secret: 只在非web应用方式下需要，用于计算签名

__get_access_token(client_id, code, client_secret='', grant_type='')__

- grant_type: 授权方式，在web应用方式下应传入"authorization_code"，在非web方式应传入"client_code"。
- client_id: 第三方应用的client_id。
- code: 只在非web方式下需要，是authorized函数中提供的client_code。
- client_secret: 只在web应用方式下需要。

