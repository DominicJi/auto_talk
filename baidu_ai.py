from aip import AipSpeech
import os
import uuid
from aip import AipNlp
import to_tuling

""" 你的 APPID AK SK """
APP_ID = '11710179'
API_KEY = 'Pmnoe7g14eryGgkDfMQAqakk'
SECRET_KEY = '2sTfYI0GRhdCKazWQR9L1AqfGwt7FNAc '

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
baidu_nlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def audio2text(file_name):
    # 将wav wma mp3 等音频文件转换为 pcm 无压缩音频文件
    cmd_str = "ffmpeg -y -i %s -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm" % (file_name, file_name)
    # 调用操作自动执行上述命令完成转换
    os.system(cmd_str)
    # 读取音频文件数据
    file_content = ""
    with open(f"{file_name}.pcm", 'rb')as f:
        file_content = f.read()
    # 将音频转换成文本
    res = client.asr(file_content,'pcm',16000,{
        'dev_pid':1536
    })
    # 返回文本数据
    return res.get('result')[0]


def text2audio(text):
    # 生成文件名存放转换过的文本文件
    mp3_file = f"{uuid.uuid4()}.mp3"
    mp3_file_path = os.path.join('templates',mp3_file)
    # 将文本文件识别成音频文件
    speech = client.synthesis(text, 'zh', 1, {
        'spd': 4,
        'vlo': 8,
        'pit': 8,
        'per': 4
    })
    # 存放到文件中
    with open(mp3_file_path,'wb')as f:
        f.write(speech)
    # 将转换成功的音频文件路径发给客户端
    return mp3_file


def faq(text, user_id):
    return to_tuling.to_tuling(text, user_id)
