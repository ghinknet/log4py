'''
Copyright Ghink © 2014 MIT
Website https://www.ghink.net/
Author Bigsk (https://www.xiaxinzhe.cn/)
See the copytight
'''
import os, time, shutil
from threading import Thread

__VERSION__ = (2, 1, 0)

class log(object):
   def __init__(self, workdir):
      '''
      Init vars and threads.
      '''
      self.FATAL = "FATAL"
      self.ERROR = "ERROR"
      self.WARN = "WARN"
      self.INFO = "INFO"
      self.__levelMap = {
         'FATAL': self.FATAL,
         'ERROR': self.ERROR,
         'WARN': self.WARN,
         'INFO': self.INFO
      }
      if type(workdir) != str:
         raise TypeError("Wrong type for param @workdir")
      self.workdir = workdir
      self.__logs = []
      if os.path.exists(os.path.join(workdir, "logs")) and os.path.isdir(os.path.join(workdir, "logs")):
         daemon = Thread(target = self.__daemon, name = "log4py-daemon")
         daemon.daemon = True
         daemon.start()
      else:
         try:
               os.makedirs(os.path.join(workdir, "logs"), exist_ok = True)
               daemon = Thread(target = self.__daemon, name = "log4py-daemon")
               daemon.daemon = True
               daemon.start()
         except:
               raise PermissionError("Failed to operate the log file! ")
   def __daemon(self):
      '''
      Guard thread for recording logs and archiving.
      '''
      workdir = os.path.abspath(os.path.join(self.workdir, "logs"))
      def archive(workdir):
         timeStamp = time.time()
         logsList = []
         for fname in os.listdir(workdir):
               if os.path.isfile(os.path.join(workdir, fname)):
                  logsList.append(os.path.join(workdir, fname))
         archiveList = []
         today = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
         # yesterday = time.strftime("%Y-%m-%d", time.localtime(timeStamp - 86400))
         flag = False
         for fname in logsList:
               if os.path.basename(fname) != "{}.logs".format(today) and os.path.splitext(fname)[-1] == ".logs":
                  archiveList.append(fname)
                  flag = True
         if flag:
               self.info("Archiving logs.")
               # Archive each log in independence zip file
               for fname in archiveList:
                  basename = os.path.basename(fname)
                  shutil.make_archive(os.path.join(workdir, os.path.splitext(basename)[0]), "zip", workdir, basename)
                  try:
                     os.remove(os.path.join(workdir, basename))
                  except:
                     pass

      Thread(target = archive, args = (workdir,), name = "log4py-archive").start()
      while True:
         timeStamp = time.time()
         today = time.strftime("%Y-%m-%d", time.localtime(timeStamp))
         while True:
               with open(os.path.join(workdir, "{}.logs".format(today)),"a+") as fb:
                  data, self.__logs = self.__logs, []
                  for log in data:
                     fb.write("[{}] [{}] {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log[0])), log[1], log[2]))
                  if today != time.strftime("%Y-%m-%d", time.localtime()):
                     break
               archive(workdir)
   def record(self, level = "INFO", *content, split = " ", output = True):
      '''
      Record logs.
      @*content: The content for your log
      @split: The split text for your each log
      @level: The level for your log level
      @output: Print the log or not
      '''
      temp = []
      for con in content:
         temp.append(str(con))
      content = split.join(temp)
      if type(level) != str or level not in self.__levelMap.values():
         raise TypeError("Wrong type for param @level")
      if type(output) != bool:
         raise TypeError("Wrong type for param @output")
      timeStamp = time.time()
      self.__logs.append((timeStamp, level.upper(), content))
      if output:
         print("[{}] [{}] {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp)), level.upper(), content))
   def info(self, *content, split = " ", output = True):
      '''
      Record logs for info level.
      @*content: The content for your log
      @split: The split text for your each log
      @output: Print the log or not
      '''
      temp = []
      for con in content:
         temp.append(str(con))
      content = split.join(temp)
      self.record("INFO", content, split = split, output = output)
   def warn(self, *content, split = " ", output = True):
      '''
      Record logs for warn level.
      @*content: The content for your log
      @split: The split text for your each log
      @output: Print the log or not
      '''
      temp = []
      for con in content:
         temp.append(str(con))
      content = split.join(temp)
      self.record("WARN", content, split = split, output = output)
   def error(self, *content, split = " ", output = True):
      '''
      Record logs for error level.
      @*content: The content for your log
      @split: The split text for your each log
      @output: Print the log or not
      '''
      temp = []
      for con in content:
         temp.append(str(con))
      content = split.join(temp)
      self.record("ERROR", content, split = split, output = output)
   def fatal(self, *content, split = " ", output = True):
      '''
      Record logs for fatal level.
      @*content: The content for your log
      @split: The split text for your each log
      @output: Print the log or not
      '''
      temp = []
      for con in content:
         temp.append(str(con))
      content = split.join(temp)
      self.record("FATAL", content, split = split, output = output)
      raise Exception(content)