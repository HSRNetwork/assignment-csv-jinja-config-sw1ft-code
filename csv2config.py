import csv
import re
from jinja2 import Template


def csv_import(file_name):
    context_list = []
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            context_list.append(row)

    return context_list

def render_template(file_name, data_list):
    list_rendered_templates = []
    with open(file_name) as jinjafile:
        raw_template = jinjafile.read()
        template = Template(raw_template)
        for device in data_list:
            list_rendered_templates.append(template.render(device))

    return list_rendered_templates

def write_files(content_list):
    for cfg in content_list:
        hostname = re.search(r'hostname (.*)', cfg)
        hostname = hostname.group(0).replace('hostname ', '')
        with open("configs/{hostname}.cfg".format(hostname=hostname), "w") as text_file:
            text_file.write(cfg)

    return None


if __name__ == '__main__':
    csv_data = csv_import('parameter.csv')
    configs = render_template('config_template.j2', csv_data)
    write_files(configs)
