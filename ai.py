from flask import Flask,request,render_template
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import os
import uuid
import baidu_ai

app=Flask(__name__)
# @app.route('/',strict_slashes=False)
# def home():
#     return render_template('listen_say.html')


@app.route('/toy')
def toy():
    user_socket = request.environ.get("wsgi.websocket") #type:WebSocket
    while True:
        msg=user_socket.receive()
        #利用uuid给文件命名 并用到python3.6新语法格式化字符串
        wav_file = f"{uuid.uuid4()}.wav"
        #拼接文件路径 放到templates下面存放
        wav_file_path = os.path.join('templates',wav_file)
        #判断文件类型，如果是音频数据则执行写入等一系列操作
        if type(msg) == bytearray:
            with open(wav_file_path,'wb')as f:
                f.write(msg)
            #将音频数据转换成正常文本数据
            text = baidu_ai.audio2text(wav_file_path)
            #对此文本数据进行识别并回复相应内容
            answer=baidu_ai.faq(text,'xxx')
            #再将文本数据转换成音频文件
            file_name=baidu_ai.text2audio(answer)
            #将转换过后的音频文件路径发给客户端
            user_socket.send(file_name)
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1',8000),app,handler_class=WebSocketHandler)
    http_server.serve_forever()