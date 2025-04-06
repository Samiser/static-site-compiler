from setuptools import setup

_ = setup(
    name="static-site-compiler",
    version="0.1.0",
    description="my cool static site compiler",
    author="Samiser",
    entry_points={
        "console_scripts": [
            "ssc = ssc.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "blog": [
            "src/ssc/custom_pages/*/templates/*.html",
            "style/style.css",
        ],
    },
    install_requires=[
        "Jinja2",
        "Markdown",
        "Pygments",
        "python-frontmatter",
        "requests",
    ],
)
