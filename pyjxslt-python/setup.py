
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# This fails on the actual setup for some unknown reason.  We're going brute force for the moment...
# jarfiles = [f for f in resource_listdir(__name__, 'lib')]
jarfiles = ['lib/py4j-0.9.jar', 'lib/pyjxslt.jar', 'lib/Saxon-HE-9.7.0-1.jar']

setup(
    name='pyjxslt',
    packages=['pyjxslt'],
    package_dir={'pyjxslt': 'src/pyjxslt'},
    package_data={'pyjxslt': ['xsl/*.xsl']},
    version='0.6.1',
    url='http://github.com/CTS2/pyjxslt',
    license='BSD License',
    author='Harold Solbrig',
    author_email='solbrig.harold@mayo.edu',
    description='Python XSLT 2.0 Gateway',
    long_description='Interface package between native python and the Saxon XSLT 2.0 process, which is'
                     ' java based.  This package requires Java 1.7.',
    install_requires=["py4j >=0.9"],
    scripts=['scripts/pyjxslt', 'scripts/testgateway'],
    zip_safe=True,
    include_package_data=True,
    data_files=[('share/pyjxslt', jarfiles)],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        'Topic :: Text Processing'
    ]
)
