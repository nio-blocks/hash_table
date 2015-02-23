HashTable
=======

Group a list of signals into one hash table signal. The output signal will contain an attribute for each evaluated *key* and the value of that attribute will be a list with an item of *value* for each matching signal.

If *one_value* is True, the Signal attributes will be just a single matching value instead of a list of all matching values. If multiple matches, then the last signal processed will be the value used.

Properties
--------------

-   **key**: Expression property. Evaluates to attribute on output signal.
-   **value**: Expression proprety. Evaluates to a value to be placed in an output signal list.
-   **group_attr**: What attribute on the signal the group should be set to. If this is blank, no group by will be performed and only one signal will be emitted. Otherwise, the value of the group by expression will be set to this attribute on each output signal.
-   **one_value**: If True, the output signals have attribute values that are a single value instead of a list of all matching values. When multiple signals match one key, the value used is from the last signal processed.


Dependencies
----------------
None

Commands
----------------
None

Input
-------
The signals should have attributes that can be evaluated by *key* and *value*.

Output
---------
For each input list of signals there is one output signal. It has an attribute for each *key* and that attribute is a list with a *value* for each corresponding input signal. When *group_attr* is set, it will be added as a value on the output signal with a value that is the group. If *one_value* is True, then the signal values are a single item instead of a list of all matching values.
