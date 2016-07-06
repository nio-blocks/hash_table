HashTable
=========

Group a list of signals into one hash table signal. The output signal will contain an attribute for each evaluated **key** and the value of the **key** attribute will be a list with an item of **value** for each matching signal.

If **one_value** is True, the Signal attributes will be just a single matching value instead of a list of all matching values. If multiple matches, then the last signal processed will be the value used.

If **group_by** is used, a Signal for each value in the **group_by** attribute will be produced.

Properties
----------

-   **key**: Expression property. Evaluates to key attribute on output signal.
-   **value**: Expression property. Evaluates to a value to be placed in an output signal list.
-   **group_by**: Expression to group signals by.
-   **group_attr**: When *group_by* is used, this is the value that will be stored in a Signal attribute called, in this case, "group".
-   **one_value**: If True, the output signals have attribute values that are a single value instead of a list of all matching values. When multiple signals match one key, the value used is from the last signal processed.


Dependencies
------------
None

Commands
--------
None

Input
-----
The signals should have attributes that can be evaluated by **key** and **value**.

Output
------
For each input list of signals there is one output signal. It has an attribute for each **key** and that attribute is a list with a **value** for each corresponding input signal.

If **one_value** is True, then the signal values are a single item instead of a list of all matching values.

If **group_by** is defined, that attribute will effectively define a new input list. One signal will be output for each value found in the **group_by** attribute.

Examples
--------

**Signals Input**

```python
[
{ "type": "shirt", "color": "red", "size": 10},
{ "type": "shirt", "color": "red", "size": 14},
{ "type": "shirt", "color": "orange", "size": 12},
{ "type": "scarf", "color": "red", "size": "M"},
{ "type": "shoes", "color": "orange", "size": 8}
]
```

**Block Config with _key_ based on _type_**

```
key: {{ $type }},
value: {{ $size }},
one_value: False

```

**Signal Output**

```python
{
  "shoes": [8],
  "scarf": ["M"],
  "shirt": [10, 14, 12],
  "group": ""
}
```
**Block Config with _key_ based on _color_**

```
key: {{ $color }}
value: {{ $type }}
one_value: False
```

**Signal Output**

```python
{
  "orange": ["shirt", "shoes"],
  "red": ["shirt", "shirt", "scarf"],
  "group": ""
}
```

**Block Config with _key_ based on _type_ and _One Value Per Key_ checked**

```
key: {{ $color }}
value: {{ $type }}
one_value: True
```

**Signal Output**

```python
{
  "red": "scarf",
  "orange": "shoes",
  "group": ""
}
```

**Block Config using _group_by_ to spit out multiple signals**

```
key: {{ $type }}
value: {{ $size }}
group_by: {{ $color }}
one_value: False
```

**Signal Output**

```python
[
  {"group": "orange", "shoes": [8], "shirt": [12]},
  {"group": "red", "scarf": ["M"], "shirt": [10, 14]}
]
```
