from futu import *
import sys
import os
import datetime


 ### 美股自动下单程序 ###
 ### intialize parameters setting ###
stock_name = "US.AMD"
basic_price = 140 #上一日收盘价
basic_number = 0 # 账户这只股票仓位，需要从账户读出
first_sell_number = 10 #第一次卖出数目
#second_sell_number = 3 #第二次卖出数目
first_sell_price = 143 #第一次卖出价格
#second_sell_price = 118 #第二次卖出价格
first_buy_number = 10 #第一次买入数目
#second_buy_number = 3 #第二次买入数目
first_buy_price = 138 #第一次买入价格
#second_buy_price = 108 #第二次买入价格


pwd_unlock = '******'

today = datetime.date.today()
output_file = "output-" + str(today) + ".txt"


sell_flag = True

with open(output_file, 'a') as f:
    print(stock_name, " begin to run deal !!!!!!!!!!!!!!!!!!!!! ", file=f)

while True:
    ### 打开交易接口， 查看账户中指定的股票的持仓情况，资金情况
    trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.US, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
    ret, data = trd_ctx.position_list_query()
    if ret == RET_OK:
        print(data)
        if data.shape[0] > 0:  # 如果持仓列表不为空
            code = data['code'].values.tolist()
            print(code)  # 获取持仓股票列表
            if stock_name in code:
                index = code.index(stock_name)
                # print(index)
                current_number = data['qty'][index]
            else:
                current_number = 0
            with open(output_file, 'a') as f:
                print(stock_name, "sock count before deal ", current_number, file=f)
    else:
        print('position_list_query error: ', data)

    ### 打开交易接口，查询账号资金
    ret, data = trd_ctx.accinfo_query()
    if ret == RET_OK:
        print("current maxpower is ",data['power'][0])  # 取第一行的购买力
    else:
        print('accinfo_query error: ', data)


    ### 买操作， 先检查账户里面是否有这只股票，如果没有，就是0
    ret, data = trd_ctx.unlock_trade(pwd_unlock)  # 若使用真实账户下单，需先对账户进行解锁。此处示例为模拟账户下单，也可省略解锁。
    if ret == RET_OK:
        ret, data = trd_ctx.position_list_query()
        if ret == RET_OK:
            if data.shape[0] > 0:  # 如果持仓列表不为空
                code = data['code'].values.tolist()
                if stock_name in code:
                    index = code.index(stock_name)
                    current_number = data['qty'][index]
                else:
                    current_number = 0
                with open(output_file, 'a') as f:
                    print(stock_name, "sock count before buy ", current_number, file=f)
                ### 如果当前仓位等于基准仓位，就可以执行买入操作
                if (current_number == basic_number) and (sell_flag ==  True):
                    with open(output_file, 'a') as f:
                        now = datetime.datetime.now()
                        print(stock_name, "sell deal successfully", now, file=f)
                    ret, data = trd_ctx.place_order(price=first_buy_price, qty=first_buy_number, code=stock_name, trd_side=TrdSide.BUY,
                                                    trd_env=TrdEnv.REAL)
                    if ret == RET_OK:
                        sell_flag = False
                        with open(output_file, 'a') as f:
                            now = datetime.datetime.now()
                            print(stock_name, "buy order placed successfully", now, file=f)
                            print(data, file=f)
                    else:
                        print('place_order error: ', data)
        else:
            print('position_list_query error: ', data)
    else:
        print('unlock_trade failed: ', data)

    time.sleep(60)

    ###卖操作， 先检查账户是否有这只股票，如果没有，仓位就是0
    ret, data = trd_ctx.unlock_trade(pwd_unlock)  # 若使用真实账户下单，需先对账户进行解锁。此处示例为模拟账户下单，也可省略解锁。
    if ret == RET_OK:
        ret, data = trd_ctx.position_list_query()
        if ret == RET_OK:
            if data.shape[0] > 0:  # 如果持仓列表不为空
                code = data['code'].values.tolist()
                if stock_name in code:
                    index = code.index(stock_name)
                    current_number = data['qty'][index]
                else:
                    current_number = 0
                with open(output_file, 'a') as f:
                    print(stock_name, "sock count before sell ", current_number, file=f)
                #### 如果当前仓位等于基准仓位加入买入仓位，就可以开始执行卖出操作
                if current_number == (basic_number + first_buy_number):
                    with open(output_file, 'a') as f:
                        now = datetime.datetime.now()
                        print(stock_name, "buy order deal  successfully", now, file=f)
                    ret, data = trd_ctx.place_order(price=first_sell_price, qty=first_sell_number, code=stock_name, trd_side=TrdSide.SELL,
                                                    trd_env=TrdEnv.REAL)
                    if ret == RET_OK:
                        sell_flag = True
                        with open(output_file, 'a') as f:
                            now = datetime.datetime.now()
                            print(stock_name, "sell order placed successfully", now, file=f)
                            print(data, file=f)
                    else:
                        print('place_order error: ', data)
        else:
            print('position_list_query error: ', data)
    else:
        print('unlock_trade failed: ', data)
    trd_ctx.close()  # 关闭当条连接
    time.sleep(60)








