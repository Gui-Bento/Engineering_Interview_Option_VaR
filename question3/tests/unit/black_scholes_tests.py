# Define test cases with different scenarios
from question3.black_scholes import black_scholes_call, black_scholes_put


def test_black_scholes():
    # Common parameters
    K = 100      # Strike price
    r = 0.05     # Risk-free interest rate
    T = 1        # Time to maturity (1 year)
    sigma = 0.2  # Volatility

    # In-the-money
    S_in_money = 120
    call_in_money = black_scholes_call(S_in_money, K, T, r, sigma)
    put_in_money = black_scholes_put(S_in_money, K, T, r, sigma)

    # At-the-money
    S_at_money = 100
    call_at_money = black_scholes_call(S_at_money, K, T, r, sigma)
    put_at_money = black_scholes_put(S_at_money, K, T, r, sigma)

    # Out-of-the-money
    S_out_money = 80
    call_out_money = black_scholes_call(S_out_money, K, T, r, sigma)
    put_out_money = black_scholes_put(S_out_money, K, T, r, sigma)

    # Display test results
    print("In-the-money Call:", call_in_money)
    print("In-the-money Put:", put_in_money)
    print("At-the-money Call:", call_at_money)
    print("At-the-money Put:", put_at_money)
    print("Out-of-the-money Call:", call_out_money)
    print("Out-of-the-money Put:", put_out_money)
