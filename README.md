# funny
基于富途， Futu API写的自动下单买卖交易的程序。写这个程序的原因有几个，第一个主要是在国内
美股相当于夜间开票，不方便盯盘。第二个主要是富途App条件订单功能还是比较受限，只能设定买卖
价格区间，没法判断订单是否完成，以及依据订单完成状态，做进一步的操作。
不好的地方是，Futu API获取美股的实时行情是收费的，所以这里并没有尝试去获取实时行情，而是预设
好每天的买卖价格。

初始配置，可以参考https://openapi.futunn.com/futu-api-doc/intro/intro.html，windows需要安装
python 环境，以及相应的 Futu API插件。云服务器ubuntu环境，直接把相应的zip包上传到服务器即可。
安装好后，用自己的futu牛牛账户登录保持在线。

总共有三个交易程序：
第一个：us_market_buy _sell_deal_once.py， 设定一个股票买入，以及卖出的代码，价格，以及数量，
如果下买入单，如果价格达到买入价格，则交易成功。交易成功后，下卖出单，如果价格达到卖出价格，
股票则卖出。一个交易日可以做一次买入和卖出的T操作。 如果一万美元本金，设定买入卖出价格差为1%，
则收益为100美元，扣除交易成本，盈利应该在90美元左右。

第二个：us_market_sell_buy_deal_once.py， 与第一个相似，只不过买卖顺序颠倒，设定一个股票卖出，
以及买入的代码，价格，以及数量，如果下卖出单，如果价格达到卖出价格，则交易成功。交易成功后，
下买入单，如果价格达到买入价格，股票则买入。一个交易日可以做一次卖出和买入的T操作。 如果一万美
元本金，设定买入卖出价格差为1%，则相当于持仓成本减少100美元，也就是收益为100美元，扣除交易成本，
盈利应该在90美元左右。

第三个：us_market_gradient_deal_repeat.py 与第一个相似，先买入后卖出，只不过可以反复重复买入卖出
操作，如果行情也是锯齿状，那么可以反复获利。

vx：zhuzhu20202023


