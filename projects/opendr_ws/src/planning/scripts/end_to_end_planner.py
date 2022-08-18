#!/usr/bin/env python
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


import rospy


class EndToEndPlannerNode:

    def __init__(self):
        """
        Creates a ROS Node for pose detection
        """
        self.node_name = "opendr_end_to_end_planner"

    def listen(self):
        """
        Start the node and begin processing input data
        """
        rospy.init_node('opendr_end_to_end_planner', anonymous=True)
        rospy.spin()


if __name__ == '__main__':
    pose_estimation_node = EndToEndPlannerNode()
    pose_estimation_node.listen()
