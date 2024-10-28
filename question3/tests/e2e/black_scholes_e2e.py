from question3.black_scholes import black_scholes_call, black_scholes_put
import pytest

def test_black_scholes_with_assertions():
    K = 100
    r = 0.05
    T = 1
    sigma = 0.2

    # Testing in-the-money option prices
    S_in_money = 120
    assert black_scholes_call(S_in_money, K, T, r, sigma) > 0, "In-the-money call should have value"
    assert black_scholes_put(S_in_money, K, T, r, sigma) < black_scholes_call(S_in_money, K, T, r, sigma), \
        "In-the-money put should be cheaper than in-the-money call"

    # Testing at-the-money option prices
    S_at_money = 100
    assert abs(black_scholes_call(S_at_money, K, T, r, sigma) - black_scholes_put(S_at_money, K, T, r, sigma)) < 10, \
        "At-the-money call and put prices should be relatively close"

    # Testing out-of-the-money option prices
    S_out_money = 80
    assert black_scholes_call(S_out_money, K, T, r, sigma) < black_scholes_put(S_out_money, K, T, r, sigma), \
        "Out-of-the-money call should be cheaper than out-of-the-money put"

    print("All tests passed.")