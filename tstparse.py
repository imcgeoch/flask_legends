from legends.dfparser.dfparser import parse
from pympler import tracker

tr = tracker.SummaryTracker()

parse('tst.xml', 'base', 0)
parse('tst2.xml', 'base', 1)

tr.print_diff()
