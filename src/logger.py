import logging

def setup_logger():
    logger = logging.getLogger('VMwareLogger')
    logger.setLevel(logging.DEBUG)
    
    # Tạo console handler để ghi log ra màn hình
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # Tạo file handler để ghi log ra file
    fh = logging.FileHandler('vmware_log.log')
    fh.setLevel(logging.DEBUG)
    
    # Định dạng log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    # Thêm handler vào logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger

logger = setup_logger()