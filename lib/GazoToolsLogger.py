'''
作成日: 2026年01月04日
作成者: tamate masayuki
機能: GazoTools 用のロギング設定・管理
'''
import logging
import os
from datetime import datetime
import logging.handlers

try:
    from lib.config_defaults import (
        DEFAULT_SMTP_SERVER, DEFAULT_SMTP_PORT, 
        DEFAULT_SENDER_EMAIL, DEFAULT_SENDER_PASSWORD, 
        DEFAULT_RECIPIENT_EMAIL, DEFAULT_ENABLE_EMAIL_LOGGING
    )
except ImportError:
    # デフォルト値がない場合のフォールバック
    DEFAULT_SMTP_SERVER = "smtp.gmail.com"
    DEFAULT_SMTP_PORT = 587
    DEFAULT_SENDER_EMAIL = ""
    DEFAULT_SENDER_PASSWORD = ""
    DEFAULT_RECIPIENT_EMAIL = ""
    DEFAULT_ENABLE_EMAIL_LOGGING = False



class LoggerManager:
    """ロギング設定を一元管理するクラス"""
    
    _loggers = {}
    _log_dir = "logs"
    _debug_mode = False
    
    @classmethod
    def setup(cls, debug_mode=False):
        """ロギングを初期化する
        
        Args:
            debug_mode (bool): デバッグモード有効時は詳細ログを出力
        """
        cls._debug_mode = debug_mode
        
        # ログディレクトリを作成
        if not os.path.exists(cls._log_dir):
            os.makedirs(cls._log_dir, exist_ok=True)
        
        # ハンドラの設定
        log_level = logging.DEBUG if debug_mode else logging.INFO
        
        # コンソールハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # ファイルハンドラ（エラーログ）
        error_log_path = os.path.join(
            cls._log_dir,
            f"error_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(error_log_path, encoding='utf-8')
        file_handler.setLevel(logging.WARNING)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        # メール通知ハンドラ (エラー以上)
        if DEFAULT_ENABLE_EMAIL_LOGGING and DEFAULT_SENDER_EMAIL and DEFAULT_RECIPIENT_EMAIL:
            try:
                smtp_handler = logging.handlers.SMTPHandler(
                    mailhost=(DEFAULT_SMTP_SERVER, DEFAULT_SMTP_PORT),
                    fromaddr=DEFAULT_SENDER_EMAIL,
                    toaddrs=[DEFAULT_RECIPIENT_EMAIL],
                    subject="[GazoTools] Error Report",
                    credentials=(DEFAULT_SENDER_EMAIL, DEFAULT_SENDER_PASSWORD),
                    secure=() # TSL使用
                )
                smtp_handler.setLevel(logging.ERROR)
                smtp_handler.setFormatter(file_formatter)
                root_logger.addHandler(smtp_handler)
                print("Email logging enabled.")
            except Exception as e:
                print(f"Failed to setup email logging: {e}")

    
    @classmethod
    def get_logger(cls, name):
        """特定のモジュール用ロガーを取得
        
        Args:
            name (str): モジュール名（通常は __name__）
        
        Returns:
            logging.Logger: ロガーインスタンス
        """
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            cls._loggers[name] = logger
        return cls._loggers[name]
    
    @classmethod
    def is_debug_mode(cls):
        """デバッグモードの状態を確認
        
        Returns:
            bool: デバッグモードが有効ならTrue
        """
        return cls._debug_mode
    
    @classmethod
    def enable_debug_mode(cls):
        """デバッグモードを有効にする"""
        cls._debug_mode = True
        for logger in cls._loggers.values():
            logger.setLevel(logging.DEBUG)
            for handler in logger.handlers:
                handler.setLevel(logging.DEBUG)
    
    @classmethod
    def disable_debug_mode(cls):
        """デバッグモードを無効にする"""
        cls._debug_mode = False
        for logger in cls._loggers.values():
            logger.setLevel(logging.INFO)
            for handler in logger.handlers:
                handler.setLevel(logging.INFO)


# グローバルロガーの初期化
def setup_logging(debug_mode=False):
    """ロギングシステムをセットアップ"""
    LoggerManager.setup(debug_mode=debug_mode)


def get_logger(name):
    """モジュール別ロガーを取得"""
    return LoggerManager.get_logger(name)
