import jinja2
import datetime

today = datetime.date.today()
title = "Test Note Creation"
fname = "".join(title.split()) + ".adoc"
context = {
  "title": title,
  "fname": fname,
  "today_object" : today,
  "today_iso_underscored" : today.strftime("%Y_%m_%d"),
  "today_human_readable" : today.strftime("%A, %B %d, %Y"),
}

env = jinja2.Environment(loader=jinja2.FileSystemLoader("template/"))
template = env.get_template("note.adoc.jinja")

rendered = template.render(context)
output_name = f"note/{fname}.adoc"
with open(output_name, "w", encoding="utf-8") as output:
  output.write(rendered)

print(f"created note {output_name}.")
