from python.carioca_component._component import carioca_component


def test_component_roundtrip():
    data = {"hello": "world"}
    result = carioca_component(data)
    assert result == data
