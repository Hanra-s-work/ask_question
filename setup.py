import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ask-question',  
    version='1.1.0',
    scripts=['src/ask_question.py'] ,
    author="Henry Letellier",
    author_email="henrysoftwarehouse@protonmail.com",
    description="A module simplifie the boiling process when asking the user a question via TTY.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hanra-s-work/ask_question",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
