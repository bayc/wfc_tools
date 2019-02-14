#
# Copyright 2019 NREL
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#


class Vec3():
    def __init__(self, x1, x2, x3):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.x3 = float(x3)

    def __str__(self):
        return "<{:8.3f},{:8.3f},{:8.3f}>".format(self.x1, self.x2, self.x3)

    def __add__(self, arg):
        if type(arg) is Vec3:
            return Vec3(self.x1 + arg.x1,
                        self.x2 + arg.x2,
                        self.x3 + arg.x3)
        else:
            return Vec3(self.x1 + arg,
                        self.x2 + arg,
                        self.x3 + arg)

    def __sub__(self, arg):
        if type(arg) is Vec3:
            return Vec3(self.x1 - arg.x1,
                        self.x2 - arg.x2,
                        self.x3 - arg.x3)
        else:
            return Vec3(self.x1 - arg,
                        self.x2 - arg,
                        self.x3 - arg)

    def __mul__(self, arg):
        if type(arg) is Vec3:
            return Vec3(self.x1 * arg.x1,
                        self.x2 * arg.x2,
                        self.x3 * arg.x3)
        else:
            return Vec3(self.x1 * arg,
                        self.x2 * arg,
                        self.x3 * arg)

    def __truediv__(self, arg):
        if type(arg) is Vec3:
            return Vec3(self.x1 / arg.x1,
                        self.x2 / arg.x2,
                        self.x3 / arg.x3)
        else:
            return Vec3(self.x1 / arg,
                        self.x2 / arg,
                        self.x3 / arg)

    def __eq__(self, arg):
        return self.x1 == arg.x1 \
            and self.x2 == arg.x2 \
            and self.x3 == arg.x3
