import setuptools

setuptools.setup(
    name="pytweetdeck",
    version="1.0.1",
    install_requires=open("requirements.txt").read().splitlines(),
    author="mafu",
    author_email="mafusukee@gmail.com",
    description="Wrapper library of TweetDeck's internal api.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/m4fn3/pytweetdeck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
