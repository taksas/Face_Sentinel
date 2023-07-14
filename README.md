# Face Sentinel
### 常時起動型 顔認証ソフトウェア


#### 初回設定
- Pythonの実行環境があること
- `Dependencies.md`を参考に、必要なライブラリをインストールしていること
- `config_sample.ini`をコピーして`config.ini`を作成、内容の編集

が最低要件になります。

##### config.iniの記述

config.iniには以下の7つのパラメータが必要であり、かつFace Sentinel(以降FSと表記)と同じフォルダに入っている必要があります。
- **debugging** : デバッグ用の出力を行うかどうか。動作には影響ありません。GUIからは設定できません。
- **limit** : 動作間隔（秒）。実際の動作間隔はこの数字+顔認証処理時間となります。GUIからも設定可能です。
- **your_pics_dir** : 事前に用意する本人画像を入れたフォルダ。何枚用意しても構いませんが増やした分だけ動作は重くなります。GUIからは設定できません。
- **capture_pics_dir** : カメラから撮影した写真の保存先。撮影した写真については、自動で削除する機能は用意していません（ログ代わりになるため）。必要に応じて、定期的に削除するスクリプトなど組んでください。GUIからは設定できません。
- **tolerate_target_face__errors** : 写真解析時にエラーが出た場合、そのエラーを許容するかどうか。逆光や周囲が暗すぎる、撮影した写真（または、用意した本人写真）の中に複数人が映り込むなどで解析エラーが発生しますが、そのエラーを許容するかどうかです。許容する（1）の場合、エラーが起きても動作を継続します。許容しない場合（0）、エラーが起きると画面をロックします。GUIからも設定可能です。
- **rigidity** : 集計された本人判定結果の内、どの程度の他人判定を許容するかの厳格度（0～100で記述、単位は%）。事前に用意した本人写真の内、どれだけの枚数（%）で本人と判定されれば良いかの閾値です。GUIからも設定可能です。
- **threshold** : 本人判定の厳格度（0～1で記述）。各本人画像と撮影画像について、それぞれこの閾値を用いて同一人物か判定します。（その判定結果の内何%以上で同一人物判定になる必要があるかは`rigidity`で設定）0に近いほど同一人物に近くなります。GUIからも設定可能です。


##### 追加の設定

加えて、常駐の設定をしたい場合は、タスクスケジューラからよしなに設定してください。
設定の例として、`FS_TaskScheduler_Example.xml`を用意しています。ユーザー名などを書き換えて使用してください。

また、常駐時、セキュリティを向上するためにFSの含まれるフォルダにUACチャレンジを必須にすることも可能です。

1. `UserAccountControlSettings.exe`からセキュリティレベルを最上位に設定しておいてください。

2. タスクスケジューラで登録するタスクでは`最上位の特権で実行する`にチェックを入れます。

3. FSの含まれるフォルダからログオン中のユーザーの権限を全削除してください。

このとき、Administratorが残っていれば「タスクスケジューラからは動作するがログオン中のユーザーからは（UACチャレンジ無しでは）FSのファイルは閲覧&編集できない」状況になるはずです。

`your_pics_dir`、`capture_pics_dir`も同じアクセス権限にすることをお勧めします。