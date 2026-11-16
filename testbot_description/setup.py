import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'testbot_description'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # URDF, launch, rviz 파일을 설치 폴더로 복사해야 get_package_share_directory 로 찾을 수 있다
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jeonggeun Lim',
    maintainer_email='jglim@inhatc.ac.kr',
    description='URDF description of testbot',
    license='Apache-2.0',
    entry_points={'console_scripts': []},
)
