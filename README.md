# youtube-summarize

以下は、ローカル環境でプロジェクトを実行するための手順をマークダウン形式で書き直したものです。

プロジェクト実行手順

1. Python環境のセットアップ

以下のコマンドを使用して仮想環境を作成し、有効化します。

Linux/Mac

python -m venv venv
source venv/bin/activate

Windows

python -m venv venv
.\venv\Scripts\activate

2. 必要なパッケージのインストール

以下のコマンドで必要なパッケージをインストールします。

pip install streamlit google-api-python-client youtube_transcript_api google-generativeai supabase python-dotenv

3. 環境変数の設定

プロジェクトのルートディレクトリに.envファイルを作成し、以下の環境変数を設定します。

YOUTUBE_API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

	注意: 各環境変数のyour_***部分は、実際の値に置き換えてください。APIキーはそれぞれのサービス（YouTube, Google Cloud, Supabase）から取得してください。

4. アプリケーションの実行

以下のコマンドでアプリケーションを実行します。

streamlit run main.py

これでプロジェクトがローカル環境で実行できるようになります。