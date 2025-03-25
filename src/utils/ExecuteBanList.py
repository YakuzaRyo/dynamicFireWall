import json
import subprocess
from datetime import datetime
import logging
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别
    format='[%(asctime)s][%(name)s]%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/Execute.log', mode='a', encoding='utf-8'),  # 文件处理器
        logging.StreamHandler()  # 控制台处理器
    ]
)
logger = logging.getLogger("ExecuteBanList")
logger.critical("模块加载")


# 示例：屏蔽测试IP
class ExecuteBanList:
    def __init__(self):
        self.BanList = json.load(open('src/config/BanList.json', 'r', encoding='utf-8'))
        logger.info(f"load list from {self.BanList}")
        self.ips = []
        self.execute()

    def execute(self):
        if self.BanList:
            # 修改为遍历索引以便更新状态
            for index, v in enumerate(self.BanList):
                if v[1] == 0:
                    ip, _, tag_time = v[:3]
                    self.block_ip(ip, tag_time, index)  # 新增index参数
        try:
            with open("src/config/BanList.json", "w", encoding="utf-8") as a:
                json.dump(self.BanList, a, ensure_ascii=False)  # 修正变量名错误
                a.close()
                logger.info("BanList Changed")
        except Exception as e:
            logger.error(f"Error: {e}")

    def block_ip(self, ip, tag_time, index):
        # 添加永久规则屏蔽指定IP
        cmd = f'firewall-cmd --permanent --add-rich-rule="rule family=ipv4 source address={ip} drop"'
        result = subprocess.run(cmd, shell=True, capture_output=True)

        if result.returncode == 0:
            # 重载防火墙使规则生效
            subprocess.run('firewall-cmd --reload', shell=True)
            logger.critical(f"成功屏蔽IP: {ip}")
            # 通过索引更新列表元素的状态位
            self.BanList[index] = (ip, 1, tag_time, f"execute_time:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
           logger.error(f"屏蔽失败: {result.stderr.decode()}")