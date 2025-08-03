# 操作マニュアル
## 仮想環境の作り方
1. ターミナルを開く(Ctrl+Shiht+@)

1. 仮想環境を作りたいフォルダに移動

1. 仮想環境を作る

```
python -m venv venv　 (最後のvenvはファイル名)
```
4. 仮想環境を有効化する
```
venv\Scripts\Activate.ps1
```
---
## 新しくGitHubへ保存
1. GitHubで新しいリポジトリを作成
1. VSCodeでターミナルを開く(Ctrl+Shiht+@)
1. 初期化する 
```
git init
```
4. 追加する
```
git add .
```
5. GitHubのQuick setupに表示されている\
`https://github.com/ユーザー名/リポジトリ名.git`\
をコピーしてターミナルに貼り付ける
```
git remote add origin https://github.com/ユーザー名/リポジトリ名.git
```
※gitignoreでファイルが除外されない場合
```
git rm -r --cached .
```
---
## 今回インストールするライブラリ
```
flask
Flask-Migrate
Flask-SQLAlchemy
Flask-WTF
pandas (pandas --prefer-binary)
plotly
```
※pipをアップグレードする場合は\
`python -m pip install --upgrade pip`


---
## migrate(データベースについて)
1. マイグレーションの初期化
```
flask db init
```

2. モデルの変更を検知してマイグレーションファイルを作成
```
flask db migrate -m "メッセージ" (-m "メッセージはなくてもよい")
```

3. マイグレーションファイルを適用
```
flask db upgrade
```

---
## css, jsのライブラリ

|ライブラリ名 | 種類 | 主な役割 | CDN例 |
|---|---|---|---|
|Bootstrap|CSS|スタイリングやボタン，レイアウトなど全般|https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css|
|jQuery|JS|DOM操作、Ajax通信|https://code.jquery.com/jquery-3.7.1.min.js|
|Charts.js|JS|グラフ描画|https://cdn.jsdelivr.net/npm/chart.js|
|Plotly.js|JS|インタラクティブなグラフ描画|https://cdn.plot.ly/plotly-latest.min.js|
|Vue.js|JS|リアクティブなUI構築|https://cdn.jsdelivr.net/npm/vue@3/dist/vue.min.js|
|Font Awesome|CSS|アイコンフォント|https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css|
