from setuptools import setup

setup(
    name = 'py40kie', 
    
    version = '0.0.3',
    
    description = 'Command line Python program to extract army rules and unit cards from 10th edition Warhammer 40k indexes to create army list specific pdfs with reduced file size.',
    
    py_modules = ["__main__"],
    
    package_dir = {'':'src'},
    
    author = 'ChrisAustin',
    author_email = 'dragons.ire.oce@gmail.com',
    
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type = "text/markdown",
    
    url='https://github.com/Dragons-Ire/40k-index-pdf-extracto',
    
    include_package_data=True,
    
    classifiers  = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Text Processing",
    ],
    
    install_requires = [
        'pypdf ~= 3.12.1',
    ],
    
    entry_points={
        "console_scripts": [
            "py40kie=src.__main__:console_entry",
        ]
    }
    
    keywords = ['Warhammer 40000'],
)