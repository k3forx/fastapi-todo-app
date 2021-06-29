# fastapi-todo-app

## ライブラリなどのバージョン

バックエンド (Python)

- Python: 3.9.x
- FastAPI (フレームワーク): v0.65.2

フロント (CSS と JavaScript)

- bootstrap: v5.0.2

## 仮想環境の構築

公式ドキュメントにしたがって仮想環境を構築していきます。

- https://docs.python.org/ja/3/library/venv.html

まずは現状の python のバージョンをチェックしましょう。

```bash
❯ python -V
Python 2.7.16

❯ python3 -V
Python 3.9.5
```

```bash
❯ python3 -m venv venv

❯ ls
README.md  venv

❯ source venv/bin/activate

❯ python -V
Python 3.9.5

❯ python3 -V
Python 3.9.5

❯ deactivate

❯ python -V
Python 2.7.16

❯ python3 -V
Python 3.9.5
```

## FastAPI で Hello World

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}
```

起動する。

```bash
❯ uvicorn main:my_app --reload
```

http://localhost:8000 にアクセスする。

![image](https://user-images.githubusercontent.com/45956169/123547586-57a17080-d79c-11eb-8680-d6cc190b2267.png)

さらに http://localhost:8000/docs にアクセスする。
![image](https://user-images.githubusercontent.com/45956169/123547668-9a634880-d79c-11eb-82b4-de7316a6173c.png)

## ORM

https://docs.sqlalchemy.org/en/14/tutorial/engine.html

## データベースの設定

### Docker で MySQL で
