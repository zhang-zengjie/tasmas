from setuptools import setup, find_packages

setup(
    name='tasmas',
    version='0.1.0',
    description='A risk-aware framework for task allocation of stochastic multi-agent systems',
    url='https://github.com/zhang-zengjie/tasmas.git',
    author='Zengjie Zhang',
    author_email='z.zhang3@tue.nl',
    license='BSD3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'gurobipy',
        'matplotlib',
        'numpy',
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
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', 'src/*.py']
    },
)