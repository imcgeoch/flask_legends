from legends.dfparser.dfparser import parse
from pympler import tracker

tr = tracker.SummaryTracker()

parse('tst.xml', 0)

tr.print_diff()
