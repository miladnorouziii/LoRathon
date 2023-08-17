from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A LoRa commiunication package'
LONG_DESCRIPTION = 'This library is for LoRa modules (Sx127x) based on the Python language'

setup(
    name="convsn",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Milad Norouzi",
    author_email="miladnorouzi@icloud.com",
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[],
    keywords='Lora',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GPL-3.0 License',
        "Programming Language :: Python :: 3",
    ]
)
