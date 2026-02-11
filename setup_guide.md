# 環境構築手順書

## 概要
このドキュメントは、GazoToolsアプリケーションを動作させるために必要な環境構築手順をまとめたものなのじゃ。

## 必要要件
- OS: Windows 10/11
- Python: 3.8 以上

## 必須ライブラリ
以下のライブラリが必要じゃ。

| ライブラリ名 | 用途 |
| --- | --- |
| `Pillow` | 画像処理 (表示、加工) |
| `tkinterdnd2` | ドラッグ＆ドロップ機能 |
| `psutil` | システムリソース (CPU/メモリ) 監視 |
| `torch` | AI機能 (PyTorch本体) |
| `torchvision` | AI機能 (画像処理用モデル・変換) |
| `numpy` | 数値計算 (Tensor処理など) |
| `send2trash` | ファイル削除 (ゴミ箱へ移動) |

## インストール手順
コマンドプロンプトまたはPowerShellで以下のコマンドを実行するのじゃ。

```bash
python -m pip install Pillow tkinterdnd2 psutil torch torchvision numpy send2trash
```

## 動作確認
以下のコマンドを実行してエラーが出なければOKじゃ。

```bash
python -c "import PIL, psutil, tkinterdnd2, torch, torchvision, numpy, send2trash; print('OK')"
```

## トラブルシューティング
- `pip` コマンドが見つからない場合は、`python -m pip` を試すのじゃ。
- 権限エラーが出る場合は、管理者権限で実行するか、`--user` オプションを付けるのじゃ。
- PyTorch関連でエラーが出る場合は、[公式ページ](https://pytorch.org/get-started/locally/)を参照して環境に合ったコマンドを確認するのじゃ。
