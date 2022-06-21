import setuptools

with open("README.md", "r") as f:
   long_description = f.read()

setuptools.setup(
    name="pygenetic",
    version="1.0.2",
    author="Bharatraj S Telkar, Daniel Isaac, Shreyas V Patil",
    author_email="telkarraj@gmail.com, danielbcbs2@gmail.com, pshreyasv100@gmail.com",
    description="An Efficient Python Genetic Algorithm API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danny311296/pygenetic",
    packages=['pygenetic'],
    include_package_data=True,
    license='MIT',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
          'rstr==2.2.6',
          'numpy==1.22.0',
          'matplotlib==2.2.2',
      ],
)