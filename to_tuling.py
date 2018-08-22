import requests,json

#图灵接入接口
tuling_url="http://openapi.tuling123.com/openapi/api/v2"

def to_tuling(text,user_id):
    #按照图灵给我们提供的API文档 传递固定格式的数据
    data={
	"reqType":0,
    "perception": {
        "inputText": {
            "text": text
        },
    },
    "userInfo": {
        "apiKey": "03f1bb5ce38d40fcb0b19c5544372d6b",
        "userId": user_id
    }
}
    #发送json数据给图灵进行匹配测试
    res=requests.post(tuling_url,json.dumps(data))
    #接收图灵返回的消息
    response=json.loads(res.content.decode('utf-8'))
    response_text=response.get('results')[0].get('values').get('text')
    return response_text