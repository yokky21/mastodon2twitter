# Mastodon to Twitter

## 使い方

読み込む ini ファイルを引数で指定します。  
指定しなかった場合、mastodon2twitter.py と同じ場所にある mastodon2twitter.ini を読みます。

[mastodon] セクションでは読み込み元の URL を指定します。  
ユーザ名のうしろに .atom をつけると RSS でデータが取れるので、このスクリプトではそのデータをパースしています。

[twitter] セクションでは投げ込み先である Twitter の consumer key 及び access token を設定します。


