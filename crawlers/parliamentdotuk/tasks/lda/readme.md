Be aware that LDA API responses are somewhat inconsistent which can result in frustration(!)

### Watch out for:

- A list of objects (e.g. `result['items']`) may have a string (e.g. `"http://data.parliament.uk/resources/0"`) thrown on the end for fun.
  
- Object nesting:
  - Some values are available directly `obj['name']`
  - Some values are wrapped in their own object `obj['name']['_value]`
  - Some values are wrapped in their own list despite that list only ever having one item `obj['name'][0]`
    - The actual value may be further wrapped in its own object inside that list `obj['name'][0]['_value']`

- Sometimes a null value is denoted by something like `{"@xsi:nil": true}`. Other times it is not present at all.
- Some values appear to only exist before/after some point in time so beware of relying on a value being non-null.
