from django.http import HttpResponse
import pandas as pd
from ..models import *
from ..constant import *
import datetime
import csv

def trade_position_list(request):
    if request.method == "GET":
        strategy_id = request.GET.get('strategy_id')
        day = int(request.GET.get('day'))
        all_date = StrategyTradePositionList.objects.order_by("create_date").values("create_date").distinct()
        #print(all_date[len(all_date)-1]["create_date"])
        target_position = StrategyTradePositionList.objects.filter(create_date=all_date[len(all_date)-1+day]["create_date"],strategy_id=strategy_id).values()
        hold_position = StrategyTradePositionList.objects.filter(create_date=all_date[len(all_date)-1-1+day]["create_date"],strategy_id=strategy_id).values()
        df_order = generate_order(target_position,hold_position)
        print(df_order)
        return HttpResponse(df_order,content_type='text/csv')
    else:
        strategy_id = request.GET.get('strategy_id')
        file = request.FILES.get('upload_file', None)
        df = pd.read_csv(file,encoding="gb2312")

        date = file.name.split('.')[0].split('_')[1]
        StrategyTradePositionList.objects.filter(create_date=date,strategy_id=strategy_id).delete()


        for index,row in df.iterrows():
            position = StrategyTradePositionList(
                create_date=date,
                code=row[4],
                position=row[5] if row[5]>0 else row[6],
                direction= Direction.LONG.value if row[5]>0 else Direction.SHORT.value,
                strategy_id=strategy_id
            )
            position.save()
        return HttpResponse("put trade list succeed")

def generate_order(target_position,hold_position):
    orders = []
    long = Direction.LONG.value
    short = Direction.SHORT.value
    for hp in hold_position:
        order = {}
        shold_close = True
        # 调整现有仓位
        for tp in target_position:
            if tp['code'] == hp['code'] and tp['direction'] == hp['direction'] :
                diff = tp['position'] - hp['position']
                order['合约id'] = tp['code']
                order['开平（开仓；平仓；平今；平昨）'] = Offset.OPEN if diff>=0 else Offset.CLOSE

                if order['开平（开仓；平仓；平今；平昨）'] == Offset.OPEN:
                    if tp['direction'] == long:
                        order['买卖（买；卖）'] = long
                    else:
                        order['买卖（买；卖）'] = short
                else:
                    if tp['direction'] == long:
                        order['买卖（买；卖）'] = short
                    else:
                        order['买卖（买；卖）'] = long

                order['数量'] = abs(diff)
                if diff != 0:
                    orders.append(order)
                shold_close = False
                break

        # 平老仓位
        if shold_close:
            order['合约id'] = hp['code']
            order['开平（开仓；平仓；平今；平昨）'] = Offset.CLOSE
            order['买卖（买；卖）'] = long if hp['direction'] == short else short
            order['数量'] = hp['position']
            orders.append(order)

    for tp in target_position:

        shold_open = True
        for hp in hold_position:
            if hp['code'] == tp['code'] and hp['direction'] == tp['direction'] :
                shold_open = False
                break

        #开新仓位
        if shold_open:
            order = {}
            order['合约id'] = tp['code']
            order['开平（开仓；平仓；平今；平昨）'] = Offset.OPEN
            order['买卖（买；卖）'] = short if tp['direction'] == short else long
            order['数量'] = tp['position']
            orders.append(order)

    for order in orders:
        order['C\S（本地；云端）'] = "本地"
        order['触发日期（年月日；例如：2019.3.15）'] = datetime.date.today().strftime('%Y.%m.%d')
        order['触发时间（时分秒；例如：13:25）'] = '9:00'
        order['附加条件（是；否）'] = '否'
        order['触发价类型（附加条件）（最新价；买一价；卖一价）'] = ''
        order['触发价方向（附加条件）（向上突破；向下跌破；大于等于；小于等于；大于；小于）'] = ''
        order['触发线（附加条件）'] = ''
        order['委托价（最新价；对手价；市价；自定义）'] = '对手价'
        order['超价'] = ''
        order['自定义委托价'] = ''
        order['追单（是；否）'] = '是'
        order['投保（投机；套保）'] = '投机'
        order['买卖（买；卖）'] = "买" if order['买卖（买；卖）']==long else "卖"
        order['开平（开仓；平仓；平今；平昨）'] = "开仓" if order['开平（开仓；平仓；平今；平昨）'] == Offset.OPEN else "平仓"

    order_context = HttpResponse(content_type='text/csv')  # 告诉浏览器是text/csv格式
    order_context['Content-Disposition'] = 'attachment; filename="somefilename.csv"'  # csv文件名，不影响
    writer = csv.writer(order_context)

    columns = ["合约id","C\S（本地；云端）","触发日期（年月日；例如：2019.3.15）","触发时间（时分秒；例如：13:25）","附加条件（是；否）","触发价类型（附加条件）（最新价；买一价；卖一价）",
     "触发价方向（附加条件）（向上突破；向下跌破；大于等于；小于等于；大于；小于）","触发线（附加条件）","买卖（买；卖）","开平（开仓；平仓；平今；平昨）","委托价（最新价；对手价；市价；自定义）","超价","自定义委托价",
               "数量","追单（是；否）","投保（投机；套保）"]


    writer.writerow(columns)
    for order in orders:
        writer.writerow([order[column] for column in columns])
    return order_context

