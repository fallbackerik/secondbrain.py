import jinja2
import datetime
import os.path

from new_daily import main as Journal

def main():
  today = datetime.date.today()
  title = "Test Note Creation"
  fname = "".join(title.split()) + ".adoc"
  today_iso_underscored = today.strftime("%Y_%m_%d")
  journal = f"journal/{today_iso_underscored}.adoc"
  if not os.path.isfile(journal):
    Journal()

  context = {
    "title": title,
    "fname": fname,
    "today_object" : today,
    "today_human_readable" : today.strftime("%A, %B %d, %Y"),
    "journal" : journal,
  }

  env = jinja2.Environment(loader=jinja2.FileSystemLoader("template/"))
  template = env.get_template("note.adoc.jinja")

  rendered = template.render(context)
  output_name = f"note/{fname}.adoc"
  with open(output_name, "w", encoding="utf-8") as output:
    output.write(rendered)

  print(f"created note {output_name}.")

if __name__ == '__main__':
  main()
