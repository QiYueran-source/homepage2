# 现代投资组合理论与Python实现

## 引言

投资组合理论是现代金融学的基石，由Harry Markowitz于1952年提出。通过合理分配资产，可以在控制风险的前提下最大化收益。

## 核心概念

### 1. 预期收益
投资组合的预期收益是各资产收益的加权平均：

$$E(R_p) = \sum_{i=1}^{n} w_i E(R_i)$$

其中 $w_i$ 是资产i的权重，$E(R_i)$ 是资产i的预期收益。

### 2. 投资风险
使用方差衡量投资组合的波动性：

$$\sigma_p^2 = \sum_{i=1}^{n} \sum_{j=1}^{n} w_i w_j \sigma_{ij}$$

### 3. 相关性
资产之间的相关系数决定了分散风险的效果。

## Python实现

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 示例代码：计算投资组合收益和风险
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights)
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, std

# 最小化方差的优化函数
def minimize_volatility(weights, mean_returns, cov_matrix):
    return portfolio_performance(weights, mean_returns, cov_matrix)[1]
```

## 实际应用

通过Python可以实现：
- 有效前沿计算
- 最优投资组合选择
- 风险-收益分析
- 再平衡策略

这种量化方法为投资者提供了科学的决策工具。
