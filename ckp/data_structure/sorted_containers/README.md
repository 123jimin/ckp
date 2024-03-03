# Python Sorted Containers

## Modifications

Codes in this directory is based on the Python [Sorted Containers](https://github.com/grantjenks/python-sortedcontainers) library.

Here are the list of changes:

* Added `COPYRIGHT` attribute to attribute (no pun intended) original authors.
* Removed the following functions / proeprties:
  * `Sorted*.__new__`
  * `Sorted*._check`
  * `Sorted*.__reduce__`
  * `Sorted*._check`
  * `SortedDict.iloc`
  * `SortedList.key`
  * `SortedDict.keys`, `SortedDict.items`, `SortedDict.values`
* Removed docstrings from comparers returned by `__make_cmp`.
* Replaced `Sorted*.__repr__` with a simpler one, and added `Sorted*.__str__`.
* In `SortedList._build_index`, removed usage of `log` in size computation.
* Removed `key` argument from `SortedList` and `SortedDict`.
* Removed `Sorted*View`.

## Original License

Copyright 2014-2024 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

> <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.