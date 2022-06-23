class Log:

    from datetime import datetime
    import os.path

    # Variables
    current_file = None
    current_file_length = 0
    log_file = None

    def __init__(self, path="./", log_max_size=100):
        self.path = path
        self.log_max_size = log_max_size
        self.set_current_file_name()
        self.open_file()

    def get_current_time(self):
        now = self.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def set_current_file_name(self):
        """
        Create filename based on datetime and a counter.
        If file exists, add counter and try again.
        """
        now = self.datetime.now()
        counter = 0
        found_viable_name = False
        while not found_viable_name:
            self.current_file = self.path + now.strftime("%Y-%m-%d %H:%M:%S") + "_" + str(counter) + ".log"
            if not self.os.path.exists(self.current_file):
                break
            counter = counter + 1

    def open_file(self):
        self.log_file = open(self.current_file, "w")
        self.current_file_length = 0

    def close_file(self):
        self.log_file.close()

    def new_file(self):
        self.close_file()
        self.set_current_file_name()
        self.open_file()

    def add_line(self, process_name, line):
        write_line = self.get_current_time() + ' | ' + process_name + ' | ' + line + '\n'
        self.log_file.write(write_line)
        self.current_file_length = self.current_file_length + 1
        if self.current_file_length == self.log_max_size:
            self.new_file()


