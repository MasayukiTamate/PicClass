# エラー履歴 (error_hister.md)

## 2026-02-11 10:27
- **エラー**: `ModuleNotFoundError: No module named 'send2trash'` (ユーザー報告: "send2trach")
- **原因**: ゴミ箱への移動機能で使用している `send2trash` モジュールがインストールされていなかったのじゃ。
- **対処**: `pip install send2trash` を実行してインストールするのじゃ。
