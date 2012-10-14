# -*- coding: utf-8 -*-


def initlog():
    import logging
    
    logger = logging.getLogger()
    
    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler('D:/Python27/log5/doulist.log')  
    fh.setLevel(logging.NOTSET)  
      
    # 再创建一个handler，用于输出到控制台  
    ch = logging.StreamHandler()  
    ch.setLevel(logging.NOTSET)  
      
    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s -- %(message)s')  
    fh.setFormatter(formatter)  
    ch.setFormatter(formatter)  
      
    # 给logger添加handler  
    logger.addHandler(fh)  
    logger.addHandler(ch)
    
    logger.setLevel(logging.NOTSET)
    
    return logger
    