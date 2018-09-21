"""
Reads the Airmar three times, probably was used for testing
"""

import airmar_reader as ar
import time

ar.print_airmar_sentence_contents = True

ar.setup()
ar.read_airmar()
time.sleep(1)
ar.read_airmar()
time.sleep(1)
ar.read_airmar()
