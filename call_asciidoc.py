import sys
from asciidoc import asciidoc

def main() -> None:
  """ use more core asciidoc functionality
  """
  print("call asciidoc")
  asciidoc.cli(sys.argv)
  # from the asciidoc codebase, these are the args asciidoc is looking for:
  # argv=['attribute=', 'backend=', 'conf-file=', 'doctype=', 'dump-conf',
  # 'help', 'no-conf', 'no-header-footer', 'out-file=',
  # 'section-numbers', 'verbose', 'version', 'safe', 'unsafe',
  # 'doctest', 'filter=', 'theme=']

if __name__ == '__main__':
  main()
