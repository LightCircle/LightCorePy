
## setup.py 中 setup 函数的参数

 - packages
  可以列举要打包的内容
  也可以简单的使用 find_packages()
 
 - install_requires
  指定工程所需要的依赖关系, 由 pip 自动进行安装
  你的工程被安装时, pip 会尝试解析 install_requires 指定的内容
  
 - extras_require
  指定开发或单元测试需要的依赖关系, 可以使用如下方式解决依赖关系
  ```pip install -e dev```
  ```pip install -e test```
 
 - package_data
  如果工程有需要与代码一起安装的数据文件, 可以在这里指定

 - data_files
 
 - entry_points

## README.rst
 - 一般用于描述用户开发环境的构建手顺
 - rst后缀 : 是指使用 reStructuredTest 语法书写的文本文件

## python 基础知识

 - __init__.py
  Python会查找sys.path文件夹下存放的文件本身, 
  以及包含 __init__.py 文件的子文件夹中的文件作为 import 对象.
  _init__.py 文件内容可以为空
  
 - 执行单体测试
  ```# python setup.py test```
  
 - 关于 ``` if __name__ == '__main__': ```
  当 Python 文件被当做脚本执行时, __name__ 变量会被设定成 '__main__'
  而, 当被 import 加载时, __name__ 不会被设定
  所以, 一般用他来判断是否是以脚本方式启动的

 - json 的 dump 与 dumps 的区别
  dump会生成一个类文件对象，dumps会生成字符串

## Python 工程目录结构
 参考 http://monklof.com/post/19/

## 工具
 - 检查所有已经安装的 module 的版本
  ```$ pip freeze``` 

## 发布 Python 工程
 - 准备 setup.py 文件
 
 - PyPI账户操作
  ```$ python setup.py register```
  如果没有注册, 启动上述命令, 会提示注册, 按照命令行向导完成注册即可
  使用PyPI的用户名密码进行登陆, 登陆成功的状态会保存在 ~/.pypirc 里
 
 - 上传工程到 PyPI
  1. 需要twine，如果没有安装则使用pip安装，$ pip install twine
  1. 创建 ~/.pypirc 文件，指定PyPI的账户
  2. 程序打包 $ python setup.py sdist，在dist文件夹下生成zip文件
  3. 注册包 $ twine register dist/light-core-0.2.5.tar.gz
  4. 上传包 $ twine upload dist/light-core-0.2.5.tar.gz

 - 本地安装
  ```$ python3 setup.py install```

## 异常处理 关于 Exception 和 Return
 1. 未知的异常用try...except.
 2. 可预见的可以用if..else..处理下

## Coverage
 - ```$ coverage html```
  安装
 
 - ```$ coverage run -m unittest tests/mongo/test_type.py```
  收集测试覆盖率
  
 - ```$ coverage html ```
  查看HTML版覆盖率结果

## 部署
 - uwsgi:
 https://github.com/unbit/uwsgi
 http://qiita.com/morinokami/items/e0efb2ae2aa04a1b148b

 - gevent:
 https://github.com/gevent/gevent

 - asyncio:

 - uwsgi for mac
 安装依赖
 $ brew install openssl
 $ sudo brew link openssl --force
 $ sudo brew install pcre  >>>> 对应错误 !!! no internal routing support, rebuild with pcre support !!!
 $ pip install greenlet >>> 启用 asyncio 时, 需要先安装这个包
 
 编译安装
 $ LDFLAGS="-L/usr/local/lib" UWSGI_PROFILE=asyncio pip3 install uwsgi -I --no-use-wheel --verbose --no-cache-dir
   LDFLAGS - 编译用动态库路径
   UWSGI_PROFILE - 

 - uwsgi for linux

 启动
 $ uwsgi --http 0.0.0.0:7002 --http-websockets --greenlet  --master  --asyncio 100 --wsgi wsgi:application --python-autoreload 1 --pyargv '-local'
 
## map, reduce
  a = [{'key': list(item.keys())[0], 'select': True} for item in [{'a': 1}, {'b': 2}]]
  a = [{'key': k, 'select': True} for k, v in {'a': 1, 'b': 2}.items()]

## webpack 监视代码变化
 $ webpack --watch


## centos7 安装pip
  $ curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
  $ python get-pip.py