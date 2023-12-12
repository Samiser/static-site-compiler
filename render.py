import jinja2


def render_template(template_dir, template_file, template_vars):
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template(template_file)

    return template.render(template_vars)
