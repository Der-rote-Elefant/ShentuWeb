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
        df = pd.read_csv(file,encoding="gbk")

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
    for hp in hold_position:
        order = {}
        shold_close = True
        # 调整现有仓位
        for tp in target_position:
            if tp['code'] == hp['code'] and tp['direction'] == hp['direction'] :
                diff = tp['position'] - hp['position']
                order['code'] = tp['code']
                order['offset'] = Offset.OPEN if diff>0 else Offset.CLOSE

                if order['offset'] == Offset.OPEN:
                    if tp['direction'] == Direction.LONG:
                        order['direction'] = Direction.LONG
                    else:
                        order['direction'] = Direction.SHORT
                else:
                    if tp['direction'] == Direction.LONG:
                        order['direction'] = Direction.SHORT
                    else:
                        order['direction'] = Direction.LONG

                order['vol'] = abs(diff)
                if diff != 0:
                    orders.append(order)
                shold_close = False
                break

        # 平老仓位
        if shold_close:
            order['code'] = hp['code']
            order['offset'] = Offset.CLOSE
            order['direction'] = Direction.LONG if hp['direction'] == Direction.SHORT else Direction.SHORT
            order['vol'] = hp['position']
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
            order['code'] = tp['code']
            order['offset'] = Offset.OPEN
            order['direction'] = Direction.SHORT if tp['direction'] == Direction.SHORT else Direction.LONG
            order['vol'] = tp['position']
            orders.append(order)

    for order in orders:
        order['cs'] = "本地"
        order['date'] = datetime.date.today().strftime('%Y.%m.%d')
        order['time'] = '9:00'
        order['condition'] = '否'
        order['p1'] = ''
        order['p2'] = ''
        order['p3'] = ''
        order['price'] = '对手价'
        order['p4'] = ''
        order['p5'] = ''
        order['p6'] = ''
        order['bidden'] = '是'
        order['type'] = '投机'
        order['direction'] = "买" if order['direction']==Direction.LONG else "卖"
        order['offset'] = "开仓" if order['offset'] == Offset.OPEN else "平仓"

    order_context = HttpResponse(content_type='text/csv')  # 告诉浏览器是text/csv格式
    order_context['Content-Disposition'] = 'attachment; filename="somefilename.csv"'  # csv文件名，不影响
    writer = csv.writer(order_context)
    columns = ['code', 'cs','date','time','condition','p1','p2','p3','direction','offset','price','p4','p5','p6','vol','bidden','type']
    writer.writerow(columns)
    for order in orders:
        writer.writerow([order[column] for column in columns])
    return order_context

