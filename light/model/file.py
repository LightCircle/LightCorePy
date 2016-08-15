import flask
import os


def add():
    """
    添加文件, 物理文件保存到 GridFS 中，Meta信息保存到 files 表中
    :return: Meta信息
    """
    raise NotImplementedError


def update():
    raise NotImplementedError


def upload():
    # <form action="" method=post enctype=multipart/form-data>
    # <p>
    #     <input type=file name=file>
    #     <input type=submit value=upload>
    # </p>
    # </form>

    # app.add_url_rule('/upload', endpoint='nnn', view_func=func4, methods=['POST'])
    # app.add_url_rule('/download', endpoint='qqq', view_func=func5, methods=['GET'])

    # 保存上传文件
    def upload():
        if flask.request.method == 'POST':
            file = flask.request.files['file']
            d = os.path.join(os.path.abspath('..'), 'uploaded')
            file.save(d)

        return 'OK'

    # 对应下载文件
    def download():
        def generate():
            data = [['1', '2', '3', '4', '5'], ['6', '7', '8', '9', '10']]
            for row in data:
                yield ','.join(row) + '\n'

        return flask.Response(generate(), mimetype='text/csv')

    raise NotImplementedError


def download():
    raise NotImplementedError


def image():
    raise NotImplementedError


def pdf():
    raise NotImplementedError


def stream():
    raise NotImplementedError


def zip():
    raise NotImplementedError


def qrcode():
    pass
