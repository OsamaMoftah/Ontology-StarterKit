# Classes, instances and relations

`Person`, `Team` and `Project` are classes: concepts in the model. `Maya`, `Aurora` and `Alpha` are instances: entities in the data. `manages` and `worksOn` are relations between instances. A `name` is a data property.

```text
Maya --manages--> Aurora --worksOn--> Alpha
Person            Team              Project
```

The lower line describes the type of each instance; it is not another fact that Maya is the class Person. Run the bundled SPARQL competency question through the Python API:

```python
from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import run_named_query
pack = load_pack("examples/hello-ontology")
print(run_named_query(pack, "manager"))
```

Expected result contains Maya Chen. Change the relation or remove it and observe that the query becomes empty; an empty answer is an unknown in this dataset, not proof that no manager exists.
