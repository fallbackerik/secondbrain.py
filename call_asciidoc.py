import sys

from asciidoc import asciidoc
import argparse

def main() -> None:
  """ use more core asciidoc functionality
  """
  

  parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

  parser.add_argument('-i', '--infiles')
  parser.add_argument("-v", "--verbose")

  args = parser.parse_args()
  print("call asciidoc", args)
  
  asciidoc.cli(['./call_asciidoc.py', '--verbose', '--out-file=web/index.html', 'index.adoc'])
  
  # from the asciidoc codebase, these are the args asciidoc is looking for:
  # argv=['attribute=', 'backend=', 'conf-file=', 'doctype=', 'dump-conf',
  # 'help', 'no-conf', 'no-header-footer', 'out-file=',
  # 'section-numbers', 'verbose', 'version', 'safe', 'unsafe',
  # 'doctest', 'filter=', 'theme=']

if __name__ == '__main__':
  main()
