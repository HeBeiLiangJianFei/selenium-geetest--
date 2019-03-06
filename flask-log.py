# import logging
# import logging.config
#
# log_filename = 'logg.log'
# logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s]%(levelname)s[%(funcName)s:%(filename)s,%(lineno)d]%(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filemode='a')
# def test01(i):
#     ret = -1
#     if i >0:
#         ret = 0
#     else:
#         ret = -1
#     return ret
#
# def test02():
#     i = -1
#     ret = test01(i)
#     if ret != 0:
#         logging.exception('test01 is error %d'% ret)
#
#
# if __name__ == "__main__":
#     test02()
import json

import request as request
from flask import Flask, render_template, request
import logging

app = Flask(__name__)

handler = logging.FileHandler('app.log',encoding='utf-8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
)
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.route("/")
def index():
    try:
        no_thing = []
        i = no_thing[0]
    except Exception as e:
        app.logger.exception("%s",e)
        return "error"

@app.route("/test-02")
def test_02():
    a = [1,2,3]
    try:
        print(a[3])
    except Exception as e:
        app.logger.exception('%s',e)


@app.route('/test-03')
def test_03():
    lis = [
        {"li":1},
        {"li":0},
        {"li":2},

    ]
    return render_template("test-03.html",lis=lis,name="hello wprld",)

@app.route('/test-03-server', methods=['POST'])
def test_03_server():
    if request.method == "POST":
        name = request.form.get('name')
        print("name==",name)
        return render_template("test-04.html",name=name)

@app.route('/test-03-ajax')
def test_o3_ajax():
    dic = {
        "message":"nihao"
    }
    dic = json.dumps(dic)
    return dic

from aliyunsdkcore import client
from aliyunsdkiot.request.v20180120 import RegisterDeviceRequest
from aliyunsdkiot.request.v20180120 import PubRequest
import json
import base64
from mns.queue import MNSClient, Queue

@app.route('/test-05')
def test_05():
    from flask import request
    if request.args.get("state") == '1':
        accessKeyId = 'LTAIwo0lpyvKhukW'
        accessKeySecret = 'RsPoPIC9AHXmVhxTh7EUUCdMEKC5tk'
        clt = client.AcsClient(accessKeyId,accessKeySecret,'cn-shanghai')
        request = PubRequest.PubRequest()
        request.set_accept_format('json')
        request.set_ProductKey('a1FSheGU7IX')
        request.set_TopicFullName('a1FSheGU7IX/WG581LL0718092000135/get')
        request.set_MessageContent('aGVsbG8gd29ybGQ=')
        request.set_Qos(0)
        result = clt.do_action_with_exception(request)
        print("result",result)
        return render_template('test-04.html',name=result)
    elif request.args.get('state') == '2':
        product_key = 'a1FSheGU7IX'
        access_key_id = 'LTAIwo0lpyvKhukW'
        access_key_secret = 'RsPoPIC9AHXmVhxTh7EUUCdMEKC5tk'
        host = "http://1255428372877457.mns.cn-shanghai.aliyuncs.com/"
        queue_name = 'aliyun-iot-' + product_key
        msn_clt = MNSClient(host=host, access_id=access_key_id, access_key=access_key_secret)
        queue = Queue(queue_name=queue_name, mns_client=msn_clt)
        message_body = queue.receive_message().message_body
        message_dict = json.loads(message_body)
        print('机器返回结果: ' + base64.b64decode(message_dict['payload']))
        data = base64.b64decode(message_dict['payload'])
        return render_template('test-04.html',name=data)



if __name__ == "__main__":
    app.run(debug=False)




























