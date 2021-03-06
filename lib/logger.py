from datetime import datetime
import os

os.system("") # init color system

class LevelStyles():
    ## 1 if bold else 0;color
    info_color = "0;37m"
    success_color = "1;32m"
    warning_color = "1;33m"
    error_color = "1;31m"

class Logger():
    pref = "\033["
    reset = f"{pref}0m"

    def __init__(self, *, file_path=None):
        self.file_path = f"logs/{file_path}"
        if not file_path:
            self.file_path = f"logs/{datetime.now().strftime('%m%d%H%M%S')}.log"
        self.log_file = open(self.file_path, "w", encoding="utf-8")

    def write_log(self, text):
        self.log_file.write(text + "\n")
        self.log_file.flush()
        os.fsync(self.log_file.fileno())

    def success(self, text):
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        format_str = f"{nowtime} (SUCCESS) : {text}"
        self.write_log(format_str)
        print(f'{self.pref}{LevelStyles.success_color}{format_str}{self.reset}')

    def info(self, text):
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        format_str = f"{nowtime} (INFO) : {text}"
        self.write_log(format_str)
        print(f'{self.pref}{LevelStyles.info_color}{format_str}{self.reset}')

    def warning(self, text):
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        format_str = f"{nowtime} (WARNING) : {text}"
        self.write_log(format_str)
        print(f'{self.pref}{LevelStyles.warning_color}{format_str}{self.reset}')

    def error(self, text):
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        format_str = f"{nowtime} (ERROR) : {text}"
        self.write_log(format_str)
        print(f'{self.pref}{LevelStyles.error_color}{format_str}{self.reset}')

if __name__ == "__main__":
    logger = Logger()
    logger.success("Success Test")
    logger.info("Info Test")
    logger.warning("Warning Test")
    logger.error('Error Test')
    print("Reset test")
