Join
====
The Join block will group a list of incoming signals into one outgoing signal. The outgoing signal will contain an attribute for each evaluated `key` and the `value` of the key will be a **list** of each value with a matching key.

Properties
----------
- **enrich**: If checked (true), the attributes of the incoming signal will be excluded from the outgoing signal. If unchecked (false), the attributes of the incoming signal will be included in the outgoing signal.
- **group_attr**: A hidden property. When `group_by` is used, the attibute name 'group' assigned by the `group_by` mixin will be replaced by this property. The default value is `group`.
- **group_by**: The signal attribute of the incoming signal whose values will be used to define groups on the outgoing signal.
- **key**: Evaluates to a key attribute on the outgoing signal.
- **one_value**: If true, each attribute on the outgoing signal has a value that is a single item instead of a list of all matching values.
- **value**: Evaluates to a value in a list of values with a matching key.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: One outgoing signal that has an attribute for each `key` and the value of that `key` is a **list** of each value from a matching key found on in the incoming signal.

Commands
--------
- **groups**: Returns a list of the block’s current signal groupings.

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

