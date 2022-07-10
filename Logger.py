import logging
import datetime


class Logger:

    def __init__(self, log_level=20, log_name='__name__', log_folder='./log/'):
        now = datetime.datetime.now()
        filename = log_folder + now.strftime('%Y%m%d_%H%M%S.log')
        logging.basicConfig(filename=filename,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=log_level)
        logger = logging.getLogger(log_name)
        logger.info('Initiated loging')


if __name__ == '__main__':
    logger = Logger(20, 'test')
    print('Test logging')
