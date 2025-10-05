# LangGraph News Twitter Agent

LangSmith向けのニュース取得・要約・Twitter投稿を行うエージェントプロジェクトです。

## 🚀 クイックスタート

### 前提条件

- Docker
- Docker Compose
- OpenAI API Key
- LangSmith API Key
- News API Key（オプション）
- Twitter API Keys（オプション）

### 1. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下の内容を設定してください：

```bash
# OpenAI API Key（必須）
OPENAI_API_KEY=your_openai_api_key_here

# LangSmith設定（必須）
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=news-twitter-agent

# News API Key（オプション）
NEWS_API_KEY=your_news_api_key_here

# Twitter API設定（オプション）
BEARER_TOKEN=your_bearer_token_here
X_API_KEY=your_x_api_key_here
X_API_SECRET_KEY=your_x_api_secret_key_here
ACCESS_TOKEN=your_access_token_here
ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

### 2. Dockerコンテナの起動

```bash
# コンテナをビルドして起動
docker-compose up --build

# バックグラウンドで実行する場合
docker-compose up --build -d
```

### 3. アクセス方法

コンテナが起動したら、以下のURLにアクセスしてください：

#### 🎨 LangSmith Studio（推奨）
```
https://smith.langchain.com/studio/?baseUrl=http://localhost:8000
```

#### 📚 API ドキュメント
```
http://localhost:8000/docs
```

#### 🔧 直接API呼び出し
```
http://localhost:8000/runs/stream
```

## 📋 利用可能なコマンド

```bash
# コンテナの起動
docker-compose up

# コンテナの停止
docker-compose down

# ログの確認
docker-compose logs -f

# コンテナ内でシェルを実行
docker-compose exec langgraph-app bash

# イメージの再ビルド（コード変更後）
docker-compose build --no-cache
```

## 🛠️ 開発

### ホットリロード

開発時は、ソースコードの変更が自動的に反映されます。コンテナを再起動する必要はありません。

### トラブルシューティング

#### ポートが使用中の場合
```bash
# ポート8000が使用中の場合は、docker-compose.ymlのportsを変更
ports:
  - "8001:8000"  # ホスト側のポートを8001に変更
```

#### 環境変数が読み込まれない場合
- `.env`ファイルがプロジェクトルートに存在することを確認
- ファイル名が正確に`.env`であることを確認（拡張子なし）

#### 依存関係の更新
```bash
# requirements.txtを更新した後
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## 📁 プロジェクト構成

```
├── Dockerfile              # Dockerイメージ定義
├── docker-compose.yml      # Docker Compose設定
├── requirements.txt        # Python依存関係
├── langgraph.json         # LangGraph設定
├── news_twitter_agent.py  # メインのエージェントコード
└── README.md              # このファイル
```

## 🔧 機能

このエージェントは以下の機能を提供します：

1. **ニュース取得**: NewsAPIを使用して最新ニュースを取得
2. **要約**: OpenAI GPT-4を使用してニュースを要約
3. **Twitter投稿**: Twitter APIを使用して要約を投稿

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します。

## 📞 サポート

問題が発生した場合は、以下の手順でデバッグしてください：

1. `docker-compose logs -f` でログを確認
2. `http://localhost:8000/docs` でAPIドキュメントを確認
3. 環境変数が正しく設定されているか確認
