import flask
import os

from light.model.datarider import Rider


def add(handler):
    """
    Add files, save the physical file to GridFS, Meta information to the files table
    :param handler:
    :return: Meta information
    """

    rider = Rider.instance()
    files, error = rider.write_stream_to_grid(handler)
    if error:
        return None, error

    meta = handler.params.data or {}
    handler.params.data = [dict(item, **meta) for item in files['items']]
    return rider.file.add(handler)


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


def stream(handler):
    rider = Rider.instance()
    file, error = rider.file.get(handler)
    if error:
        return None, error

    handler.params.id = file['fileId']
    result = Rider.read_stream_from_grid(handler)
    return result['fileStream'], None


def zip():
    raise NotImplementedError


def qrcode():
    pass
