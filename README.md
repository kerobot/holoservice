# ホロサービス

MongoDB に登録されているホロジュールのホロライブスケジュールや配信者の情報を API として提供します。（ホロコレクトで登録したデータを利用します。）

## 動作環境

* Windows 11
* Python 3.11+
* uv
* MongoDB
* Visual Studio Code

## MongoDB の事前確認

### 1. MongoDB バージョン確認

```powershell
mongosh --version
```

### 2. MongoDB へ接続できることを確認

```powershell
mongosh localhost:27017/admin -u admin -p
```

### 3. データベース作成とロール設定（dbOwner）

```powershell
use holoduledb
db.createUser({ user: "owner", pwd: "password", roles: [{ role: "dbOwner", db: "holoduledb" }] })
```

## セットアップ（uv）

### 1. `.env` を作成

`.env.sample` をコピーして `.env` を作成し、接続情報を設定してください。

```powershell
Copy-Item .env.sample .env
```

`.env` の主な項目:

```env
MONGO_URI="mongodb://[user]:[password]@127.0.0.1:27017/[db]"
MONGO_DATABASE="holoduledb"
JWT_SECRET_KEY="[JWT_SECRET_KEY]"
JWT_ALGORITHM="HS256"
JWT_EXP_DELTA_MINUTES=15
```

### 2. 依存関係のインストール

```powershell
uv sync
```

### 3. API の起動

```powershell
uv run uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

## VS Code での実行・デバッグ

`.vscode/launch.json` は uv 環境（`.venv`）を使う設定です。

* `FastAPI: Run (uv)`
  * `--reload` ありの通常実行
* `FastAPI: Debug (uv)`
  * `--reload` なしのデバッグ向け実行

現在の設定例:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI: Run (uv)",
            "type": "debugpy",
            "request": "launch",
            "python": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
            "module": "uvicorn",
            "args": [
                "api.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8001",
                "--reload"
            ],
            "cwd": "${workspaceFolder}",
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "FastAPI: Debug (uv)",
            "type": "debugpy",
            "request": "launch",
            "python": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
            "module": "uvicorn",
            "args": [
                "api.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8001"
            ],
            "cwd": "${workspaceFolder}",
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

## Swagger

```text
http://127.0.0.1:8001/docs
```

## 補足（認証関連）

* このプロジェクトは `passlib` + `bcrypt` を利用します。
* 依存は `pyproject.toml` にて `bcrypt>=4.0.0,<4.1.0` を指定しています。
* ログイン用の `users.password` は必ずハッシュ値（bcrypt 形式）を保存してください。
