#Twitter API用のモジュール
import tweepy
import simplejson

#画像処理モジュール
import numpy as np
import cv2

#URL用モジュール(画像のダウンロード)
import urllib.request

#その他モジュール
import random

#----------------------------------------------#

#先ほど取得した各種キーを代入する


#Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth_handler=auth)

#自身のボットネームの取得
bot_name = api.me().screen_name

#h@@@ttps://www.take01x.okinawa/archives/151
class myStreamListener(tweepy.StreamListener):
    print('test999')

    def on_status(self, status):
        print(status.text)

    #データが来たとき
    def on_data(self, data):
        print('データ来た！')
        FLAG = 1;
        if data.startswith("{"):
            print('処理するね！')
            #データをパイソンの辞書に変換
            data = simplejson.loads(data)
            #データを取得したときの動作
            if "text" in data:
                print('---処理中---')
                #ボットへのリプライにキーワードが含まれていたとき、挨拶を返す
                if data['in_reply_to_screen_name'] == bot_name and "chop" in data['text']:
                    print('返信したよ！')

                    #処理①：画像の保存(urllib)
                    url = data['entities']['media'][0]['media_url']
                    savename = "download_twitter.jpg"

                    print(url)

                    urllib.request.urlretrieve(url, savename)

                    #処理②：画像のリサイズ(opencv)
                    img = cv2.imread("download_twitter.jpg") #画像読み込み

                    height, width, ch = img.shape

                    x1, y1 = 0, 0
                    x2, y2 = round(width / 2), 0

                    w, h = round(width / 2), height

                    roi1 = img[y1:y1+h, x1:x1+w]
                    roi2 = img[y2:y2+h, x2:x2+w]


                    #cv2.imshow('test', hsv)       #imgをtestウィンドウで表示

                    cv2.imwrite("out1.jpg", roi1)

                    cv2.imwrite("out2.jpg", roi2)


                    #処理③：画像付きのツイート(tweepy)
                    Tweet = "@" + data['user']['screen_name'] + " " + "done " + " " * random.randint(0,10)

                    #複数画像投稿するための処理
                    file_names = ['out1.jpg','out2.jpg']
                    media_ids = []
                    for filename in file_names:
                        res = api.media_upload(filename)
                        media_ids.append(res.media_id)

                    #ツイート
                    api.update_status(media_ids = media_ids, status = Tweet, in_reply_to_status_id = data['id'])#画像添付機能修正


#ストリーミングに情報をセット
stream = tweepy.Stream(auth = api.auth, listener = myStreamListener(), secure = True, timeout = None)

#ユーザーストリーミングを開始
stream.userstream()
print('実行！')
stream.filter(track=['@Kochi_tongpoo'])
