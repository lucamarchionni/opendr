# Copyright 2021 RangiLyu.
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

import copy

from opendr.perception.object_detection_2d.nanodet.algorithm.nanodet.model.weight_averager.ema import ExpMovingAverager


def build_weight_averager(cfg, device="cpu"):
    cfg = copy.deepcopy(cfg)
    name = cfg.pop("name")
    if name == "ExpMovingAverager":
        return ExpMovingAverager(**cfg, device=device)
    else:
        raise NotImplementedError(f"{name} is not implemented")
