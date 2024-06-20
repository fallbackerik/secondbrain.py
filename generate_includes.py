import os
import os.path

def note_includes(dir: str) -> list[str]:
  note_includes=[]
  for note in os.listdir(dir):
    full_path = os.path.join(dir, note)
    print("found:", full_path)
    if os.path.isfile(full_path) and note.endswith(".adoc") and not note.startswith("README"):
      note_includes.append(f"include::{full_path}[]")
  note_includes.sort()
  return note_includes

def main() -> None:
  with open("index.adoc", "r") as index_in:
    index_txt = index_in.read()
  with open("index.adoc", "w") as index_out:
    out_txt = index_txt.replace("include::journal[]", "\n\n".join(note_includes("journal")) + "\n").replace("include::concept[]", "\n\n".join(note_includes("concept")) + "\n")
    print("---")
    print(repr(out_txt))
    print("---")
    index_out.write(out_txt)

if __name__ == '__main__':
  main()
