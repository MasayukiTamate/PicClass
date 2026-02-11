# GazoTools (PicClass)


## 最初に

PicClass.zipをダウンロードしてください。
PicClass.zipのリンクをクリックしてページを移動後に中央のView rawをクリックしてください。




**「整理を、クリエイティブな体験へ。」**

GazoToolsは、大量の画像を効率的に整理・閲覧するためのデスクトップアプリケーションです。
直感的なドラッグ&ドロップ操作と、AIによる類似画像検出で、画像の仕分け作業を楽しく快適にします。

## 主な機能

### マルチウィンドウ画像ビューア
- フォルダ一覧・ファイル一覧・画像プレビューの3画面構成
- フローティングウィンドウで複数画像を同時表示
- タイル表示（Ctrl+T）で一覧比較

### ドラッグ&ドロップによる仕分け
- 最大12個の移動先フォルダを登録
- 画像をD&Dするだけで瞬時にファイル移動
- 複数ファイルの一括移動にも対応

### AI Visual Sort（視覚的仕分け）
- MobileNetV3による画像の特徴ベクトル抽出
- 類似画像を自動検出し、まとめて移動・コピー・削除
- 類似度の閾値をスライダーで直感的に調整

### 評価・タグ付け
- 画像に1〜6段階の星評価を付与
- 自由なテキストタグで画像を分類
- 評価・タグはファイルのハッシュ値に紐づけて永続保存

### ベクトル解析の可視化
- AIが画像をどう認識しているかを可視化
- 色彩・エッジ・テクスチャ・形状・セマンティック特徴を表示

### その他
- スクリーンセーバー / スライドショー機能（AI類似度順再生対応）
- CPU・メモリ使用量のリアルタイム表示
- ウィンドウ配置・設定の自動保存・復元

## 技術スタック

| カテゴリ | 技術 |
|:---|:---|
| 言語 | Python 3.8+ |
| GUI | tkinter + tkinterdnd2 |
| AI | PyTorch + torchvision (MobileNetV3 Small) |
| 画像処理 | Pillow (PIL) |
| システム監視 | psutil |
| 配布 | PyInstaller |

## セットアップ

### 必須ライブラリのインストール

```bash
pip install Pillow tkinterdnd2 psutil torch torchvision numpy send2trash
```

PyTorchのインストールで問題がある場合は [PyTorch公式](https://pytorch.org/get-started/locally/) を参照してください。

### 動作確認

```bash
python -c "import PIL, psutil, tkinterdnd2, torch, torchvision, numpy, send2trash; print('OK')"
```

### 起動

```bash
python GazoToolsApp.py
```

## 操作方法

| 操作 | 説明 |
|:---|:---|
| Space | ランダムに画像を表示 |
| Ctrl+T | 画像をタイル状に整列 |
| Ctrl+R | 全ての画像ウィンドウを閉じる |
| Ctrl+E | エクスプローラーで開く |
| Ctrl+I | 情報ウィンドウの表示切替 |
| Ctrl+F | メインウィンドウをフォーカス |
| Escape | スクリーンセーバーを停止 |

## プロジェクト構成

```
GazoToolsApp.py       # メインアプリケーション (UI)
GazoToolsLogic.py     # ビジネスロジック
lib/
  GazoToolsAI.py      # AI エンジン (MobileNetV3)
  GazoToolsData.py    # データ I/O (JSON)
  GazoToolsState.py   # アプリケーション状態管理
  GazoToolsGUI.py     # 再利用可能なGUIコンポーネント
  GazoToolsImageCache.py  # 画像キャッシュ (LRU)
  GazoToolsLib.py     # ファイル操作ユーティリティ
  config_defaults.py  # 定数・デフォルト値
```

## ターゲットユーザー

- **クリエイター** - 資料収集やアイデア整理で大量の画像を扱う方
- **コレクター** - 推し活や趣味の画像を体系的に管理したい方
- **データサイエンティスト** - 画像データセットの整理やAI認識の確認に

## ライセンス

作成者: tamate masayuki
