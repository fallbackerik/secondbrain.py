import os
import os.path

def main() -> None:
  journal_includes = []
  for journal in os.listdir("journal/"):
    full_path = os.path.join("journal/", journal)
    print("including: ", full_path)
    if os.path.isfile(full_path) and journal.endswith(".adoc"):
      journal_includes.append("include::{full_path}[]")
  with open("index.adoc", "r") as index_in:
    index_txt = index_in.read()
  with open("index.adoc", "w") as index_out:
    index_out.write(index_txt.replace("include::journal/*.adoc[]", "\n".join(journal_includes)))

if __name__ == '__main__':
  main()
