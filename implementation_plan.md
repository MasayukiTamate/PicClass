# 実装計画: AI類似画像仕分け機能 (AI Visual Sort)

## 目標 (Goal Description)

IT企業向けのポートフォリオとして、AI（Smart Machine Learning）を活用した効率的な画像管理・運用を実現する機能を実装する。
具体的には、基準となる画像の下に、AIが探し出した類似画像を一覧表示し、直感的な操作で仕分け（移動・コピー・削除）ができるGUIを追加する。

## ユーザーレビュー事項 (User Review Required)
>
> [!IMPORTANT]
> **「AI Visual Sort」とは？**
> 本機能を**「AI Visual Sort」**と呼称を変更します。
> （旧称：SMLソート → ユーザーフィードバックにより改名）
> AIの検索結果を視覚的（Visual）に提示し、仕分け（Sort）を行うツールという意味を込めています。

## 変更提案 (Proposed Changes)

### GUI層 (GUI Layer)

#### [MODIFY] [lib/GazoToolsGUI.py](file:///k:/Syusyoku/PicClass/lib/GazoToolsGUI.py)

- **新規クラス**: `VisualSortWindow(Toplevel)`
  - **レイアウト**:
    - **上部フレーム (基準エリア)**:
      - 基準画像（ターゲット）を大きく表示。
      - 現在の画像パスや情報を表示。
    - **中部フレーム (操作エリア)**:
      - 類似度判定のスライダー（その場で調整可能）。
      - 「全選択/全解除」チェックボックス。
      - 実行ボタン群（「登録フォルダへ移動」「コピー」「ゴミ箱へ」など）。
      - ステータス表示（「検索時間: 0.05秒」「類似画像: 12枚」など、性能を可視化）。
    - **下部フレーム (結果エリア)**:
      - `ScrollableFrame` を使用。
      - 類似度が高い順に画像をタイル状、またはリスト状に表示。
      - 各画像の下に「類似度スコア（例: 98%）」を表示。
  - **機能**:
    - スライダー操作時にリアルタイム（または遅延実行）でリストを更新。
    - 画像クリックでプレビュー、ダブルクリックで拡大表示など。

### ロジック層 (Logic Layer)

#### [MODIFY] [GazoToolsLogic.py](file:///k:/Syusyoku/PicClass/GazoToolsLogic.py)

- **関数追加**: `open_visual_sort_window(target_path, app_state)`
  - バックグラウンドでベクトル検索を実行し、結果をGUIに渡す。
  - 移動・削除などのアクション実行時に、ファイル移動処理と同時にデータベース（`vectors.pkl`）の更新を行う。

### アプリケーション層 (Application Layer)

#### [MODIFY] [GazoToolsApp.py](file:///k:/Syusyoku/PicClass/GazoToolsApp.py)

- **メニュー追加**:
  - 画像の右クリックメニューに「AI Visual Sort」を追加。
  - メインメニューの「ツール」などにも追加。

## 検証計画 (Verification Plan)

### 手動検証 (Manual Verification)

1. **起動確認**: 画像を右クリックし、「AI Visual Sort」を選択してウィンドウが開くことを確認。
2. **表示確認**: 上に基準画像、下に類似画像が正しく表示されるか確認。
3. **スライダー動作**: 類似度スライダーを動かして、下のリストが増減することを確認。
4. **アクション**: 類似画像を選択して「移動」を実行し、実際にファイルが移動されるか、リストから消えるか確認。
5. **パフォーマンス**: 多数の画像があるフォルダで、検索や表示がスムーズか確認（プログレスバーなどが機能するか）。

# 実装計画: コンセプト説明書の作成 (Concept Documentation)

## 目標 (Goal Description)

アプリの利用者に対し、機能だけでなく「どのような思想で作られたか」「どのような体験を提供するのか」を伝えるためのコンセプト説明書を作成する。
これにより、ポートフォリオとしての価値を高め、開発者の意図を明確に伝える。

## 成果物 (Deliverables)

### [NEW] [concept.md](file:///k:/Syusyoku/PicClass/concept.md)

- **構成案**:
    1. **アプリ名 & キャッチコピー**: 一言でアプリを表す言葉。
    2. **Mission (ミッション)**: 開発の動機と目的。
    3. **Core Values (3つの核)**:
        - **Intuitive (直感)**: 思考を止めないUI。
        - **Intelligence (知能)**: AIによる強力な支援。
        - **Joy (楽しさ)**: 使うこと自体の喜び。
    4. **Key Features (主要機能の紹介)**: コンセプトに紐づいた機能説明。
    5. **Target Audience (想定ユーザー)**: どのような人に使ってほしいか。
    6. **Future Vision (展望)**: 今後の進化について。

## 検証計画 (Verification Plan)

- ユーザー（あなた）によるレビューとフィードバック。
- わかりやすい言葉選びと、Markdownによる視覚的な構成。

# 実装計画: 実行ファイル化と部分アップデート対応 (Executable Build & Partial Update)

## 目標 (Goal Description)

アプリケーションを実行ファイル(EXE)化し、Python環境がないPCでも動作するようにする。
また、**「部分的なアップデートを可能にする」**という要望に応えるため、重要なロジックファイル（`GazoToolsLogic.py` や `lib/` 以下のモジュール）をEXE内にバンドルせず、外部ファイルとして配置する構成を採用する。これにより、ロジック変更時に巨大なEXE全体を再配布する必要がなくなり、スクリプトファイルの差し替えだけでアップデートが可能になる。

## 成果物 (Deliverables)

### [NEW] [build_exe.py](file:///k:/Syusyoku/PicClass/build_exe.py)

- PyInstaller を実行するビルドスクリプト。
- **戦略**: `--onedir` モードを使用。
- **除外設定**: `lib` パッケージと `GazoToolsLogic` モジュールをビルドから除外し、手動コピーする処理を含める。
- **成果物**: `dist/GazoTools/` フォルダ（EXE + `lib/` + `GazoToolsLogic.py` + 依存DLL等）。

### [MODIFY] [GazoToolsApp.py](file:///k:/Syusyoku/PicClass/GazoToolsApp.py)

- 実行ファイル化された際、自身のディレクトリ（`dist/GazoTools/`）を `sys.path` に追加し、外部にある `lib` や `GazoToolsLogic.py` を正しくインポートできるようにする。

## 検証計画 (Verification Plan)

1. ビルドスクリプトを実行し、エラーなく完了することを確認。
2. 生成された `dist/GazoTools/GazoTools.exe` を実行し、アプリが起動することを確認。
3. **部分アップデート検証**:
    - `dist/GazoTools/lib/GazoToolsGUI.py` などを直接編集（例: ウィンドウタイトルを変更）。
    - アプリを再起動し、変更が反映されていることを確認（＝外部ファイルを読み込んでいることの証明）。
