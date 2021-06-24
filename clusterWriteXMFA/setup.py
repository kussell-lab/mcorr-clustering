from setuptools import setup

# read requirements.
requirements = []
with open("requirements.txt", 'rU') as reader:
    for line in reader:
        requirements.append(line.strip())

setup(name='clusterWrite',
        python_requires='>=3',
        version='210624',
        description='cluster and write XMFA files for core and flexible genomes',
        url='https://github.com/kussell-lab/mcorr-clustering',
        license='MIT',
        author='Asher Preska Steinberg',
        author_email='apsteinberg@nyu.edu',
        packages=['writeClusters'],
        install_requires=requirements,
        entry_points = {
            'console_scripts' : ['clusterWrite=writeClusters.cli:main'],
            }
      )
