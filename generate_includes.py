import os
import os.path

def main() -> None:
  with open("index.adoc", "w") as index:
    for journal in os.listdir("journal/"):
      full_path = os.path.join("journal/", journal)
      print("including: ", full_path)
      if os.path.isfile(full_path) and journal.endswith(".adoc"):
        index.append("include::{journal}[]")
      
if __name__ == '__main__':
  main()
