from distutils.core import setup
setup(name="tvinfo",
        version="1.0",
        description="TV information lookup",
        author="Scott Raynel",
        author_email="scottraynel@gmail.com",
        url="http://www.github.com/scottr/tvinfo/",
        packages=["tvinfo", "tvinfo.backends"],
        scripts=["tvrenamer3"],
)

