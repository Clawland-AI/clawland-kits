import code

def test_get_kit_cost():
    assert code.get_kit_cost() == 88.0

def test_bom_integrity():
    assert len(code.BOM) == 8
    assert all(isinstance(item['cost'], (int, float)) for item in code.BOM)

def test_config_scenario():
    assert code.PICOCLAW_CONFIG["scenario"] == "datacenter_monitor"
    assert code.PICOCLAW_CONFIG["gpio"]["dht_pin"] == 15