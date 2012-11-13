import time
import re
from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException
# For help with what this is all about, see one of the sample
# Logster parsers which have more detailed comments about
# the structure of the class and each method's function.
# Collect arbitrary metric lines and spit out aggregated
# metric values (MetricObjects) based on the metric names
# found in the lines. Any conforming metric, one parser. Sweet.
class SumLogster(LogsterParser):
    def __init__(self, option_string=None):
        self.metrics = {}
        self.reg = re.compile('metric=(?P<metricname>[-_a-zA-Z0-9.]+) value=(?P<value>[0-9.]+)')
    def parse_line(self, line):
        try:
            regMatch = self.reg.search(line)
            if regMatch:
                linebits = regMatch.groupdict()
                metric = str(linebits['metricname'])
                value = int(linebits['value'])
                if self.metrics.has_key(metric):
                    self.metrics[metric] = self.metrics[metric] + int(value)
                else:
                    self.metrics[metric] = int(value)
            else:
                raise LogsterParsingException, "regmatch failed to match"
        except Exception, e:
            raise LogsterParsingException, "regmatch or contents failed with %s" % e
    def get_state(self, duration):
        self.duration = duration
        outlines = []
        for k in self.metrics.keys():
            outlines.append(MetricObject(k, self.metrics[k], "", "int"))
        return outlines
