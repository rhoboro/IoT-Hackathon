# Intel IoT Roadshow

## プロジェクト構成
* app.py
  - BluemixでたてたMQTTブローカーへきた情報をごにょごにょして、remote.pyへの指示を決める

* local.py
  - 自宅の栽培キットで取得したデータをMQTTブローカーへパブリッシュする

* remote.py
  - app.pyによって決められた野菜工場のLEDの増減指示をMQTTブローカーからサブスクライブする

# リモート栽培キット

## 課題
![スライド1](./keynote/slide1.png)

## 解決策
![スライド2](./keynote/slide2.png)

## 全体像
![スライド3](./keynote/slide3.png)
