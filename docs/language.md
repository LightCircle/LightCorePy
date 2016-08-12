
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
  ```$ python setup.py sdist upload```
  sdist 会将工程进行打包, 默认为tar.gz格式
  upload 用于上传工程到 PyPI
  install 

 - 本地安装
  ```$ python3 setup.py install```

## 异常处理 关于 Exception 和 Return
 1. 未知的异常用try...except.
 2. 可预见的可以用if..else..处理下
