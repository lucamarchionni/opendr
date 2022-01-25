# ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD
# Copyright 2020-2022 OpenDR European Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=[
        'map_simulator',
        'map_simulator.geometry', 'map_simulator.geometry.primitives',
        'map_simulator.map_obstacles',
        'map_simulator.robot_commands',
        'map_simulator.robot_commands.message', 'map_simulator.robot_commands.misc', 'map_simulator.robot_commands.move'
    ],
    package_dir={
        '': 'src'
    },
)

setup(**setup_args)
