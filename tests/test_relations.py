from ..src.aero.normal_shock import normal_shock_ratios

def test_normal_shock_basic():
    r = normal_shock_ratios(7.0, gamma=1.4)
    assert r['M2'] < 1.0
    assert r['p2_p1'] > 1.0
    assert r['rho2_rho1'] > 1.0
    assert r['T2_T1'] > 1.0
