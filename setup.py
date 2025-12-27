import setuptools

with open("README.md", "r", encoding="utf-8") as f:
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
          'rstr>=2.2.6',
          'numpy>=1.19.0',
          'matplotlib>=3.0.0',
      ],
)