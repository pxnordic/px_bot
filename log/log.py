import logging


def mylog(name, fname = 'myGlobalLog.log'):
    logger = logging.getLogger(name);
    logger.setLevel(logging.DEBUG)
    fhan = logging.FileHandler(fname)
    fhan.setLevel(logging.DEBUG)
    logger.addHandler(fhan)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhan.setFormatter(formatter)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    return logger