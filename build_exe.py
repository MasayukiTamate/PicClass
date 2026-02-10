import PyInstaller.__main__
import shutil
import os
import sys

# アプリ名
APP_NAME = "GazoTools"
SCRIPT_NAME = "GazoToolsApp.py"

print("Building GazoTools Executable...")

# PyInstaller の実行
# 注意: --exclude-module で指定したモジュールはEXEに含まれません。
# これにより、distフォルダにコピーした .py ファイルが優先して読み込まれるようになります。
PyInstaller.__main__.run([
    SCRIPT_NAME,
    '--name=%s' % APP_NAME,
    '--onedir',        # 1つのディレクトリにまとめる
    '--noconsole',     # コンソール画面を出さない (デバッグ時は外しても良い)
    '--clean',         # キャッシュクリア
    '--exclude-module=GazoToolsLogic',  # ロジックを除外
    # libパッケージ全体を除外（個別に指定する必要があるかもだが、まずはパッケージ指定でトライ）
    '--exclude-module=lib',
    # 必要に応じて追加のインポートを除外
    #'--exclude-module=PIL', # PILはEXEに含めたいので除外しない
    #'--exclude-module=tkinterdnd2', # これも含める
])

# ビルド後のディレクトリ
dist_dir = os.path.join('dist', APP_NAME)

if not os.path.exists(dist_dir):
    print("Error: Build failed, dist directory not found.")
    sys.exit(1)

# ロジックファイルとlibフォルダをコピー
print("Copying external logic files to dist folder...")

# GazoToolsLogic.py
try:
    shutil.copy('GazoToolsLogic.py', dist_dir)
    print(" - Copied GazoToolsLogic.py")
except Exception as e:
    print(f"Error copying GazoToolsLogic.py: {e}")

# libフォルダ
lib_dest = os.path.join(dist_dir, 'lib')
try:
    if os.path.exists(lib_dest):
        shutil.rmtree(lib_dest)
    shutil.copytree('lib', lib_dest)
    print(" - Copied lib folder")
except Exception as e:
    print(f"Error copying lib folder: {e}")

# 不要な__pycache__を削除
for root, dirs, files in os.walk(lib_dest):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
            print(f" - Removed __pycache__ from {root}")

print("-" * 30)
print(f"Build complete! Executable is in: {os.path.abspath(dist_dir)}")
print("Run GazoTools.exe to start.")
print("-" * 30)
