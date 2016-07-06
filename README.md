HashTable
=========

Group a list of signals into one hash table Signal. The output Signal will contain an attribute for each evaluated **key** and the **value** of the **key** attribute will be a **list** with an item of **value** for each matching signal.

If `one_value` is `True`, the Signal attributes will have a single matching value instead of a list of all values with a matching key. If multiple matches, then the last input signal processed will be the value used.

If `group_by` is defined, a Signal for each value in the `group_by` attribute will be produced.

Properties
----------
-   **key**: Expression property. Evaluates to key attribute on output Signal.
-   **value**: Expression property. Evaluates to a value in a list of values with a matching key.
-   **group_by**: Expression to group signals by.
-   **group_attr**: When `group_by` is used, this is the value that will be stored in a Signal attribute called, in this case, `group`.
-   **one_value**: If `True`, the output signals have attribute values that are a single value instead of a list of all matching values. When multiple signals match one key, the value used is from the last signal processed.

Dependencies
------------
None

Commands
--------
None

Output
------
For each input list of signals there is one output Signal. It has an attribute for each **key** and that attribute is a list with a **value** for each corresponding input signal.

If `one_value` is `True`, then the Signal values are a single item instead of a list of all matching values.

If `group_by` is defined, that attribute will effectively define a new input list of signals. One Signal will be output for each value found in the `group_by` attribute.

Examples
--------

**Input Signals**

```python
[
{ "type": "shirt", "color": "red", "size": 10},
{ "type": "shirt", "color": "red", "size": 14},
{ "type": "shirt", "color": "orange", "size": 12},
{ "type": "scarf", "color": "red", "size": "M"},
{ "type": "shoes", "color": "orange", "size": 8}
]
```

**Block Config with _key_ based on `type`**

```
key: {{ $type }},
value: {{ $size }},
one_value: False
```

**Output Signal**

```python
{
  "shoes": [8],
  "scarf": ["M"],
  "shirt": [10, 14, 12],
  "group": ""
}
```
**Block Config with _key_ based on `color`**

```
key: {{ $color }}
value: {{ $type }}
one_value: False
```

**Output Signal**

```python
{
  "orange": ["shirt", "shoes"],
  "red": ["shirt", "shirt", "scarf"],
  "group": ""
}
```

**Block Config with _key_ based on `color` and _One Value Per Key_ checked**

```
key: {{ $color }}
value: {{ $type }}
one_value: True
```

**Output Signal**

```python
{
  "red": "scarf",
  "orange": "shoes",
  "group": ""
}
```

**Block Config using `group_by` to spit out multiple signals**

```
key: {{ $type }}
value: {{ $size }}
group_by: {{ $color }}
one_value: False
```

**Output Signals**

```python
[
  {"group": "orange", "shoes": [8], "shirt": [12]},
  {"group": "red", "scarf": ["M"], "shirt": [10, 14]}
]
```
