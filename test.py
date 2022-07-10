
class Test2:
    import logging

    def __init__(self):
        self.log = self.logging.getLogger("my-logger")


    def probeer(self):
        self.log.info("test2")

class Test1:

    import logging
    test2 = Test2()

    logging.basicConfig(filename='./log/test.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

    log = logging.getLogger("my-logger")
    log.info("test 1")
    test2.probeer()
    print(str(logging.INFO))
    print(__name__)

