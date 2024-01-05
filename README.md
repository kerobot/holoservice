# ホロサービス

MongoDB に登録されているホロジュールのホロライブスケジュールや配信者の情報を API として提供します。（ホロコレクトで登録したデータを利用します。）

## 環境

* Windows 11
* Python 3.11
* PowerShell 7.3.8
* Visual Studio Code 1.83
* Git for Windows 2.41
* MongoDB

## Poetry と pyenv の確認

```powershell
> poetry --version
Poetry version 1.3.2

> pyenv --version
pyenv 3.1.1
```

## MongoDB の確認

```powershell
> mongosh --version
1.6.0
```

## MongoDB に接続できることを確認

```powershell
> mongosh localhost:27017/admin -u admin -p
```

## データベースを作成してロール（今回は dbOwner ）を設定

```powershell
MongoDB > use holoduledb
MongoDB > db.createUser( { user:"owner", pwd:"password", roles:[{ "role" : "dbOwner", "db" : "holoduledb" }] } );
```

## プロジェクトで利用する Python をインストール

```powershell
> pyenv install 3.11.1
```

## プロジェクトで利用するローカルの Python のバージョンを変更

```powershell
> pyenv local 3.11.1
> python -V
Python 3.11.1
```

## バージョンを指定して、Python 仮想環境を作成

```powershell
> python -c "import sys; print(sys.executable)"
> poetry env use C:\Users\[UserName]\.pyenv\pyenv-win\versions\3.11.1\python.exe
```

## pyproject.toml を利用して Python のパッケージを一括インストール

```powershell
> poetry install
```

## プログラムの実行

```powershell
> poetry run uvicorn api.main:app --reload --port 8001
```

## Swaggerの利用

```text
http://127.0.0.1:8001/docs
```

## lounch.json の設定

```json
{
    "version": "1.0.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "api.main:app",
                "--reload",
                "--port",
                "8001"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```
