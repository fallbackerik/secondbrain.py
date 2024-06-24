import sys
import os
import os.path

from asciidoc import asciidoc
from asciidoc.asciidoc import asciidoc as fasciidoc
from asciidoc.asciidoc import reset_asciidoc, config, usage
import argparse

def execute(cmd, opts, args):
    """ function is taken directly from the asciidoc-py source for experimentation
    """
    reset_asciidoc()
    config.init()
    if len(args) > 1:
        usage('Too many arguments')
        sys.exit(1)
    backend = None
    doctype = None
    confiles = []
    outfile = None
    options = []
    help_option = False
    for o, v in opts:
        if o in ('-b', '--backend'):
            backend = v
        if o in ('-c', '--dump-conf'):
            options.append('-c')
        if o in ('-d', '--doctype'):
            doctype = v
        if o in ('-e', '--no-conf'):
            options.append('-e')
        if o in ('-f', '--conf-file'):
            confiles.append(v)
        if o == '--filter':
            config.filters.append(v)
        if o in ('-n', '--section-numbers'):
            o = '-a'
            v = 'numbered'
        if o == '--theme':
            o = '-a'
            v = 'theme=' + v
        if o in ('-a', '--attribute'):
            e = parse_entry(v, allow_name_only=True)
            if not e:
                usage('Illegal -a option: %s' % v)
                sys.exit(1)
            k, v = e
            # A @ suffix denotes don't override existing document attributes.
            if v and v[-1] == '@':
                document.attributes[k] = v[:-1]
            else:
                config.cmd_attrs[k] = v
        if o in ('-o', '--out-file'):
            outfile = v
        if o in ('-s', '--no-header-footer'):
            options.append('-s')
        if o in ('-v', '--verbose'):
            options.append('-v')
    stdin, stdout = sys.stdin, sys.stdout
    try:
        infile = args[0]
        if infile == '-':
            infile = '<stdin>'
        elif isinstance(infile, str):
            infile = os.path.abspath(infile)
        else:   # Input file is file object from API call.
            sys.stdin = infile
            infile = '<stdin>'
        if outfile == '-':
           outfile = '<stdout>'
        elif isinstance(outfile, str):
           outfile = os.path.abspath(outfile)
        elif outfile is None:
            if infile == '<stdin>':
                outfile = '<stdout>'
        else:   # Output file is file object from API call.
            sys.stdout = outfile
            outfile = '<stdout>'
        # Do the work.
        fasciidoc(backend, doctype, confiles, infile, outfile, options)
        if document.has_errors:
            sys.exit(1)
    finally:
      sys.stdin, sys.stdout = stdin, stdout

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
    execute(__file__, inner_argv, [file])
    #try:
    #  execute(__file__, inner_argv, [file])
    #except Exception as ex:
    #  print("!!!!!! EXCEPTION:", ex)
    #  sys.stdout.flush()
  
  # from the asciidoc codebase, these are the args asciidoc is looking for:
  # argv=['attribute=', 'backend=', 'conf-file=', 'doctype=', 'dump-conf',
  # 'help', 'no-conf', 'no-header-footer', 'out-file=',
  # 'section-numbers', 'verbose', 'version', 'safe', 'unsafe',
  # 'doctest', 'filter=', 'theme=']

if __name__ == '__main__':
  main()
