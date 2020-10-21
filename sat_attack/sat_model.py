def extract_from_model(model, to_extract, completion = False):
    values = {}

    for input in model:
        if str(input) in to_extract:
            values[str(input)] = model[input]

    if completion:
        remaining = [i for i in to_extract if i not in values.keys()]
        for r in remaining:
            values[r] = False

    return values
