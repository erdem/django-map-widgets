from setuptools import setup, find_packages

VERSION = (0, 3, 3)
__version__ = '.'.join(map(str, VERSION))

setup(
    name='django-map-widgets',
    version=__version__,
    description='Map widgets for Django PostGIS fields',
    long_description='Configurable, pluggable and more user friendly map widgets for Django PostGIS fields.',
    long_description_content_type='text/x-rst',
    author='Erdem Ozkol',
    author_email='erdemozkol@gmail.com',
    url='https://github.com/erdem/django-map-widgets',
    license='MIT',
    platforms=['any'],
    packages=find_packages(exclude=('example', 'static', 'env')),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python',
    ],
)

