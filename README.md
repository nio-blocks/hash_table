HashTable
=========

Group a list of input signals into one hash table signal. The output signal will contain an attribute for each evaluated **key** and the **value** of the key will be a **list** containing each value with a matching key.

If `one_value` is `True`, the output signal's attributes will each have a single value instead of a list of all values. If multiple matching keys are found, the value of the last input signal processed will be the value of the key.

If `group_by` is defined, an output signal will be produced for each value in the `group_by` attribute.

If including existing signal attributes with `enrich`, then the last signal passed into the block will be the one enriched.

Properties
----------
-   **key**: Expression property. Evaluates to a key attribute on output signal.
-   **value**: Expression property. Evaluates to a value in a list of values with a matching key.
-   **group_by**: Expression to group signals by.
-   **group_attr**: When `group_by` is used, this is the value that will be stored in a signal attribute called, in this case, `group`.
-   **one_value**: If `True`, the output signal's attributes have a single value instead of a list of values. When multiple input signals match one key, the value of the last signal processed is the value used.

Dependencies
------------
None

Commands
--------
None

Output
------
For each list of input signals there is one output signal. It has an attribute for each **key** and that attribute is a **list** containing a **value** for each matching key found in an input signal.

If `one_value` is `True`, then each attribute on the output signal has a value that is a single item instead of a list of all matching values.

If `group_by` is defined, the `group_by` attribute will effectively define a new list of input signals. One output signal will be generated for each value found in the `group_by` attribute.

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

**Block Config with _key_ based on `type` and enriching signals**

```
key: {{ $type }},
value: {{ $size }},
one_value: False
enrich.exclude_existing: False
```

**Output Signal**

```python
{
  "shoes": [8],
  "scarf": ["M"],
  "shirt": [10, 14, 12],
  "group": "",
  "type": "shoes",
  "color": "orange",
  "size": 8
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

**Output Signals (one for each value of `color`)**

```python
[
  {"group": "orange", "shoes": [8], "shirt": [12]},
  {"group": "red", "scarf": ["M"], "shirt": [10, 14]}
]
```
