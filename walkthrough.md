# GazoTools アップデート報告

## 2026-02-11 更新内容

以下の機能追加と修正を行い、実行ファイル (EXE) を再構築したのじゃ！

### 1. 実行ファイル (EXE) 化
- Python環境がなくても動作する `GazoTools.exe` を作成したのじゃ。
- output: `dist/GazoTools/GazoTools.exe`
- 必要なライブラリ (`tkinterdnd2`, `send2trash`, `torch` 等) をすべて同梱したのじゃ。

### 2. 機能追加・改善
- **視覚的仕分け (Visual Sort) 改善**:
    - [x] 更新ボタンを追加 (再スキャン可能)
    - [x] ウィンドウ幅に合わせた列数の自動調整
- **ウィンドウサイズ修正**:
    - 配布時の初期ウィンドウサイズを `600x600` に変更したのじゃ。
- **エラーログ通知機能**:
    - エラー発生時に指定メールアドレス (`tamaya2473616@gmail.com`) へレポートを送信する機能を追加したのじゃ。
- **メモリ表示**:
    - ステータスバーに「アプリ使用メモリ」に加え、「システム空きメモリ」も表示するようにしたのじゃ。
    - 例: `CPU: 10%  App: 150MB  Free: 8192MB`

### 3. トラブルシューティング
- `ImportError: cannot import name 'ttk'` -> 修正済み
- `ModuleNotFoundError: No module named 'send2trash'` -> 修正済み

---
**確認方法**:
1. `dist/GazoTools/GazoTools.exe` をダブルクリックして起動するのじゃ。
2. ステータスバー（画面下部）にメモリ情報が表示されているか確認してほしいのじゃ。
