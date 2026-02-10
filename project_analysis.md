# PicClass (GazoTools) プロジェクト分析レポート

**分析日**: 2026-02-10
**作成者**: tamate masayuki / Refactored by Antigravity
**プロジェクトパス**: `K:\Syusyoku\PicClass`

---

## 1. プロジェクト概要

**GazoTools** は、AI（MobileNetV3）を活用した画像整理・分類デスクトップアプリケーション。
tkinter + tkinterdnd2 によるGUIで、画像の閲覧・評価・タグ付け・類似画像検索・ドラッグ＆ドロップによるフォルダ移動を直感的に行える。

### コンセプト（3つの柱）
| 柱 | 内容 |
|---|---|
| **Intuitive（直感）** | D&D操作、シームレスなフォルダ・ファイル参照 |
| **Intelligence（知能）** | AI Visual Sort、ベクトル解析による類似画像検出 |
| **Joy（楽しさ）** | パズル配置、スプラッシュ画面、カスタマイズ性 |

---

## 2. ディレクトリ構成

```
PicClass/
├── GazoToolsApp.py          # メインアプリケーション（UIエントリーポイント）
├── GazoToolsLogic.py         # ビジネスロジック（画像表示制御・レイアウト計算）
├── config.json               # アプリ設定ファイル（自動保存）
├── build_exe.py              # EXE化ビルドスクリプト
├── benchmark_ai.py           # AIベンチマークスクリプト
├── runtime_checks.py         # ランタイムチェック
│
├── lib/                      # ライブラリモジュール群
│   ├── config_defaults.py        # 定数・デフォルト設定
│   ├── GazoToolsAI.py            # AI画像ベクトル化エンジン
│   ├── GazoToolsBasicLib.py      # 基本ユーティリティ関数
│   ├── GazoToolsData.py          # データ永続化層
│   ├── GazoToolsExceptions.py    # カスタム例外クラス群
│   ├── GazoToolsGUI.py           # GUIダイアログ群
│   ├── GazoToolsImageCache.py    # LRU画像キャッシュ
│   ├── GazoToolsLib.py           # ファイル・フォルダ操作
│   ├── GazoToolsLogger.py        # ログ管理
│   ├── GazoToolsState.py         # アプリ状態管理（シングルトン）
│   ├── GazoToolsUI.py            # UI部品（評価・情報ウィンドウ）
│   └── GazoToolsVectorInterpreter.py  # ベクトル意味解釈
│
├── data/                     # データファイル
│   ├── folder_32.png             # フォルダアイコン
│   ├── ratings.json              # 評価データ
│   ├── tagdata.csv               # タグデータ
│   └── vectordata.json           # ベクトルキャッシュ
│
├── above/                    # 旧バージョン・テスト用スクリプト
│   ├── flet_gazo006syoki.py
│   ├── GazoHakoTools.py
│   ├── GazoTest001.py ～ GazoTest003Ai.py
│   └── ...（計11ファイル）
│
├── tests/                    # テストスイート
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_file_operations.py
│   ├── test_integration.py
│   └── test_ui_state.py
│
├── docs/                     # ドキュメント群（計21ファイル）
│   ├── API_REFERENCE.md
│   ├── CONFIGURATION.md
│   ├── TESTING_GUIDE.md
│   └── ...
│
├── logs/                     # エラーログ
│   └── error_YYYYMMDD.log
│
├── concept.md                # コンセプト文書
├── manual.md / manual.html   # ユーザーマニュアル
└── task.md                   # タスク管理
```

---

## 3. アーキテクチャ

### レイヤー構成（MVC風）

```
┌─────────────────────────────────────────────┐
│              GazoToolsApp.py                │  ← エントリーポイント / UIコントローラー
│         （メインウィンドウ・メニュー）        │
├─────────────────────────────────────────────┤
│             GazoToolsLogic.py               │  ← ビジネスロジック
│  （GazoPicture / レイアウト計算 / Visual Sort）│
├──────────┬──────────┬───────────┬────────────┤
│  UI層    │  AI層    │ データ層  │ 状態管理   │
│ GUI.py   │ AI.py    │ Data.py   │ State.py   │
│ UI.py    │ Vector   │ ImageCache│            │
│          │ Interp.  │           │            │
├──────────┴──────────┴───────────┴────────────┤
│           共通ユーティリティ                  │
│   BasicLib / Lib / Logger / Exceptions       │
│              config_defaults                 │
└─────────────────────────────────────────────┘
```

---

## 4. 主要モジュール詳細

### 4.1 GazoToolsApp.py（メインアプリケーション）
- **行数**: 約1,470行
- **役割**: tkinterメインウィンドウの構築、メニューバー、D&Dエリア、イベントバインド
- **主要機能**:
  - スプラッシュ画面表示（起動時1.5秒）
  - フォルダ一覧ウィンドウ / ファイル一覧ウィンドウの生成
  - D&D移動先の登録・管理（最大12スロット）
  - CPU/メモリ使用率のリアルタイム表示（バックグラウンドスレッド）
  - スクリーンセーバーモード（自動再生）
  - キーボードショートカット（Space, Ctrl+F/R/E/T/I, Escape）

### 4.2 GazoToolsLogic.py（ビジネスロジック）
- **行数**: 約1,675行
- **役割**: 画像表示制御、ウィンドウレイアウト計算、評価・タグ管理
- **主要クラス**:
  - `GazoPicture` - 画像表示の中核クラス
    - `Drawing(fileName)` - 画像の表示（リサイズ・配置・ベクトル解析）
    - `TileWindows()` - パズル型タイル配置（二分木空間分割）
    - `CloseAll()` - 全画像ウィンドウ閉鎖
    - 評価ウィンドウ / 情報ウィンドウの管理
    - 右クリックメニュー（タグ編集・移動・類似検索・Visual Sort）

### 4.3 lib/GazoToolsAI.py（AIエンジン）
- **役割**: MobileNetV3を使った画像特徴ベクトル抽出
- **主要クラス**:
  - `VectorEngine`（シングルトン）- 1024次元の特徴ベクトル生成
    - `get_image_feature(path)` - 単一画像のベクトル化
    - `get_image_features_batch(paths)` - バッチ処理
    - `compare_features(v1, v2)` - コサイン類似度計算
  - `VectorBatchProcessor` - バックグラウンド一括ベクトル化
- **依存**: PyTorch, torchvision, Pillow

### 4.4 lib/GazoToolsData.py（データ永続化）
- **役割**: JSON/CSV形式での設定・タグ・評価・ベクトルデータの読み書き
- **主要関数**:
  - `load_config()` / `save_config()` - アプリ設定の永続化
  - `load_tags()` / `save_tags()` - タグデータ（CSV）
  - `load_ratings()` / `save_ratings()` - 評価データ（JSON）
  - `load_vectors()` / `save_vectors()` - ベクトルキャッシュ（JSON）
  - `calculate_file_hash(filepath)` - MD5ハッシュ（画像識別用）
- **主要クラス**:
  - `HakoData` - 画像ファイルリスト管理、ランダム選択、AI順序再生

### 4.5 lib/GazoToolsState.py（状態管理）
- **役割**: アプリ全体の状態をシングルトンで一元管理
- **管理項目**: フォルダ/ファイル情報、移動先スロット、UI表示設定、SS設定、ベクトル表示設定、ウィンドウ位置、画像サイズ制限、評価UI設定
- **特徴**: コールバック通知機能（Observer パターン）、`to_dict()` / `from_dict()` によるシリアライズ

### 4.6 lib/GazoToolsGUI.py（GUIダイアログ）
- **主要クラス**:
  - `SplashWindow` - 起動スプラッシュ（フェードイン＋豆知識）
  - `SimilarityMoveDialog` - 類似画像一括移動ダイアログ（閾値スライダー付き）
  - `VisualSortWindow` - AI Visual Sort ウィンドウ（グリッド表示＋仕分け）
  - `VectorWindow` - ベクトル解析情報表示ウィンドウ
  - `ScrollableFrame` / `RowWidget` - カスタムUI部品

### 4.7 lib/GazoToolsVectorInterpreter.py（ベクトル意味解釈）
- **役割**: 1024次元ベクトルを人間が読めるテキストに変換
- **解釈モード**: `labels`（トップN次元）、`shap`（貢献度ベース）、`custom`（拡張用）
- **カテゴリマッピング**（1024次元 → 5カテゴリ）:
  - 色彩 (0-251): 赤, 緑, 青, 明度, 彩度, 色相 等
  - エッジ (251-451): 水平線, 垂直線, 曲線, 複雑度 等
  - テクスチャ (451-751): 滑らか, 粗い, パターン, グラデーション 等
  - 形状 (751-921): 円, 四角, 三角, 対称性 等
  - セマンティック (921-1024): 動物, 植物, 風景, 建物, 人物 等

### 4.8 lib/GazoToolsImageCache.py（画像キャッシュ）
- **役割**: LRU方式の画像メモリキャッシュ（スライドショー・タイル表示の高速化）
- **主要クラス**:
  - `ImageCache`（シングルトン）- 最大256MBのLRUキャッシュ
  - `TileImageLoader` - タイル表示用ローダー
  - `SlideShowImageLoader` - スライドショー用先読みローダー

### 4.9 その他ユーティリティ

| モジュール | 役割 |
|---|---|
| `GazoToolsBasicLib.py` | ウィンドウサイズ変換、色ブレンド関数 |
| `GazoToolsLib.py` | フォルダ抽出 (`GetKoFolder`)、画像ファイル抽出 (`GetGazoFiles`) |
| `GazoToolsLogger.py` | ログ管理（コンソール＋日次ファイル出力） |
| `GazoToolsExceptions.py` | カスタム例外階層（11種類） |
| `config_defaults.py` | グローバル定数・バリデーション関数 |

---

## 5. データフロー

```
画像フォルダ選択
    ↓
GetKoFolder / GetGazoFiles でファイル列挙
    ↓
フォルダ一覧ウィンドウ / ファイル一覧ウィンドウに表示
    ↓
ダブルクリック or Space で画像表示
    ↓
GazoPicture.Drawing()
  ├── Image.open() → リサイズ → tkinter Canvas 表示
  ├── calculate_file_hash() → MD5ハッシュ計算
  ├── VectorEngine → 1024次元ベクトル取得（キャッシュ or リアルタイム計算）
  ├── VectorInterpreter → ベクトルの意味解釈テキスト生成
  ├── 評価ウィンドウ更新（星＋評価名）
  └── 情報ウィンドウ更新（ファイル名・サイズ・タグ・評価・ベクトル）
    ↓
D&D or 右クリック → ファイル移動 / 類似画像検索 / Visual Sort
    ↓
設定・タグ・評価・ベクトルデータの自動保存（JSON/CSV）
```

---

## 6. 主な技術スタック

| カテゴリ | 技術 |
|---|---|
| **言語** | Python 3.10 - 3.13 |
| **GUI** | tkinter + tkinterdnd2（D&D対応） |
| **画像処理** | Pillow (PIL) |
| **AI/ML** | PyTorch + torchvision（MobileNetV3） |
| **システム監視** | psutil（CPU/メモリ） |
| **ファイル操作** | shutil, send2trash |
| **Windows API** | ctypes（ワークエリア取得） |
| **データ形式** | JSON（設定・評価・ベクトル）、CSV（タグ） |
| **ハッシュ** | MD5（画像一意識別） |

---

## 7. 主要機能一覧

### 画像閲覧
- 画像ウィンドウ表示（アスペクト比維持リサイズ）
- ランダム位置/サイズ表示
- パズル型タイル配置（画面敷き詰め）
- スクリーンセーバーモード（自動再生）
- ドラッグ移動可能な画像ウィンドウ

### 画像整理
- D&Dによるフォルダ移動（最大12スロット）
- 右クリックメニューからの移動・名前変更
- AI類似画像検索（SimilarityMoveDialog）
- AI Visual Sort（視覚的一括仕分け）
- バッチファイル移動

### AI機能
- MobileNetV3による1024次元特徴ベクトル抽出
- コサイン類似度による類似画像検出
- ベクトルの意味解釈（5カテゴリ: 色彩・エッジ・テクスチャ・形状・セマンティック）
- オンデマンド/自動ベクトル計算
- バックグラウンド一括ベクトル化

### メタデータ管理
- タグ付け（セミコロン区切り）
- 6段階星評価システム（名前付き評価＋連動/固定モード）
- 画像情報ウィンドウ（ファイル名・サイズ・タグ・評価・ベクトル解釈）

### 設定・カスタマイズ
- ウィンドウ位置・サイズの記憶
- CPU負荷に応じたステータスバー色変化
- 評価UIのサイズ・位置・フォント・レイアウト順序
- 画像表示サイズの最小/最大設定
- ベクトル表示のカテゴリ別ON/OFF
- スプラッシュ画面の豆知識表示ON/OFF

### キーボードショートカット

| キー | 機能 |
|---|---|
| `Space` | ランダム画像表示 |
| `Ctrl+F` | メインウィンドウにフォーカス |
| `Ctrl+R` | 全画像ウィンドウを閉じる |
| `Ctrl+E` | エクスプローラーで開く |
| `Ctrl+T` | タイル配置 |
| `Ctrl+I` | 情報ウィンドウ表示/非表示 |
| `Escape` | スクリーンセーバー停止 |

---

## 8. ファイル統計

| 区分 | ファイル数 | 主な拡張子 |
|---|---|---|
| メインソース | 2 | .py |
| ライブラリ | 12 | .py |
| テスト | 9 | .py |
| 旧バージョン/テスト | 11 | .py |
| ドキュメント | 21+ | .md, .html, .text |
| データ | 4 | .json, .csv, .png |
| ログ | 4 | .log |
| 設定 | 1 | .json |
| **合計** | **約64ファイル** | |

---

## 9. 設計上の特徴

1. **シングルトンパターン**: `AppState`, `VectorEngine`, `ImageCache` で状態・リソースを一元管理
2. **Observerパターン**: `AppState` のコールバック通知で UI 自動更新
3. **EXE化対応**: `sys.frozen` 判定で外部スクリプト差し替えによるアップデート可能
4. **バックグラウンド処理**: AI計算・リソース監視をスレッドで非同期実行
5. **LRUキャッシュ**: メモリ上限付き画像キャッシュで高速表示
6. **ハッシュベース管理**: MD5ハッシュで画像を一意識別（ファイル名変更に強い）

---

*このレポートは PicClass プロジェクトの全ファイルを分析して自動生成されました。*
