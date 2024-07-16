import jinja2
import datetime

def main():
  today = datetime.date.today()
  context = {
    "today_object" : today,
    "today_iso_underscored" : today.strftime("%Y_%m_%d"),
    "today_human_readable" : today.strftime("%A, %B %d, %Y"),
  }

  env = jinja2.Environment(loader=jinja2.FileSystemLoader("template/"))
  template = env.get_template("journal.adoc.jinja")

  rendered = template.render(context)
  output_name = f"journal/{context['today_iso_underscored']}.adoc"
  with open(output_name, "w", encoding="utf-8") as output:
    output.write(rendered)

  print(f"created journal entry {output_name}.")

if __name__ == '__main__':
  main()
