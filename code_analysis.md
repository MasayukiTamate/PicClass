# コード詳細分析 (code_analysis.md)

## 対象ファイル
- GazoToolsApp.py

## 概要
このファイルは「GazoTools」という画像ビューアアプリケーションのメインエントリーポイントであり、UI（Tkinter）の構築とイベント処理を担当しているのじゃ。

## 構造分析
### 1. インポートと初期化
- **標準ライブラリ**: os, sys, shutil, time, threading
- **UIライブラリ**: tkinter (filedialog, messagebox, simpledialog), tkinterdnd2 (D&D対応)
- **画像処理**: Pillow (Image, ImageTk)
- **システム監視**: psutil
- **自作モジュール**:
  - `lib.GazoToolsLogger`: ログ出力
  - `GazoToolsLogic`: コアロジック（設定管理、データ操作、画像処理）
  - `lib.GazoToolsImageCache`: 画像キャッシング
  - `lib.GazoToolsGUI`: UIコンポーネント（スプラッシュ画面など）

### 2. アプリケーションの状態管理
- `app_state = get_app_state()` で状態を一元管理している。
- `on_app_state_changed` コールバックにより、状態変化時にUIを自動更新する設計になっている（Observerパターン）。

### 3. UI構成
- **メインウィンドウ (`koRoot`)**: 画像表示エリア、D&Dターゲットエリア、ステータスバー。
- **フォルダ一覧ウィンドウ (`folder_win`)**: 左側のツリー構造に相当。
- **ファイル一覧ウィンドウ (`file_win`)**: フォルダ内の画像リスト。
- **スプラッシュ画面 (`SplashWindow`)**: 起動時に表示。

### 4. 機能詳細
- **画像表示**: `GazoPicture` クラス（`GazoControl` インスタンス）が担当。
- **スライドショー**: `auto_slideshow` 関数で定期的に画像を切り替え。AIによる画像選別機能 (`ss_ai_mode`) もあるようだが、詳細は `GazoToolsLogic` に委譲されている。
- **ファイル操作**: ファイル名の変更、フォルダ移動、タグ付けなどの機能がコンテキストメニューから利用可能。
- **リソース監視**: 別スレッドで `psutil` を使いCPUとメモリ使用率を監視し、ステータスバーに表示。CPU負荷に応じて背景色が変わる視覚的フィードバックがある。
- **設定保存**: アプリ終了時 (`on_closing_main`) に設定と評価データをJSON形式などで保存。

## 依存関係
外部ライブラリとして `Pillow`, `tkinterdnd2`, `psutil` が必須。

## コメント
全体的にモジュール化が進んでおり、LogicとUIの分離が意識されている。特に `AppState` を用いた状態管理は拡張性が高い良い設計じゃ。
今後の拡張（ログウィンドウなど）もこのパターンに従うのが望ましいのじゃ。
