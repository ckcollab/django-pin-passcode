from setuptools import setup, find_packages


try:
    with open('README.md') as readme:
        long_description = readme.read()
except (IOError, ImportError):
    long_description = ''


setup(
    name="django-pin-passcode",
    packages=find_packages(),
    include_package_data=True, # declarations in MANIFEST.in
    version="0.1.9",
    author="Eric Carmichael",
    author_email="eric@ckcollab.com",
    description="A simple django app that provides site-wide easy password authentication for 1 user",
    long_description=long_description,
    license="MIT",
    url="https://github.com/ckcollab/django-pin-passcode",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
