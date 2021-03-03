# Copyright 2020 Institute for Automation of Complex Power Systems,
# E.ON Energy Research Center, RWTH Aachen University
#
# This project is licensed under either of
# - Apache License, Version 2.0
# - MIT License
# at your option.
#
# Apache License, Version 2.0:
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
#
# MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module implements the agent class for the pingpong benchmark
"""

import json
import clonemapy.agent as agent
import clonemapy.agency as agency
import clonemapy.datamodels as datamodels
import time


class AgentData():
    def __init__(self):
        self.testdata = 0

    def to_json_dict(self):
        js_dict = {'test': self.testdata}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.testdata = js_dict.get("test", 0)

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)


class Agent(agent.Agent):
    def __init__(self, info, msg_in, msg_out, log_out):
        super().__init__(info, msg_in, msg_out, log_out)

    def task(self):
        time.sleep(5)
        print("Hello")
        recv = (self.id+1) % 2
        msg = datamodels.ACLMessage(receiver=recv, content="msg from "+str(self.id))
        self.acl.send_message(msg)
        self.logger.new_log("app", "agent"+str(self.id), "")
        svc = datamodels.Service(desc="svc by " + str(self.id))
        svcid = self.df.register_service(svc)
        print(svcid)
        msg = self.acl.recv_message_wait()
        print(msg)
        self.loop_forever()


if __name__ == "__main__":
    ag = agency.Agency(Agent)