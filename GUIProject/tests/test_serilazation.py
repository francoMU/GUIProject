from guiproject.selectable_points import DataSchema, Data


def test_deserialization_to_object():
    data = {
        "energies": [10.1, 10.2],
        "delta": [0.1, 0.2],
    }

    schema = DataSchema()
    result = schema.load(data)

    assert type(result) == Data
    assert result.energies == [10.1, 10.2]
    assert result.delta == [0.1, 0.2]
