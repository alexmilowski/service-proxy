import sys
from codecs import iterdecode
from functools import partial
import re
import logging

def replaceuri(textiter,uri,replacement):

   exp = re.compile(re.escape(uri[0:16]))
   slen = len(uri)
   remaining = ''
   try:
      for text in textiter:
         value = remaining + text
         remaining = value[-slen:]
         end = len(value)-slen
         last = 0
         for match in exp.finditer(value):
               if match.start()>=end:
                  break
               if last!=match.start():
                  yield value[last:match.start()]
               if value[match.start():match.start()+slen]==uri:
                  last = match.start()+slen
                  yield replacement
         if last<end:
            yield value[last:end]
      yield remaining
   except Exception as ex:
      logging.exception('Drat! Halt and catch fire.')


if __name__ == '__main__':

   with open(sys.argv[1],'rb') as input:
      def bchunks():
         for chunk in iter(partial(input.read, 32*1024), b''):
            yield chunk

      def chunks(dataiter,encoding):
         for text in iterdecode(dataiter,encoding):
            yield text

      for text in replaceuri(chunks(bchunks(),'UTF-8'),sys.argv[2],sys.argv[3]):
         sys.stdout.write(text)
