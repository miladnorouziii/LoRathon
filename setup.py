from setuptools import setup, find_packages

VERSION = '1.1.3'
DESCRIPTION = 'A LoRa commiunication package'
LONG_DESCRIPTION = 'This library is for LoRa modules (Sx127x) based on the Python language'

setup(
    name="LoRathon",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Milad Norouzi",
    author_email="miladnorouzi1998@gmail.com",
    license='GPL-3.0',
    url='https://github.com/miladnorouziii/LoRathon',
    packages=find_packages(),
    keywords=['Lora', 'Lora python', 'Lora raspberry pi','Lora python library', 'lora library raspberry pi'],
    install_requires=['spidev>=1.6',
                      'RPi.GPIO'                     
                      ],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: GNU General Public License (GPL)',
        "Programming Language :: Python :: 3",
    ]
)
