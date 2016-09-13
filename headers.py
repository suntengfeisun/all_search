# -*- coding: utf-8 -*-

import platform
import random
from config import Config


class Headers:
    @staticmethod
    def getHeaders():
        if 'Windows' in platform.system():
            headers_path = ''
        else:
            headers_path = Config.headers_path
        userAgentFile = open(headers_path + 'user_agent_list.txt', 'r')
        userAgentList = []
        for line in userAgentFile:
            userAgentList.append({
                'User-Agent': line.strip(),
                'Referer': Config.headers_referer
            })
        userAgentFile.close()
        userAgent = random.sample(userAgentList, 1)
        return userAgent[0]
