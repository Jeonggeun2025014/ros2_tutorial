import glob

from setuptools import find_packages, setup

package_name = 'square_patrol'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob('launch/*.launch.py')),
        ('share/' + package_name + '/param', glob.glob('param/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jglim',
    maintainer_email='jglim@inhatc.ac.kr',
    description='Robot patrols a randomly-ordered square path using odom + path-based angle control',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robot_simulator_node = square_patrol.robot_simulator_node:main',
            'path_manager_node = square_patrol.path_manager_node:main',
            'path_follower_node = square_patrol.path_follower_node:main',
        ],
    },
)
