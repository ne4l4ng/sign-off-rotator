"""Unit test for SignOffRotater.py"""
import unittest
from binhex import openrsrc

import SignOffRotator
import fileinput
import yaml
import logging
import logging.config
import datetime

logConfig = yaml.safe_load(open('/projects/SignOffRotator/logging.yaml'));
logging.config.dictConfig(logConfig);

# create log
log = logging.getLogger("SignOffRotatorTest");

class SignOffRotatorTest(unittest.TestCase):

  def testRotateSignOff(self):
      filename = "sign-off.html";
      replacementString = "{{ signoff }}";
      SignOffRotator.main(filename);
      try:
        a_file = open("sign-off.html", 'r',encoding='UTF-8');
        self.assertFalse(replacementString in a_file,"%s should be replaced by quoted message in file %s" % (replacementString, filename));
      except IOError:
        log.exception("cannot open %s" % a_file);
      finally:
        a_file.close();

  def testDate(self):
      today = datetime.datetime.now();
      log.debug("today = %s" % today.now());
      log.debug("week day of the week = %s" % datetime.date.today().strftime("%W"));

      weekNumber = today.isocalendar()[1]
      modOfWeekNumber = 11 %10
      log.debug("weeknumber = %i, mod of week number = %i" % (weekNumber, modOfWeekNumber) );


if __name__ == '__main__':
    unittest.main()