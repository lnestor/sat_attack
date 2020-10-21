def extract_from_model(model, to_extract, completion = False):
    """
    Extracts python literal values from a z3 model.

    model: the z3 model
    to_extract: a list of names to extract from the model
    completion: if True, return a value for all names in to_extract
                   even if they do not have a value in the model
                if False, only return values for those in the model
    returns: a dictionary of the form {name: value}
    """
    values = {}

    for input in model:
        if str(input) in to_extract:
            values[str(input)] = model[input]

    if completion:
        remaining = [i for i in to_extract if i not in values.keys()]
        for r in remaining:
            values[r] = False

    return values
