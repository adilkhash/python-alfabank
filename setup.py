from setuptools import find_packages, setup

install_requires = [
    'zeep',
]

tests_require = [
    'pytest>=2.8.3',
    'responses>=0.5.1',
]

setup(
    name='alfabank',
    version='0.1dev0',
    description='Alfabank payment gateway client',
    long_description='',
    author="Adylzhan Khashtamov",
    author_email="adil@khashtamov.com",
    url='https://github.com/adilkhash/python-alfabank',

    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    packages=find_packages(),
    include_package_data=True,

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    zip_safe=False,
)
