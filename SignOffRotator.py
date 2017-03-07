import sys;
import getopt;
import yaml;
import logging;
import logging.config;
import datetime;

logConfig = yaml.safe_load(open('/projects/SignOffRotator/logging.yaml'));
logging.config.dictConfig(logConfig);
# create log
log = logging.getLogger("SignOffRotator");

cfg = yaml.safe_load(open('/projects/SignOffRotator/config.yaml'))
quotes = cfg['quotes']

from jinja2 import Environment, PackageLoader

def main(argv):
    inputfile = '';
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="]);
    except getopt.GetoptError:
        print ('SignOffRotator.py -i <inputfile>');
        sys.exit(2);
    for opt, arg in opts:
      if opt == '-h':
         print ('SignOffRotator.py -i <inputfile>');
         sys.exit();
      elif opt in ("-i", "--ifile"):
          inputfile = arg;

    if inputfile is None or inputfile == "":
        print ('SignOffRotator.py -i <inputfile>');
        sys.exit(2);

    log.info('Input file is  %s' % inputfile);

    env = Environment(loader=PackageLoader('SignOffRotator', 'templates'))
    template = env.get_template('sign-off_template.html');
    weekNumber = datetime.datetime.now().isocalendar()[1];
    log.debug("weekNumber = %i" % weekNumber);
    quoteIndex = weekNumber % 10;
    log.debug("quoteIndex to use = %i" % quoteIndex);
    log.info("quote to use = %s" % quotes[quoteIndex]);

    if quoteIndex > len(quotes):
        log.warn("quoteIndex out of bounds, resetting to 0");
        quoteIndex = 0;

    try:
        f = open(inputfile, 'w');
        f.write(template.render(signoff=quotes[quoteIndex]));
        log.info("Done.");
    except IOError:
        log.exception("cannot open %s" % f);
        sys.exit(1);
    finally:
        f.close();

    sys.exit(0);

if __name__ == '__main__':
    main(sys.argv[1:])
