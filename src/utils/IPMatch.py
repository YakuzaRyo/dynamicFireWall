import re
from datetime import datetime
import json
import logging
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别
    format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/match.log', mode='a', encoding='utf-8'),  # 文件处理器
        logging.StreamHandler()  # 控制台处理器
    ]
)
logger = logging.getLogger("IPMatch")
logger.critical("模块加载")

class IPMatch:
    def __init__(self):
        # 增加异常处理防止空文件
        try:
            self.results = json.load(open('src/config/BanList.json', 'r', encoding='utf-8'))
        except (FileNotFoundError, json.JSONDecodeError):
            self.results = []
            with open('src/config/BanList.json', 'w', encoding='utf-8') as f:
                json.dump(self.results, f)
        self.rules = json.load(open('src/config/RULES.json', 'r', encoding='utf-8'))
        self.log_path = "logs/access.log"
        self.extract_ips_with_keywords()

    def extract_ips_with_keywords(self):
        """
        提取包含指定关键词的日志行中的IP地址
        参数:
            log_path (str): 日志文件路径
            keywords (list): 需要匹配的关键词列表
            output_file (str): 输出文件路径(可选)
        """
        # 复合正则模式：同时匹配IPv4和带端口的情况
        ip_pattern = re.compile(
            r'\b(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?\b'
        )

        line_count = 0
        try:
            with open(self.log_path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    line_count += 1
                    line = line.strip()

                    # 同时检查所有关键词（OR逻辑）
                    if any(keyword in line for keyword in self.rules):
                        match = ip_pattern.search(line)
                        if match:
                            ip = match.group('ip')
                            # 添加IP去重检查
                            existing_ips = [entry[0] for entry in self.results]
                            if ip not in existing_ips:
                                self.results.append((ip,0, f"tag_time:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}","execute_time"))
                            # (status:是否banned, tag_time:上名单时间, execute_time:执行时间)

            logger.info(f"分析完成，共处理 {line_count} 行日志")
            try:
                with open("src/config/BanList.json", "w", encoding="utf-8") as a:
                    json.dump(self.results, a, ensure_ascii=False)  # 修正变量名错误
                    a.close()
                    logger.info("BanList Added")
            except Exception as e:
                logger.error(f"Error: {e}")

        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
