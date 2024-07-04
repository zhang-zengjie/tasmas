from setuptools import setup, find_packages

setup(
    name='tasmas',
    version='0.1.0',
    description='A risk-aware framework for task allocation of stochastic multi-agent systems',
    url='https://github.com/zhang-zengjie/tasmas.git',
    author='Zengjie Zhang',
    author_email='z.zhang3@tue.nl',
    license='BSD3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'gurobipy<=11.0.2',
        'matplotlib',
        'numpy<=1.26.4',
        'scipy',
        'treelib',
        'control'
    ],
    extras_require={
    },
    classifiers=[
    ],
    python_requires='>=3.7',
    entry_points={
    },
    include_package_data=True
)