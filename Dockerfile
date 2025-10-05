# Python 3.12の公式イメージを使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新と必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーして依存関係をインストール
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルをコピー
COPY . .

# ポート8000を公開（LangGraphのデフォルトポート）
EXPOSE 8000

# 環境変数ファイルの存在を確認（オプション）
# .envファイルがある場合は使用
COPY .env* ./

# 環境変数を設定して自動ブラウザ起動を有効化
ENV LANGGRAPH_STUDIO_URL=https://smith.langchain.com/studio/?baseUrl=http://localhost:8000

# LangGraph開発サーバーを起動
CMD ["langgraph", "dev", "--host", "0.0.0.0", "--port", "8000"]
