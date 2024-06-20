import os
import os.path

def main() -> None:
  with open("index.adoc", "w") as index:
    for journal in listdir("journal/"):
      if isfile(join("journal/", file) and file.endswith(".adoc"):
        index.append("include::{journal}[]")
      
if __name__ == '__main__':
  main()
