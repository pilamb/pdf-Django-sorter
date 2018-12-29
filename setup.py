import setuptools

with open("README.rst", "r") as fh:
      long_description = fh.read()

      setuptools.setup(
            name="pdfuploader",
            version="0.0.1",
            author="Pedro Cordero",
            author_email="author@example.com",
            description="A Django site to store, classify and manage PDFs including tags and metadata extraction when the archives are uploaded.",
            long_description=long_description,
            long_description_content_type="text/markdown",
            url="https://github.com/pilamb/pdf-Django-sorter",
            packages=setuptools.find_packages(),
            classifiers=[
                      "Programming Language :: Python :: 3",
                      "License :: OSI Approved :: MIT License",
                      "Operating System :: OS Independent",
                  ],
      )
