import logging
import os
from datetime import datetime

# 输入/输出目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOGS = os.path.join(BASE_DIR, "logs")


def logging_init(logger_name: str, log_dir: str = LOGS) -> logging.Logger:
    """初始化日志配置

    Args:
        logger_name (str): 日志器名称
        log_dir (str, optional): 日志文件夹路径. Defaults to "log".

    Returns:
        logging.Logger: 配置好的logger实例
    """
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError as e:
        print(f"创建日志文件夹失败：{e}")
        raise
    log_file = os.path.join(
        log_dir, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
    except OSError as e:
        print(f"创建日志文件失败：{e}")
        raise

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def process_single_file(input_file_path: str, output_file_path: str) -> bool:
    """处理单个文件

    Args:
        input_file_path (str): 要处理的文件所在路径
        output_file_path (str): 文件清洗完后要放在哪个路径

    Returns:
        bool: 文件是否成功清洗的返回值,True则成功,False则失败
    """
    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        total_lines = len(lines)
        cleaned_lines = 0
        total_words = 0
        total_chars = 0
        cleaned_chars = 0
        cleaned_lines_list = []
        for line in lines:
            total_words += len(line.split())
            total_chars += len(line)
            stripped = line.strip()
            if stripped:
                cleaned_lines += 1
                cleaned_chars += len(stripped)
                cleaned_lines_list.append(stripped)
        logger.info(f"""{input_file_path}文件读取成功:
            原始总行数:{total_lines},单词数：{total_words},字符数：{total_chars}
            清洗后的行数:{cleaned_lines},字符数：{cleaned_chars}""")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines_list))
        return True
    except FileNotFoundError:
        logger.error(f"{input_file_path}文件不存在")
    except PermissionError:
        logger.error("权限不足，无法读写")
    except Exception as e:
        logger.error(f"处理失败：{str(e)}", exc_info=True)
    return False


def batch_process():
    """批量处理文件"""
    if not os.path.exists(INPUT_DIR):
        logger.error(f"输入目录{INPUT_DIR}不存在")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    success = 0
    fail = 0
    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(".txt"):
            if process_single_file(
                os.path.join(INPUT_DIR, file), os.path.join(OUTPUT_DIR, file)
            ):
                success += 1
            else:
                fail += 1

    if success > 0 or fail > 0:
        logger.info(f"处理完成，成功:{success},失败:{fail}")
    else:
        logger.info("不存在.txt文件")


if __name__ == "__main__":
    logger = logging_init("day7_logging")
    batch_process()
