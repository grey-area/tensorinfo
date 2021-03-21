from distutils.core import setup


if __name__ == '__main__':

    setup(
        name='TensorInfo',
        version='0.0.1',
        author='Andrew M. Webb',
        author_email='andrew@awebb.info',
        packages=['tensorinfo'],
        url='http://www.awebb.info',
        license='MIT License',
        description='A package for printing pytorch tensor and numpy array debug info.',
        python_requires='>=3.6.0',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
    )
