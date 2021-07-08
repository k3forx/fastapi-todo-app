# 【Python】最新フレームワーク FastAPI と Prometheus で DevOps な開発にチャレンジ！

## 目的

- Python の軽量かつ高速なフレームワーク FastAPI で ToDo アプリを作成し、フレームワークの使い方を学ぶ
- DevOps のベストプラクティスの一つであるモニタリングについて、Prometheus を通して学ぶ

## 構成

1. コースと講師の紹介
1. FastAPI で HelloWorld
1. ページの HTML ファイルを作成
1. HTML ファイルと FastAPI を連携させる
1. FastAPI とデータベース (MySQL) を連携させる
1. タスク詳細画面を完成させる
1. タスク一覧画面を完成させる
1. 新規作成画面を完成させる
1.

## アプリの詳細

### 画面

### API

- `/tasks/`: タスクの一覧を表示
- `/tasks/{task_id}`: task_id = `task_id` が割り振られたタスクの詳細を表示
- `/tasks/{task_id}/completed`: task_id = `task_id` で割り振られたタスクを完了する
- `/tasks/{task_id}/deleted`: task_id = `task_id` で割り振られたタスクを削除する
- `/tasks/new`: タスクの新規作成する
- `/tasks/download/todo`: 未完了のタスク一覧をダウンロードする
- `/tasks/download/completed`: 完了済みのタスク一覧をダウンロードする

## 紹介する技術や考え方

### fastAPI

- 比較的新しい Python のフレームワーク
- 軽量、高速

### Prometheus

監視

### DevOps

#### ベストプラクティス

- 継続的インテグレーション
- 継続的デリバリー
- マイクロサービス
  - FastAPI, Prometheus と MySQL をそれぞれコンテナで起動する
- Infrastructure as Code
- モニタリングとロギング
  - Prometheus を利用したアプリの監視方法について学ぶ
- コミュニケーションと共同作業
  - アプリの異常事態を Slack に送ったり、メールアドレスに送ったりする

## FastAPI で HelloWorld

### 仮想環境の構築

仮想環境を構築するメリットには以下のようなことがある。

- アプリごとに異なる Python のバージョンを指定することができる
- システムにもともと入っている Python の環境を壊すことなく、新しいライブラリの追加などができる
- 簡単に構築できる -> 複数人で同じ環境が構築しやすい

公式ドキュメントにしたがって仮想環境を構築する。

- https://docs.python.org/ja/3/library/venv.html

現状の python のバージョンをチェック。

```bash
❯ python -V
Python 2.7.16

❯ python3 -V
Python 3.9.5
```

まずはアプリに関するスクリプトを保存するためのディレクトリを作成する。

```bash
❯ mkdir udemy-todo-app-with-fastapi
```

仮想環境を構築する。 `source` コマンドで仮想環境を起動、 `deactivate` コマンドで仮想環境を停止することができる。 `which python` コマンドで `venv` ディレクトリ内にある Python が表示されれば、仮想環境がうまく構築できている。

```bash
❯ cd udemy-todo-app-with-fastapi

❯ python3 -m venv venv

❯ ls
README.md  venv

❯ source venv/bin/activate

❯ python -V
Python 3.9.6

❯ python3 -V
Python 3.9.6

❯ which python

❯ deactivate

❯ python -V
Python 2.7.16

❯ python3 -V
Python 3.9.5
```

### VSCode のインストール

- https://code.visualstudio.com/download

### FastAPI で Hello World

`app` というディレクトリを作成し、その中に `main.py` を以下のような内容で作成する。

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}
```

この仮想環境で使用するライブラリは全て `requirements.txt` に記述する。そうすれば、GitHub などで複数人が開発するときも、全員が同じバージョンのライブラリを使うことができ、同じ動作が保証できる。
現時点では、 `requirements.txt` には、以下のライブラリを追加しておく。このファイルも `app` ディレクトリ以下に作成する。

```txt
fastapi==0.65.2
uvicorn==0.14.0
```

`pip` コマンドでライブラリをインストールする。

```bash
❯ pip install -r requirements.txt
```

アプリを以下のコマンドで起動。

```bash
❯ uvicorn main:app --reload
```

`--reload` オプションでファイルの変更を即時に反映させる。

http://localhost:8000 にアクセスする。

![image](https://user-images.githubusercontent.com/45956169/123547586-57a17080-d79c-11eb-8680-d6cc190b2267.png)

さらに http://localhost:8000/docs にアクセスする。
![image](https://user-images.githubusercontent.com/45956169/123547668-9a634880-d79c-11eb-82b4-de7316a6173c.png)

### Unit test (単体テスト)

<!-- #### なぜテストを書くのか -->

<!-- 何かアプリケーションコードを書くとき、それに対応する「テスト」を書くと良いでしょう。なぜなら、テストはアプリケーションがどのような動作をするかを記述したものであり、すなわち、そのアプリケーションの仕様を表しているということができるからです。またバグを発見しやすくしたり、アプリケーションの設計に問題がないかなどを検証することができるなどさまざまなメリットがあります。

例えば、GitHub にコードの変更をコミットするごとにテストを実行し、自分が変更したアプリケーションコードが他の部分のコードに影響がないかをチェックすることができます。

テストにはさまざまな種類のものがありますが、ここでは単体テスト、ユニットテストと呼ばれるテストを実装していきます。 -->

### Unit test の実装

ユニットテストを記述するファイルには `test_<file name>.py` と名前をつけるのが一般的です。 `main.py` に対するユニットテストを記述するファイルは `test_main.py` となります。

まずはユニットテストのファイルを保存するディレクトリを作成しましょう。

```bash
❯ mkdir unit_test
```

その後、ディレクトリ内に `__init__.py` と `test_main.py` を作成します。 `__init__.py` はスクリプトファイルをインポートするときに必要なファイルです。 `test_main.py` は `main.py` に対するテストを記述するファイルです。

```bash
❯ touch unit_test/__init__.py

❯ touch unit_test/test_main.py
```

`test_main.py` にテストケースを書いていきます。

```Python
from fastapi import status
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_hello_world():
    response = client.get("/")
    assert response.json() == {"message": "Hello World"}
    assert response.status_code == status.HTTP_200_OK
```

解説

- テスト用のクライアントは `main.py` で生成された `app` インスタンスと `TestClient` メソッドを用いて生成します
- テストケースは `test_<function name>.py` と名前をつけます
- テスト用のクライアントに対して、メソッドやパス、リクエストボディなどを記述してレスポンスをゲットします
- 返ってきたレスポンスからステータスコードやレスポンスボディの内容をチェックします

### Unit test の実行

書いたユニットテストを実行しましょう。テストを実行するには `pytest` というライブラリを用いるので、 `requirements.test.txt` というファイルに **テストに必要なライブラリのみを** 記述しましょう。

テスト用のクライアントは内部で `requests` ライブラリを用いてるので、そのライブラリも記述しておきます。

```txt
pytest==6.2.4
requests==2.25.1
```

テスト用に必要なライブラリとアプリケーションを動かすのに必要なライブラリをきちんと分けた方が、どのライブラリがどんな目的で使われているかはっきりするので、良いでしょう。

```bash
❯ pytest
```

カバレッジを表示したい場合は、 `requirements.test.txt` に以下の 1 行を追加します。

```txt
pytest-cov==2.12.0
```

カバレッジレポートを表示したい場合は、 `--cov` オプションをつけて `pytest` を実行します。

```bash
❯ pytest --cov
```

`pytest` には非常に多くのオプションがあるので、必要に応じて付け加えるのが良いでしょう。

<!-- ❯ pytest -vvvs --cov=./ --cov-config=../.coveragerc --cov-report=term-missing unit_test --disable-pytest-warnings -->

### Docker に移行する

Docker でアプリケーションを動かせるようにしておけば、以下のどのようなプラットフォームにデプロイしても、基本的には同じ動作が保証されます。

- AWS
- GCP
- Azure
- Heroku
- etc...

プラットフォームに大きく依存せずにアプリケーションが実行できるということは、アプリケーションをデプロイするのに必要な工数を下げることができ、高速なデリバリが可能になります。

それでは、Docker コンテナを立ち上げるために必要な Dockerfile を作成してきましょう。Dockerfile は以下のようになります。

```Dockerfile
FROM python:3.9.6-slim-buster

WORKDIR /usr/src

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install -r ./requirements.txt --no-cache-dir

COPY main.py /usr/src/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

docker イメージを作成し、コンテナを起動します。

```bash
❯ docker build ./app -t fastapi-todo-app

❯ docker images | grep fastapi-todo-app
fastapi-todo-app                     latest    2bf123e25958   2 minutes ago    184MB

❯ docker run --name todo-app -d -p 8000:8000 fastapi-todo-app

❯ docker container ls
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS          PORTS                                       NAMES
2448bc401bd5   fastapi-todo-app   "uvicorn main:app --…"   24 seconds ago   Up 21 seconds   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   todo-app

❯ docker stop todo-app

❯ docker rm todo-app
```

解説

- `docker build` コマンドを実行するときは `-t` オプションをつけて、作成される Docker イメージに名前をつけることができます
- `docker images` コマンドで作成された Docker イメージを確認することができます
- `docker run` コマンドでコンテナを起動することができます。オプションの説明は以下にあります。
  - `--name`: コンテナの名前を指定
  - `-d`: デタッチドモードでコンテナを起動
  - `-p`: ホストのポートをコンテナのポートにマッピングします
- `docker container` コマンドで起動しているコンテナの確認やコンテナの停止、再開などができます

## ページの HTML ファイルの作成

このセクションでは、

やること

- タスク一覧ページを作成する
- タスクの詳細ページを作成する
- タスクの新規作成ページを作成する

### ナビゲーションバーの実装

今回は Bootstrap (v5.0.x) を利用する。

- https://getbootstrap.com/docs/5.0/getting-started/introduction/

HTML ファイルを保存するディレクトリ (`html`) と `index.html` を作成する。

```bash
❯ mkdir html

❯ touch html/index.html
```

[Starter Template](https://getbootstrap.com/docs/5.0/getting-started/introduction/#starter-template) をコピーし、 `Option 2` の部分を削除する。

```HTML
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

  </body>
</html>
```

ファイルを開いて表示する。

<img width="855" alt="貼り付けた画像_2021_07_08_23_51" src="https://user-images.githubusercontent.com/45956169/124943522-885c9200-e047-11eb-88be-d216cb149063.png">

次にトップのナビゲーションツールを実装する。

左のメニューの `Components` から `Navbar` を選択する。 `Supported content` にある例をコピペする。

- https://getbootstrap.com/docs/5.0/components/navbar/
- https://getbootstrap.com/docs/5.0/components/navbar/#supported-content

検索窓などを削る。

### タスク一覧の表示

タスクの一覧は Card を用いて表示する。 `Components` から `Card` を選択する。`Header and footer` のセクションにあるサンプルをコピペする。

- https://getbootstrap.com/docs/5.0/components/card/#header-and-footer

ボタンにアイコンを追加する。アイコンは以下のリンクにあるものを使用する。

- https://icons.getbootstrap.com/

### タスク詳細画面と新規作成画面の表示

左メニューの `Forms` から `Form controls` を選択する。 `Example` にあるコードをコピペする。

- https://getbootstrap.com/docs/5.0/forms/form-control/#example
- https://getbootstrap.com/docs/5.0/forms/select/#default
- https://getbootstrap.com/docs/5.0/components/buttons/#examples

### ページ遷移の確認

最後にリンクをハードコードして、HTML だけで遷移するかチェックする。

## HTML ページと FastAPI を連携させる

やること

- HTML ファイルをテンプレートに切り分ける
- API のエンドポイントを作成する

## FastAPI とデータベースを連携させる

### 設計

データベース名

- `todo_app`

テーブル名

- `priorities`: タスクの優先順位を保存するためのテーブル
- `tasks`: タスクの情報を保存するテーブル

スキーマ

- `priorities` テーブル

| Field      | Type         | Null | Key | Default | Extra          |
| ---------- | ------------ | ---- | --- | ------- | -------------- |
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| pririty    | varchar(255) | NO   |     | NULL    |                |
| created_at | datetime     | NO   |     | NULL    |                |
| updated_at | datetime     | NO   |     | NULL    |                |

- `tasks` テーブル

| Field        | Type          | Null | Key | Default | Extra          |
| ------------ | ------------- | ---- | --- | ------- | -------------- |
| id           | int(11)       | NO   | PRI | NULL    | auto_increment |
| title        | varchar(30)   | NO   |     | NULL    |                |
| description  | varchar(1000) | NO   |     | NULL    |                |
| priority_id  | int(11)       | NO   |     | NULL    |                |
| due_date     | date          | NO   |     | NULL    |                |
| created_at   | datetime      | NO   |     | NULL    |                |
| updated_at   | datetime      | NO   |     | NULL    |                |
| completed_at | datetime      | YES  |     | NULL    |                |
| is_disabled  | boolean       | NO   |     | false   |                |

### Docker で MySQL コンテナを起動する

`MYSQL_ROOT_PASSWORD` は `root` ユーザでログインするために必要なパスワード。 `docker exec -it mysql bash` コマンドでコンテナ内に入り、 `root` ユーザ、 `MYSQL_ROOT_PASSWORD` で指定したパスワードで MySQL にログインできる。

```bash
❯ docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql:5.7

❯ docker exec -it mysql bash
root@6f83e666ef70:/# mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.34 MySQL Community Server (GPL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> exit
Bye
root@6f83e666ef70:/# exit
exit
```

### オブジェクトリレーショナルマッパー (ORM) とは

イメージ

ORM を導入する利点。

- データベースに関する違いを考慮しなくて良い
- SQL を書かなくて良い

### SQLAlchemy の導入

Python に使われる ORM の一つに SQLAlchemy があるので、今回はこちらのライブラリを用いる。
https://docs.sqlalchemy.org/en/14/tutorial/engine.html

`requirements.txt` に以下の 2 行を追加。

```txt
SQLAlchemy==1.4.20
pymysql==1.0.2
```

`pip` コマンドでインストール。

```bash
❯ pip install -r requirements.txt
```

### FastAPI と MySQL を連携させる

以下の 3 つのファイルを作成する。

- `database.py`: データペースとテーブルにアクセスするための設定を記述する
- `crud.py`: テーブルに対する操作 (データの挿入など) を記述する
- `models.py`: テーブルのカラムとオブジェクトの対応を記述する

## 詳細画面のロジックを完成させる

## 一覧画面のロジックを完成させる

## 新規作成機能を完成させる

やること

-

## ダウンロード機能の修正

やること

-

## Unit tests の追加

## Prometheus の導入

### Prometheus とは

### Docker で Prometheus を立ち上げる

### 監視の設定

```bash
❯ curl -X POST http://localhost:9090/-/reload
```

### アラートの設定

### Grafana による可視化
