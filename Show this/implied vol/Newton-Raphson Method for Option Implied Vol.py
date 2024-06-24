#new implied vol = old implied vol - (BSM value(using the old implied vol)-current market price)/vega
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import vega#there is delta, gamma, theta,rho

def implied_vol(S, K, T, r, market_price, flag = "c", tolerance = 0.0001):#flag is option type "c"=call, "p"=put

    max_guesses = 200 #max nr. of guesses meaning xn is the first guess the nyou get xn+1 which you plot and use the same slope to get xn+2
    vol_old = 0.3 #initial guess (like you pick a value for imp vol map it to the function take the slope, get the next guess at the intersection with the x-axis and repeat)

    for k in range(max_guesses):
        bs_price= bs(flag, S, K, T, r, vol_old)
        vega_slope= vega(flag, S, K,T,r, vol_old)*100
        C= bs_price - market_price

        vol_new = vol_old - C/vega_slope
        new_bs_price = bs(flag, S, K, T, r, vol_new)

        if (abs(vol_old-vol_new)< tolerance or abs(new_bs_price-market_price)<tolerance):
            break
        vol_old=vol_new
    return vol_new

S=30
K=28
T=0.5
r=0.025
market_price=3.7
print(implied_vol(S, K, T, r, market_price)*100)