import sys
import os
import os.path

from asciidoc import asciidoc
import argparse

def main() -> None:
  """ use more core asciidoc functionality
  """
  

  parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

  parser.add_argument('-i', '--infiles', type=str, nargs='+')
  parser.add_argument("-v", "--verbose", action='store_true')

  args = parser.parse_args()
  print("call asciidoc", args)
  sys.stdout.flush()

  for file in args.infiles:
    filepath, filename = os.path.split(file)
    fname_wo_ending = filename.split(".")[0]
    out_path = os.path.join("web", filepath)
    if not os.path.isdir(out_path):
      os.mkdir(out_path)
    inner_argv = [sys.argv[0], "--verbose", f"--out-file={os.path.join(out_path, fname_wo_ending)}.html", file]
    print(f"send file {file} to asciidoc with inner argv:", inner_argv)
    sys.stdout.flush()
    try:
      asciidoc.cli(inner_argv)
    except Exception as ex:
      print("!!!!!! EXCEPTION:", ex)
      sys.stdout.flush()
    except Error as er:
      print("!!!!!! ERROR:", er)
      sys.stdout.flush()
  
  # from the asciidoc codebase, these are the args asciidoc is looking for:
  # argv=['attribute=', 'backend=', 'conf-file=', 'doctype=', 'dump-conf',
  # 'help', 'no-conf', 'no-header-footer', 'out-file=',
  # 'section-numbers', 'verbose', 'version', 'safe', 'unsafe',
  # 'doctest', 'filter=', 'theme=']

if __name__ == '__main__':
  main()
