import jinja2
import datetime

today = datetime.date.today()
context = {
  "today object" : today,
  "today iso underscored" : today.strftime("%Y_%m_%d"),
  "today human readable" : today.strftime("%A, %M %d, %Y"),
}

env = jinja2.Environment(loader=jinja2.FileSystemLoader("template/"))
template = env.get_file("journal.adoc.jinja")

rendered = template.render(context)
output_name = f"journal/{context["today iso underscore"]}.adoc"
with open(output_name, "w", encoding="utf-8") as output:
  output.write(rendered)

print(f"created journal entry {output_name}.")
