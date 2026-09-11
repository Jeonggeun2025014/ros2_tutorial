from setuptools import find_packages, setup

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jglim',
    maintainer_email='jglim@inhatc.ac.kr',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_first_node = my_package.my_first_node:main',
            'my_publisher_node = my_package.my_publisher_node:main',
            'my_subscriber_node = my_package.my_subscriber_node:main',
            'my_service_server_node = my_package.my_service_server_node:main',
            'my_service_client_node = my_package.my_service_client_node:main',
        ],
    },
)

