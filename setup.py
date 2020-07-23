from setuptools import setup 

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name = "smythbot",
    version="0.0.1",
    author="Shawn Sörbom",
    author_email="N/A",
    description="A Matrix chatbot to control your Mythtv DVR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shsorbom/sMythbot",
    install_requires=['matrix-nio', 'future', 'mysqlclient', 'lxml', 'requests'],
    dependency_links=[
        "git+https://github.com/MythTV/mythtv/tree/master/mythtv/bindings/python",
    ],
    py_modules=['smythbot', 'smythbot_outputs', 'sMythClient', 'smythbotCommandRunner'],
    scripts= ['smythbot.py'],
    python_requires='>=3.8',
    classifiers=[
        'License :: OSI Approved :: GPL 3',
        'Programming Language :: Python :: 3.8',
    ]
)