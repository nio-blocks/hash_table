HashTable
=========

Group a list of signals into one hash table signal. The output signal will contain an attribute for each evaluated *key* and the value of that attribute will be a list with an item of *value* for each matching signal.

If *one_value* is True, the Signal attributes will be just a single matching value instead of a list of all matching values. If multiple matches, then the last signal processed will be the value used.

If *group_by* is used, a Signal attribute (key) with the default (pre-assigned) name *group* will have the value of *group_by* in the output signal.

**Example:**

_Signals Input_:

```python
[
{ "type": "important", "color": "red", "age": 32 },
{ "type": "minor", "color": "red", "age": 9 },
{ "type": "important", "color": "orange", "age": 14 },
{ "type": "standard", "color": "red", "age": 1 }
]
```

_Block Config with key based on "type"_:

```python
key : {{ $type }}
value : {{ $age }}
one_value: False
```

_Signal Output_:

```python
{
    "important": [32, 14],
    "standard": [1],
    "minor": [9],
    "group": ""
}
```
_Block Config with key based on "color"_:

```python
key : {{ $color }}
value : {{ $age }}
one_value: False
```

_Signal Output_:

```python
{
    "red": [32, 9, 1],
    "orange": [14],
}
```

_Block Config with key based on "type" and "One Value Per Key" checked (one_value = True)_:

```python
key : {{ $type }}
value : {{ $age }}
one_value: True
```

_Signal Output_:

```python
{
    "important": [14],
    "standard": [1],
    "minor": [9]
    "group": ""
}
```

_Block Config using *group_by* to assign name to the *group* Signal attribute_:

```python
key : {{ $type }}
value : {{ $age }}
group_by: "priority"
one_value: False
```

_Signal Output_:

```python
[
  {
    "group": "priority",
    "important": [32, 14],
    "standard": [1],
    "minor": [9]
  }
]
```

Properties
----------

-   **key**: Expression property. Evaluates to key attribute on output signal.
-   **value**: Expression property. Evaluates to a value to be placed in an output signal list.
-   **group_by**: Expression to group signals by.
-   **group_attr**: When *group_by* is used, this is the value that will be stored in a Signal attribute called, in this case, 'group'.
-   **one_value**: If True, the output signals have attribute values that are a single value instead of a list of all matching values. When multiple signals match one key, the value used is from the last signal processed.


Dependencies
------------
None

Commands
--------
None

Input
-----
The signals should have attributes that can be evaluated by *key* and *value*.

Output
---------
For each input list of signals there is one output signal. It has an attribute for each *key* and that attribute is a list with a *value* for each corresponding input signal. If *group_by* is defined, it will become the value of the Signal attribute *group*. If *one_value* is True, then the signal values are a single item instead of a list of all matching values.
