from setuptools import setup

package_dependencies = ['numpy', ]

setup(
    name='ukb_decoder',
    version='v0.0',
    packages=['ukb_decoder'],
    url='',
    license='MIT',
    author='Adriaan van der Graaf',
    author_email='adriaan.vd.graaf@gmail.com',
    description='UKB field decoder',
    install_requires = package_dependencies,

    extras_require = {
                     'dev': ['check-manifest'],
                 },
)
