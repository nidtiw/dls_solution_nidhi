# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

# Comment
# INSTRUCTION arguments

# escape=`

# Use an official Python runtime as a parent image
FROM python:3

# TODO: add docker commands to get your service code into the container and
# running.  Some potentially useful docker keywords: ADD, WORKDIR, RUN
RUN echo "TODO!"

# Set the working directory to /docker_test
WORKDIR /docker_test

# Copy the current directory contents into the container at /app
ADD . /docker_test

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "main.py"]
