from configparser import ConfigParser
import pymysql

class Config:
    # 配置文件
    CONFIG_FILE = 'app.conf'

    @staticmethod
    def mysql():
        """
        return config
        Args:
            key:

        Returns:

        """
        cp = ConfigParser()
        cp.read(Config.CONFIG_FILE)
        config = dict(cp.items('mysql'))
        config['port'] = cp.getint('mysql', 'port')
        config['cursorclass'] = pymysql.cursors.DictCursor
        return config

