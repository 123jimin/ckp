# Sorted Containers

Sorted containers from CKP is a copy of [the `sortedcontainers` library](https://grantjenks.com/docs/sortedcontainers/) with some modifications to reduce code size.

Check [the documentation for `sortedcontainers`](https://grantjenks.com/docs/sortedcontainers/introduction.html) on how to use `SortedList` and `SortedDict` under `ckp.data_structure.sorted_containers`.

In general, these classes can be used whenever something like `std::map<K, T>::lower_bound` from C++ STL is wanted.