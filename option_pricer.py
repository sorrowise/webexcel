"""
欧式期权定价计算模块
使用Black-Scholes模型计算欧式看涨和看跌期权价格及希腊字母
"""

import numpy as np
from scipy.stats import norm


def black_scholes_call(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看涨期权的Black-Scholes价格
    
    参数:
    S: 标的资产当前价格
    K: 执行价格
    T: 到期时间(年)
    r: 无风险利率
    sigma: 波动率
    q: 股息率(默认为0)
    
    返回:
    看涨期权价格
    """
    if T <= 0 or sigma <= 0:
        return 0.0
    
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    return float(call_price)


def black_scholes_put(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看跌期权的Black-Scholes价格
    
    参数:
    S: 标的资产当前价格
    K: 执行价格
    T: 到期时间(年)
    r: 无风险利率
    sigma: 波动率
    q: 股息率(默认为0)
    
    返回:
    看跌期权价格
    """
    if T <= 0 or sigma <= 0:
        return 0.0
    
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    
    return float(put_price)


def calculate_greeks(S, K, T, r, sigma, q=0.0):
    """
    计算期权的希腊字母
    
    参数:
    S: 标的资产当前价格
    K: 执行价格
    T: 到期时间(年)
    r: 无风险利率
    sigma: 波动率
    q: 股息率(默认为0)
    
    返回:
    包含Delta, Gamma, Vega, Theta, Rho的字典
    """
    if T <= 0 or sigma <= 0:
        return {
            'delta_call': 0.0,
            'delta_put': 0.0,
            'gamma': 0.0,
            'vega': 0.0,
            'theta_call': 0.0,
            'theta_put': 0.0,
            'rho_call': 0.0,
            'rho_put': 0.0
        }
    
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Delta
    delta_call = np.exp(-q * T) * norm.cdf(d1)
    delta_put = -np.exp(-q * T) * norm.cdf(-d1)
    
    # Gamma (看涨和看跌相同)
    gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Vega (看涨和看跌相同)
    vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) / 100  # 除以100，表示1%波动率变化的影响
    
    # Theta
    theta_call = (-S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                   - r * K * np.exp(-r * T) * norm.cdf(d2)
                   + q * S * np.exp(-q * T) * norm.cdf(d1)) / 365  # 每天的时间价值
    theta_put = (-S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                  + r * K * np.exp(-r * T) * norm.cdf(-d2)
                  - q * S * np.exp(-q * T) * norm.cdf(-d1)) / 365  # 每天的时间价值
    
    # Rho
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100  # 除以100，表示1%利率变化的影响
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100  # 除以100，表示1%利率变化的影响
    
    return {
        'delta_call': float(delta_call),
        'delta_put': float(delta_put),
        'gamma': float(gamma),
        'vega': float(vega),
        'theta_call': float(theta_call),
        'theta_put': float(theta_put),
        'rho_call': float(rho_call),
        'rho_put': float(rho_put)
    }


def calculate_option_price(S, K, T, r, sigma, q=0.0):
    """
    计算期权价格和希腊字母的完整函数
    
    参数:
    S: 标的资产当前价格
    K: 执行价格
    T: 到期时间(年)
    r: 无风险利率
    sigma: 波动率
    q: 股息率(默认为0)
    
    返回:
    包含所有计算结果的字典
    """
    try:
        call_price = black_scholes_call(S, K, T, r, sigma, q)
        put_price = black_scholes_put(S, K, T, r, sigma, q)
        greeks = calculate_greeks(S, K, T, r, sigma, q)
        
        return {
            'call_price': call_price,
            'put_price': put_price,
            'greeks': greeks,
            'success': True,
            'message': '计算成功'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'计算错误: {str(e)}'
        }
