import wibtex_parser
import logger

log = logger.SimpleLogger()

wibtex_parser.parse('demo_data/complete_bib.bib', log)