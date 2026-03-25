import os
import json
import logging
from typing import Dict, List

LOG_PATH = "config_scan.log"
REPORT_PATH = "report.json"
CONFIG_DIR = "configs"


def setup_logging() -> None:
    """配置日志系统，同时输出到文件和控制台
    初始化logging配置，设置日志级别为INFO，格式包含时间、日志级别和消息内容。并将日志同时写入到指定文件(config_scan.log)和控制台
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def parse_json_file(filepath: str) -> bool:
    """解析单个json文件，成功返回True，失败返回False

    Args:
        filepath (str): 文件路径

    Returns:
        bool: 文件解析结果
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
            return True
    except json.JSONDecodeError:
        logging.error(f"JSON格式错误：{filepath}")
    except PermissionError:
        logging.error(f"无权限读取：{filepath}")
    except Exception as e:
        logging.error(f"读取失败：{filepath} | {str(e)}")
    return False


def scan_config_folder(folder: str) -> Dict:
    """扫描配置文件，返回统计报告

    Args:
        folder (str): 文件夹

    Returns:
        Dict:统计结果
    """
    total = 0
    success = 0
    failed = 0
    failed_files: List[str] = []

    if not os.path.isdir(folder):
        logging.error(f"目录不存在：{folder}")
        return {"total": 0, "sucess": 0, "failed": 0, failed_files: []}
    for filename in os.listdir(folder):
        if not filename.endswith(".json"):
            continue
        total += 1
        if parse_json_file(os.path.join(folder, filename)):
            success += 1
            logging.info(f"解析成功：{filename}")
        else:
            failed += 1
            failed_files.append(filename)
    logging.info(f"扫描完成，总：{total},成功：{success},失败：{failed}")
    return {
        "total": total,
        "sucess": success,
        "failed": failed,
        "failed_files": failed_files,
    }


def save_report(report: Dict, path: str) -> None:
    """保存报告到json文件

    Args:
        report (Dict): 结果报告
        path (str): 结果要保存到的路径
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        logging.info(f"报告已保存：{path}")


def main():
    setup_logging()
    report = scan_config_folder(CONFIG_DIR)
    save_report(report, REPORT_PATH)


if __name__ == "__main__":
    main()
