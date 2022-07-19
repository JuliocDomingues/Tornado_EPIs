from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import yolov5
import json
import base64

path_image = r"C:\Users\estagio.sst17\OneDrive - SESIMS\Documentos\imageToSave.png"


def detect(source):
    return yolov5.detect.run(source=source,
                             imgsz=(640, 640),
                             conf_thres=0.58,
                             save_txt=False,
                             save_conf=False,
                             nosave=True,
                             line_thickness=1,
                             name='Results_Tornado')


class Detect_EPIs(RequestHandler):
    def post(self):
        request_json = self.request.body.decode()

        base64_image = json.loads(request_json)
        image = base64_image['Key']
        base64_image_bytes = image.encode('UTF-8')

        with open(path_image, 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_image_bytes)
            file_to_save.write(decoded_image_data)

        results = detect(path_image)

        self.write({'Results': results})


def make_app():
    urls = [(r"/", Detect_EPIs),
            (r"/detect/", Detect_EPIs)]

    return Application(urls, debug=False)


if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    IOLoop.instance().start()
