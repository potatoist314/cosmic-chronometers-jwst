import vast


def test_bandwidth_limit_is_per_terabyte():
    per_gb = vast.MAX_INET_COST_USD_PER_TB / 1000
    assert not vast.bandwidth_qualifies({"inet_down_cost": 0.025, "inet_up_cost": 0.001})
    assert not vast.bandwidth_qualifies({"inet_down_cost": 0.0, "inet_up_cost": 1.5 * per_gb})
    assert vast.bandwidth_qualifies({"inet_down_cost": 0.5 * per_gb, "inet_up_cost": 0.5 * per_gb})
    assert not vast.bandwidth_qualifies({"inet_up_cost": 0.0})
