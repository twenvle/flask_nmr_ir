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