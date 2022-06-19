from Log import Log

log = Log()

for i in range(300):
    line = "line " + str(i)
    log.add_line(line)
    print(str(log.current_file_length))