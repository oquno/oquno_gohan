# oquno-gohan

Home Assistant の炊飯器ステータスを監視し、状態に応じたメッセージを X (Twitter) に投稿する小さなスクリプトです。

## できること

- Home Assistant の `state` 変化を取得
- 「炊飯中」「保温」「完了」などの状態に応じたメッセージ投稿
- 前回状態をファイルに保存し、重複投稿を回避

## 必要なもの

- Python 3.12+
- Home Assistant の長期アクセストークン
- X (Twitter) API の各種キー

## セットアップ

```bash
uv sync
```

> `uv` の導入は公式ドキュメントを参照してください: https://docs.astral.sh/uv/

## 環境変数

以下の環境変数を `.env` などで設定してください。

### Home Assistant

- `HA_TOKEN` : 長期アクセストークン
- `HA_HOST` : Home Assistant のベース URL（例: `https://your-homeassistant.local`）
- `HA_DEVICE_ID` : 監視対象のエンティティ ID（例: `sensor.rice_cooker`）

### X (Twitter) API

- `X_CONSUMER_KEY`
- `X_CONSUMER_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

### 投稿メッセージ

- `RUNNING_MESSAGE`
- `READY_MESSAGE`
- `COMPLETE_MESSAGE`
- `KEEPWARM_MESSAGE`
- `KEEPWARM_END_MESSAGE`
- `CANCEL_MESSAGE`

## 使い方

```bash
python oquno_gohan.py
```

定期実行したい場合は cron などから呼び出してください。

## ファイル構成

- `oquno_gohan.py` : メインスクリプト
- `last_state.txt` : 最終状態の保存先
- `crontab.sh` : cron 用の簡易スクリプト

## 注意点

- API キーは漏洩しないように管理してください。
- X API の制限に注意してください。
