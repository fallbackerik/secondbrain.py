import sys
import os
import os.path

from asciidoc import asciidoc
from asciidoc.asciidoc import reset_asciidoc, config, usage, document, reader
from asciidoc.exceptions import EAsciiDoc
import argparse

def fasciidoc(backend, doctype, confiles, infile, outfile, options):
    """Convert AsciiDoc document to DocBook document of type doctype
    The AsciiDoc document is read from file object src the translated
    DocBook file written to file object dst."""
    def load_conffiles(include=[], exclude=[]):
        # Load conf files specified on the command-line and by the conf-files attribute.
        files = document.attributes.get('conf-files', '')
        files = [f.strip() for f in files.split('|') if f.strip()]
        files += confiles
        if files:
            for f in files:
                if os.path.isfile(f):
                    config.load_file(f, include=include, exclude=exclude)
                else:
                    raise EAsciiDoc('missing configuration file: %s' % f)
   
    document.attributes['python'] = sys.executable
    for f in config.filters:
        if not config.find_config_dir('filters', f):
            raise EAsciiDoc('missing filter: %s' % f)
    if doctype not in (None, 'article', 'manpage', 'book'):
        raise EAsciiDoc('illegal document type')
    # Set processing options.
    for o in options:
        if o == '-c':
            config.dumping = True
        if o == '-s':
            config.header_footer = False
        if o == '-v':
            config.verbose = True
    document.update_attributes()
    if '-e' not in options:
        # Load asciidoc.conf files in two passes: the first for attributes
        # the second for everything. This is so that locally set attributes
        # available are in the global asciidoc.conf
        if not config.load_from_dirs('asciidoc.conf', include=['attributes']):
            raise EAsciiDoc('configuration file asciidoc.conf missing')
        load_conffiles(include=['attributes'])
        config.load_from_dirs('asciidoc.conf')
        if infile != '<stdin>':
            indir = os.path.dirname(infile)
            config.load_file('asciidoc.conf', indir, include=['attributes', 'titles', 'specialchars'])
    else:
        load_conffiles(include=['attributes', 'titles', 'specialchars'])
    document.update_attributes()
    # Check the infile exists.
    if infile != '<stdin>':
       if not os.path.isfile(infile):
           raise EAsciiDoc('input file %s missing' % infile)
    document.infile = infile
    AttributeList.initialize()
    # Open input file and parse document header.
    reader.tabsize = config.tabsize
    reader.open(infile)
    has_header = document.parse_header(doctype, backend)
    # doctype is now finalized.
    document.attributes['doctype-' + document.doctype] = ''
    config.set_theme_attributes()
    # Load backend configuration files.
    if '-e' not in options:
        f = document.backend + '.conf'
        conffile = config.load_backend()
        if not conffile:
            raise EAsciiDoc('missing backend conf file: %s' % f)
        document.attributes['backend-confdir'] = os.path.dirname(conffile)
    # backend is now known.
    document.attributes['backend-' + document.backend] = ''
    document.attributes[document.backend + '-' + document.doctype] = ''
    doc_conffiles = []
    if '-e' not in options:
        # Load filters and language file.
        config.load_filters()
        document.load_lang()
        if infile != '<stdin>':
            # Load local conf files (files in the source file directory).
            config.load_file('asciidoc.conf', indir)
            config.load_backend([indir])
            config.load_filters([indir])
            # Load document specific configuration files.
            f = os.path.splitext(infile)[0]
            doc_conffiles = [
                f for f in (f + '.conf', f + '-' + document.backend + '.conf')
                if os.path.isfile(f)
            ]
            for f in doc_conffiles:
                config.load_file(f)
    load_conffiles()
    # Build asciidoc-args attribute.
    args = ''
    # Add custom conf file arguments.
    for f in doc_conffiles + confiles:
        args += ' --conf-file "%s"' % f
    # Add command-line and header attributes.
    attrs = {}
    attrs.update(AttributeEntry.attributes)
    attrs.update(config.cmd_attrs)
    if 'title' in attrs:    # Don't pass the header title.
        del attrs['title']
    for k, v in list(attrs.items()):
        if v:
            args += ' --attribute "%s=%s"' % (k, v)
        else:
            args += ' --attribute "%s"' % k
    document.attributes['asciidoc-args'] = args
    # Build outfile name.
    if outfile is None:
        outfile = os.path.splitext(infile)[0] + '.' + document.backend
        if config.outfilesuffix:
            # Change file extension.
            outfile = os.path.splitext(outfile)[0] + config.outfilesuffix
    document.outfile = outfile
    # Document header attributes override conf file attributes.
    document.attributes.update(AttributeEntry.attributes)
    document.update_attributes()
    # Set the default embedded icons directory.
    if 'data-uri' in document.attributes and not os.path.isdir(document.attributes['iconsdir']):
        document.attributes['iconsdir'] = os.path.join(document.attributes['asciidoc-confdir'], 'icons')
    # Set compat mode
    # TODO: Enable this in 10.3 (see https://github.com/asciidoc-py/asciidoc-py/issues/254)
    # if 'future-compat' in document.attributes:
    #     set_future_compat()
    # if 'legacy-compat' in document.attributes or 'compat-mode' in document.attributes:
    #     set_legacy_compat()
    # Configuration is fully loaded.
    config.expand_all_templates()
    # Check configuration for consistency.
    config.validate()
    # Initialize top level block name.
    if document.attributes.get('blockname'):
        AbstractBlock.blocknames.append(document.attributes['blockname'])
    paragraphs.initialize()
    lists.initialize()
    if config.dumping:
        config.dump()
    else:
        writer.newline = config.newline
        try:
            print(f"writing translation to {outfile}")
            sys.stdout.flush()
            writer.open(outfile, reader.bom)
            print(f"writing translation to {outfile} done")
            sys.stdout.flush()
            try:
                document.translate(has_header)  # Generate the output.
            finally:
                writer.close()
        finally:
            reader.closefile()

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
        print("call fasciidoc() before")
        sys.stdout.flush()
        fasciidoc(backend, doctype, confiles, infile, outfile, options)
        print("call fasciidoc() after")
        sys.stdout.flush()
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
    out_file = os.path.join(out_path, fname_wo_ending)
    if not os.path.isdir(out_path):
      os.mkdir(out_path)
    inner_argv = [sys.argv[0], "--verbose", f"--out-file={out_file}.html", file]
    print(f"send file {file} to asciidoc with inner argv:", inner_argv)
    sys.stdout.flush()
    execute(__file__, (("verbose", True), ("out-file", out_file)), [file])
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
