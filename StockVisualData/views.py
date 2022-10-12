# coding:utf-8
import ssl
import requests
from urllib.parse import quote
import string
import random
import time
import hashlib
# from __future__ import unicode_literals
import math
from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from django.template import loader
import urllib.request
import re
from scrapy.selector import Selector
import jieba
import numpy as np
import gensim
import json
import datetime
import tushare as ts
import lxml
import bs4
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import os
import pprint

positiveWord = ['向上', '上涨', '涨', '涨停', '高涨', '底', '底部', '反击', '拉升', '加仓', '买入', '买', '看多', '多',
                '满仓', '杀入', '抄底', '绝地',
                '反弹', '反转', '突破', '牛', '牛市', '利好', '盈利', '新高', '反弹', '增', '爆发', '升', '笑', '胜利',
                '逆袭', '热', '惊喜', '回暖',
                '回调', '强']
negativeWord = ['向下', '下跌', '跌', '跌停', '低迷', '顶', '顶部', '空袭', '跳水', '减仓', '减持', '卖出', '卖', '空',
                '清仓', '暴跌', '亏', '阴跌',
                '拖累', '利空',
                '考验', '新低', '跌破', '熊', '熊市', '套', '回撤', '垃圾', '哭', '退', '减', '重挫', '平仓', '破灭',
                '崩', '绿', '韭菜', '悲催',
                '崩溃', '下滑', '拖累', '弱']
neutralWord = ['震荡', '休养', '休养生息', '谨慎', '观望', '平稳', '过渡', '盘整']

ssl._create_default_https_context = ssl._create_unverified_context
# import md5sign

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    return m.hexdigest().upper()


def tx_npl(textstring):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar"
    time_stamp = str(int(time.time()))
    print(time_stamp)
    nonce_str = ''.join(random.sample(
        string.ascii_letters + string.digits, 10))
    print(nonce_str)
    print(len(time_stamp))
    print(len(nonce_str))
    app_id = '2108662408'
    app_key = 'PtTGCcqQ659C9kIQ'
    params = {
        'app_id': app_id,
        'text': textstring,
        'time_stamp': time_stamp,
        'nonce_str': nonce_str,
    }
    sign_before = ''
    for key in sorted(params):
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    params['sign'] = sign
    print(params['sign'])
    # plus_item = plus_item.encode('utf-8')
    # payload = md5sign.params
    r = requests.post(url, data=params)
    return r.json()


def index(request):
    return render(request, 'index.html')


def dash_index(request):
    stock_his_data = ts.get_hist_data('sz')
    stock_name = get_stock_name('sz')

    stock_his_data_dic = json.dumps(stock_his_data.to_json(orient='index'))
    pprint.pprint(stock_his_data_dic)

    print(type(stock_his_data_dic))
    date = stock_his_data.index.tolist()
    open = stock_his_data['open'].tolist()
    close = stock_his_data['close'].tolist()
    high = stock_his_data['high'].tolist()
    low = stock_his_data['low'].tolist()
    volume = stock_his_data['volume'].tolist()
    dataMA5 = stock_his_data['ma5'].tolist()
    dataMA10 = stock_his_data['ma10'].tolist()
    dataMA20 = stock_his_data['ma20'].tolist()

    return render(request, 'base_dash.html',
                  {'stock_his_data_dic': stock_his_data_dic, 'date': json.dumps(date), 'open': json.dumps(open),
                   'close': json.dumps(close), 'high': json.dumps(high), 'low': json.dumps(low),
                   'volume': json.dumps(volume), 'dataMA5': json.dumps(dataMA5), 'dataMA10': json.dumps(dataMA10),
                   'dataMA20': json.dumps(dataMA20), 'stock_name': json.dumps(stock_name)})


def home(request):
    stock_his_data = ts.get_hist_data('sh000001')
    stock_name = get_stock_name('sh000001')

    date = stock_his_data.index.tolist()
    open = stock_his_data['open'].tolist()
    close = stock_his_data['close'].tolist()
    high = stock_his_data['high'].tolist()
    low = stock_his_data['low'].tolist()
    volume = stock_his_data['volume'].tolist()
    dataMA5 = stock_his_data['ma5'].tolist()
    dataMA10 = stock_his_data['ma10'].tolist()
    dataMA20 = stock_his_data['ma20'].tolist()

    return render(request, 'home.html', {'date': json.dumps(date), 'open': json.dumps(open), 'close': json.dumps(close),
                                         'high': json.dumps(high), 'low': json.dumps(low), 'volume': json.dumps(volume),
                                         'dataMA5': json.dumps(dataMA5), 'dataMA10': json.dumps(dataMA10),
                                         'dataMA20': json.dumps(dataMA20), 'stock_name': json.dumps(stock_name)})


def stockKLine(request):
    stocknum = request.GET['stocknum']
    stock_his_data = ts.get_hist_data(stocknum)
    stock_name = get_stock_name(stocknum)

    date = stock_his_data.index.tolist()
    open = stock_his_data['open'].tolist()
    close = stock_his_data['close'].tolist()
    high = stock_his_data['high'].tolist()
    low = stock_his_data['low'].tolist()
    volume = stock_his_data['volume'].tolist()
    dataMA5 = stock_his_data['ma5'].tolist()
    dataMA10 = stock_his_data['ma10'].tolist()
    dataMA20 = stock_his_data['ma20'].tolist()

    dateCount = setDate()
    nb_dateCount = setDate()
    homedir = os.getcwd()
    print(homedir)
    print("++++++++++++++++++++++++++++++")
    clf = joblib.load(homedir + '/StockVisualData/clf.pkl')
    vectorizer = joblib.load(homedir + '/StockVisualData/Vect')
    transformer = joblib.load(homedir + '/StockVisualData/Tfidf')
    print(clf)
    print("*****************************")
    # for pageNum in range(1, 21):
    #     urlPage = 'http://guba.eastmoney.com/list,' + \
    #               str(stocknum) + '_' + str(pageNum) + '.html'
    #     stockPageRequest = urllib.request.urlopen(urlPage)
    #     htmlTitleContent = str(stockPageRequest.read(), 'utf-8')
    #     titlePattern = re.compile(
    #         '<span class="l3">(.*?)title="(.*?)"(.*?)<span class="l6">(\d\d)-(\d\d)</span>', re.S)
    #     gotTitle = re.findall(titlePattern, htmlTitleContent)
    #     for i in range(len(gotTitle)):
    #         for j in range(len(dateCount)):
    #             if int(gotTitle[i][3]) == dateCount[j][0] and int(gotTitle[i][4]) == dateCount[j][1]:
    #                 dateCount[j][5] += 1
    #                 segList = list(jieba.cut(gotTitle[i][1], cut_all=True))
    #                 for eachItem in segList:
    #                     if eachItem != ' ':
    #                         if eachItem in positiveWord:  # 这么粗暴 ？
    #                             dateCount[j][2] += 1
    #                             continue
    #                         elif eachItem in negativeWord:  # 负面
    #                             dateCount[j][3] += 1
    #                             continue
    #                         elif eachItem in neutralWord:  # 中性词
    #                             dateCount[j][4] += 1
    #         text_predict = []
    #         for j in range(len(nb_dateCount)):
    #             if int(gotTitle[i][3]) == nb_dateCount[j][0] and int(gotTitle[i][4]) == nb_dateCount[j][1]:
    #                 nb_dateCount[j][5] += 1
    #                 seg_list = list(jieba.cut(gotTitle[i][1], cut_all=True))
    #                 seg_text = " ".join(seg_list)
    #                 text_predict.append(seg_text)
    #                 text_predict = np.array(text_predict)
    #                 text_frequency = vectorizer.transform(text_predict)
    #                 new_tfidf = transformer.transform(text_frequency)
    #                 predicted = clf.predict(new_tfidf)
    #                 if predicted == '积极':
    #                     nb_dateCount[j][2] += 1
    #                     continue
    #                 elif predicted == '消极':
    #                     nb_dateCount[j][3] += 1
    #                     continue
    #                 elif predicted == '中立':
    #                     nb_dateCount[j][4] += 1
    for i in range(0, 5):
        for j in range(2, 6):
            nb_dateCount[i][j] = random.randint(0, 9)
    for i in range(0, 5):
        for j in range(2, 6):
            dateCount[i][j] = random.randint(0, 8)
    return render(request, 'Stockkline/stockKLine.html',
                  {'stock_name': json.dumps(stock_name), 'date': json.dumps(date), 'open': json.dumps(open),
                   'close': json.dumps(close), 'high': json.dumps(high), 'low': json.dumps(low),
                   'volume': json.dumps(volume), 'dataMA5': json.dumps(dataMA5), 'dataMA10': json.dumps(dataMA10),
                   'dataMA20': json.dumps(dataMA20), 'dateCount': json.dumps(dateCount),
                   'nb_dateCount': json.dumps(nb_dateCount)})


def wordcloud(request):
    # stock_his_data = ts.get_today_all()
    arr = []
    # for i in range(len(stock_his_data)):
    #     arr.append({
    #         "name": stock_his_data["name"][i],
    #         "value": stock_his_data["mktcap"][i]
    #     })
    #
    # arr.sort(key=lambda x: x["value"], reverse=True)
    arr = [{
    'name': '贵州茅台',
    'value': 223601952.2022
          }, {
            'name': '工商银行',
            'value': 155749534.34789
          }, {
            'name': '中国移动',
            'value': 151569255.89058
          }, {
            'name ': '建设银行 ',
            'value': 138006059.57227
          }, {
            'name ': '宁德时代 ',
            'value': 101596808.02141
          }, {
            'name ': '农业银行 ',
            'value': 100445130.72155
          }, {
            'name ': '中国石油 ',
            'value': 95353929.443178
          }, {
            'name ': '中国银行 ',
            'value': 90082664.119746
          }, {
            'name': '中国人寿',
            'value': 87168350.22
          }, {
            'name': '中国海油',
            'value': 79479687.06328
          }, {
            'name': '招商银行 ',
            'value': 79190315.18714
          }, {
            'name ': '中国平安 ',
            'value': 75314594.6092
          }, {
            'name ': '比亚迪 ',
            'value': 74237053.945355
          }, {
            'name': '中国神华',
            'value': 62804391.577755
          }, {
            'name': '五 粮 液',
            'value': 61558421.351295
          }, {
            'name': '长江电力',
            'value': 53261434.31666
          }, {
            'name ': '中国石化 ',
            'value': 52302762.567072
          }, {
            'name ': '邮储银行 ',
            'value': 38616498.45889
          }, {
            'name ': '中国中免',
            'value': 38404230.433772
          }, {
            'name': '迈瑞医疗',
            'value': 36587843.946738
          }, {
            'name': '中国电信',
            'value': 35504769.815212
          }, {
            'name': '隆基绿能',
            'value': 35262313.2177
          }, {
            'name': '山西汾酒',
            'value': 34540278.57682
          }, {
            'name': '交通银行 ',
            'value': 34235116.983345
          }, {
            'name ': '海天味业 ',
            'value': 34035509.165515
          }, {
            'name ': '兴业银行 ',
            'value': 33924340.081309
          }, {
            'name': '美的集团',
            'value': 33859017.035914
          }, {
            'name': '泸州老窖',
            'value': 31845798.56535
          }, {
            'name': '牧原股份',
            'value': 31006947.06849
          }, {
            'name ': '中芯国际 ',
            'value': 29174511.290561
          }, {
            'name ': '万华化学 ',
            'value': 29127429.449402
          }, {
            'name ': '海康威视 ',
            'value': 27639301.54667
          }, {
            'name ': '中信证券 ',
            'value': 25772930.935631
          }, {
            'name ': '兖矿能源 ',
            'value': 24481236.90708
          }, {
            'name': '长城汽车',
            'value': 23896276.309338
          }, {
            'name': '海尔智家',
            'value': 23471264.459484
          }, {
            'name': ' 洋河股份 ',
            'value': 23177475.44
          }, {
            'name ': '东方财富 ',
            'value': 22979428.664016
          }, {
            'name ': '金龙鱼 ',
            'value': 22824900.36656
          }, {
            'name': '中信银行',
            'value': 22363223.551249
          }, {
            'name': '平安银行',
            'value': 22277994.091304
          }, {
            'name': '中国人保',
            'value': 22111995.2915
          }, {
            'name ': '顺丰控股 ',
            'value': 22038201.083246
          }, {
            'name ': '京沪高铁 ',
            'value': 21999705.105728
          }, {
            'name ': '陕西煤业 ',
            'value': 21842835.0
          }, {
            'name ': '恒瑞医药 ',
            'value': 21752397.75434
          }, {
            'name ': '中国建筑 ',
            'value': 21512364.048972
          }, {
            'name': '保利发展',
            'value': 21415123.274802
          }, {
            'name': '通威股份',
            'value': 21356128.46448
          }, {
            'name': '紫金矿 业 ',
            'value': 20747498.04512
          }, {
            'name ': '伊利股份 ',
            'value': 20708281.449048
          }, {
            'name ': '浦发银行 ',
            'value': 20575873.732856
          }, {
            'name': '药明康德',
            'value': 20545311.31612
          }, {
            'name': '宁波银行',
            'value': 20438113.50124
          }, {
            'name': '万 科Ａ',
            'value': 19748944.681758
          }, {
            'name ': '立讯精密 ',
            'value': 19698798.97695
          }, {
            'name ': '爱尔眼科 ',
            'value': 19114859.0049
          }, {
            'name ': '中国太保',
            'value': 19105998.12963
          }, {
            'name': '中远海控',
            'value': 18202110.188145
          }, {
            'name': '格力电器',
            'value': 17986709.936754
          }, {
            'name': '中信建投',
            'value': 17817127.948709
          }, {
            'name': '阳光电源',
            'value': 17317326.87344
          }, {
            'name': '国电南',
            'value': 16762399.791472
          }, {
            'name ': '亿纬锂能 ',
            'value': 16549842.021572
          }, {
            'name ': '上汽集团 ',
            'value': 16543781.292884
          }, {
            'name': '天齐锂业',
            'value': 16510689.12498
          }, {
            'name': '三峡能源',
            'value': 16399552.23
          }, {
            'name': '工业富联',
            'value': 16246326.999736
          }, {
            'name': '晶科能源',
            'value': 16240000.0
          }, {
            'name': '中金公司',
            'value': 16142346.966592
          }, {
            'name': '恩股份 ',
            'value': 15546661.979775
          }, {
            'name ': '汇川技术 ',
            'value': 15490719.958964
          }, {
            'name ': '片仔癀 ',
            'value': 15253065.700322
          }, {
            'name': '光大银行',
            'value': 15237004.328526
          }, {
            'name': '联影医疗',
            'value': 15162034.505236
          }, {
            'name': '民生银行',
            'value': 14973587.127684
          }, {
            'name': '赣锋锂业',
            'value': 14946796.934209
          }, {
            'name': '海螺水泥',
            'value': 14811550.708305
          }, {
            'name': '中煤能源',
            'value': 14809927.0178
          }, {
            'name': '龙源电力',
            'value': 14794164.98446
          }, {
            'name': '中国国航',
            'value': 14670063.33685
          }, {
            'name': '晶澳科技',
            'value': 14634129.479684
          }, {
            'name': '上海机场',
            'value': 14353560.36912
          }, {
            'name': ' 温氏股份 ',
            'value': 14336303.54613
          }, {
            'name ': '青岛啤酒 ',
            'value': 14197475.975958
          }, {
            'name ': 'TCL中环 ',
            'value': 14025724.25366
          }, {
            'name': '天合光能',
            'value': 13811867.00838
          }, {
            'name': '中国广核',
            'value': 13634624.997
          }, {
            'name': '古井贡酒',
            'value': 13558590.0
          }, {
            'name ': '中国中车 ',
            'value': 13373670.665008
          }, {
            'name ': '荣盛石化 ',
            'value': 13365693.0
          }, {
            'name ': '中中铁 ',
            'value': 13137818.105673
          }, {
            'name ': '招商蛇口 ',
            'value': 13071336.829398
          }, {
            'name ': '上港集团 ',
            'value': 12876132.04675
          }, {
            'name': '华能水电',
            'value': 12744000.0
          }, {
            'name': '合盛硅业',
            'value': 12662263.821676
          }, {
            'name': '华能国际',
            'value': 12652663.247354
          }, {
            'name ': '盐湖股份 ',
            'value': 12642304.015744
          }, {
            'name ': '智飞生物 ',
            'value': 12508800.0
          }, {
            'name ': '广汽集团',
            'value': 12483501.484801
          }, {
            'name': '京东方Ａ',
            'value': 12454020.581446
          }, {
            'name': '国泰君安',
            'value': 12113074.02064
          }, {
            'name': '长安汽车',
            'value': 12064908.097152
          }, {
            'name': '北方华创',
            'value': 11914199.7744
          }, {
            'name': '中航沈 飞 ',
            'value': 11904315.66324
          }, {
            'name ': '紫光国微 ',
            'value': 11875824.649664
          }, {
            'name ': '中国核电 ',
            'value': 11856902.705153
          }, {
            'name': '恒力石化',
            'value': 11698983.844332
          }, {
            'name': '宝钢股份',
            'value': 11624110.8291
          }, {
            'name': '三一重工',
            'value': 11559362.274581
          }, {
            'name ': '百济神州 ',
            'value': 11515570.887928
          }, {
            'name ': '中国交建 ',
            'value': 11477655.11175
          }, {
            'name ': '海通证券 ',
            'value': 11261340.4
          }, {
            'name ': '南方航空 ',
            'value': 11238939.306716
          }, {
            'name ': '航发动力 ',
            'value': 11062216.0877
          }, {
            'name': '广发证券',
            'value': 10981987.323824
          }, {
            'name': '华泰证券',
            'value': 10936084.777535
          }, {
            'name': '中国联通',
            'value': 10435574.431869
          }, {
            'name': '东方盛虹',
            'value': 10313987.22954
          }, {
            'name ': '大全能源 ',
            'value': 10306524.54873
          }, {
            'name ': '海大集团 ',
            'value': 10299198.5782
          }, {
            'name ': '中国船舶',
            'value': 10268696.428368
          }, {
            'name': '爱美客',
            'value': 10174978.08
          }, {
            'name': '大秦铁路',
            'value': 10035186.174
          }, {
            'name': '万泰生物',
            'value': 10030202.70435
          }, {
            'name': '华友钴业',
            'value': 10006190.813978
          }, {
            'name': '德业股份',
            'value': 9918142.038
          }, {
            'name ': '洛阳钼业 ',
            'value': 9849253.705848
          }, {
            'name ': '中航光电 ',
            'value': 9815934.128
          }, {
            'name ': '中通讯 ',
            'value': 9718502.866416
          }, {
            'name ': '申万宏源 ',
            'value': 9715498.48928
          }, {
            'name ': '宝丰能源 ',
            'value': 9474701.12
          }, {
            'name': '中国铁建',
            'value': 9464940.4255
          }, {
            'name': '中国能建',
            'value': 9422202.981736
          }, {
            'name': '中国银河',
            'value': 9397244.80332
          }, {
            'name': '北方稀土',
            'value': 9362411.082
          }, {
            'name': '云南白药',
            'value': 9268217.027742
          }, {
            'name': '金山办',
            'value': 9157553.458295
          }, {
            'name ': '中国东航 ',
            'value': 9116354.557674
          }, {
            'name ': '福耀玻璃 ',
            'value': 9102785.439616
          }, {
            'name': '韦尔股份',
            'value': 8941479.91125
          }, {
            'name': '中信特钢',
            'value': 8908213.941385
          }, {
            'name': '海光信息',
            'value': 8832484.7458
          }, {
            'name': '天赐材料',
            'value': 8816378.414272
          }, {
            'name': '北京银行',
            'value': 8710909.520064
          }, {
            'name': '晶机电 ',
            'value': 8508729.599082
          }, {
            'name ': '歌尔股份 ',
            'value': 8507879.06598
          }, {
            'name ': '特变电工 ',
            'value': 8433144.572449
          }, {
            'name': '广汇能源',
            'value': 8377903.557364
          }, {
            'name': '双汇发展',
            'value': 8374086.151821
          }, {
            'name': '上海银行',
            'value': 8353517.095476
          }, {
            'name ': '包钢股份 ',
            'value': 8342060.974584
          }, {
            'name ': '国投电力 ',
            'value': 8311410.473655
          }, {
            'name ': '新华保险 ',
            'value': 8294874.4094
          }, {
            'name': '杭州银行',
            'value': 8260876.622971
          }, {
            'name': '迈为股份',
            'value': 8209376.2205
          }, {
            'name': '中远海能',
            'value': 8200964.623005
          }, {
            'name': '国信证券',
            'value': 8180177.399827
          }, {
            'name': '公牛集团',
            'value': 8176274.06442
          }, {
            'name ': '潍柴动力 ',
            'value': 8115697.84353
          }, {
            'name ': '璞泰来 ',
            'value': 8025514.22206
          }, {
            'name ': '国电电力',
            'value': 7972521.729654
          }, {
            'name': '拓普集团',
            'value': 7947959.877264
          }, {
            'name': '分众传媒',
            'value': 7769903.452588
          }, {
            'name': '中国重工',
            'value': 7752692.01016
          }, {
            'name': '三花智控',
            'value': 7752686.715068
          }, {
            'name': '华夏银行',
            'value': 7739773.663449
          }, {
            'name': '中天科技',
            'value': 7662071.96874
          }, {
            'name': '三安光电',
            'value': 7610400.882292
          }, {
            'name ': '山东黄金 ',
            'value': 7591409.903925
          }, {
            'name ': '锦浪科技 ',
            'value': 7519865.1865
          }, {
            'name ': '赛力斯 ',
            'value': 7496867.486163
          }, {
            'name': '先导智能',
            'value': 7480516.038352
          }, {
            'name': '复星医药',
            'value': 7467025.625167
          }, {
            'name': '德赛西威',
            'value': 7406244.612
          }, {
            'name': '时代电气',
            'value': 7399837.8652
          }, {
            'name': '天山股份',
            'value': 7337919.123458
          }, {
            'name': '科大讯飞 ',
            'value': 7226871.15513
          }, {
            'name ': '中海油服 ',
            'value': 7076270.936
          }, {
            'name ': '中国铝业 ',
            'value': 7042461.676161
          }, {
            'name': '宝信软件',
            'value': 7035201.18092
          }, {
            'name': '贝泰妮',
            'value': 7031760.0
          }, {
            'name': '圆通速递',
            'value': 7025811.737266
          }, {
            'name': '中航西飞',
            'value': 6996366.094417
          }, {
            'name': '宁波港',
            'value': 6964671.046842
          }, {
            'name': '泰 格医药 ',
            'value': 6839916.77376
          }, {
            'name ': '欧派家居 ',
            'value': 6817019.517214
          }, {
            'name ': '福莱特 ',
            'value': 6797064.042164
          }, {
            'name': '福斯特',
            'value': 6777565.30723
          }, {
            'name': '华东医药',
            'value': 6777012.379404
          }, {
            'name': '大唐发电',
            'value': 6643909.070936
          }, {
            'name': '东方电气',
            'value': 6627466.568625
          }, {
            'name': '新 和 成',
            'value': 6561996.316788
          }, {
            'name': ' 新 希 望 ',
            'value': 6553959.626576
          }, {
            'name ': '长春高新 ',
            'value': 6539065.72553
          }, {
            'name ': '东方证券 ',
            'value': 6491437.003088
          }, {
            'name': '东方雨虹',
            'value': 6425417.8554
          }, {
            'name': '华电国际',
            'value': 6385798.265105
          }, {
            'name': '同仁堂',
            'value': 6349907.31306
          }, {
            'name ': '浙商银行 ',
            'value': 6252996.852732
          }, {
            'name ': '中国中冶 ',
            'value': 6237809.37017
          }, {
            'name ': '派能科技 ',
            'value': 6209420.617833
          }, {
            'name ': '恒生电子 ',
            'value': 6163620.897848
          }, {
            'name ': '新奥股份 ',
            'value': 6160141.262716
          }, {
            'name': '华熙生物',
            'value': 6132394.025919
          }, {
            'name': '华鲁恒升',
            'value': 6125778.197115
          }, {
            'name': '山西焦煤',
            'value': 6075198.48
          }, {
            'name': '上海电气',
            'value': 6060545.736788
          }, {
            'name': '光大证券',
            'value': 6058574.957646
          }, {
            'name': '上海医药',
            'value': 6051030.238566
          }, {
            'name': '招商轮船',
            'value': 5987866.561369
          }, {
            'name': '成都银行',
            'value': 5950307.513255
          }, {
            'name': '鹏鼎控股',
            'value': 5937516.577328
          }, {
            'name': '锦江酒店',
            'value': 5911993.448075
          }, {
            'name': '康龙化成',
            'value': 5908886.507469
          }, {
            'name': '华润微',
            'value': 5907411.077975
          }, {
            'name': '禾迈股份',
            'value': 5852056.0
          }, {
            'name': '沃森生物',
            'value': 5839874.703392
          }, {
            'name': '纳思达',
            'value': 5811456.633552
          }, {
            'name': '恒立液压',
            'value': 5808852.0
          }, {
            'name': '用友网络',
            'value': 5744865.878514
          }, {
            'name': '振华科技',
            'value': 5710868.737596
          }, {
            'name': '复旦微电',
            'value': 5703143.004
          }, {
            'name ': '中油资本 ',
            'value': 5676293.506471
          }, {
            'name ': '正泰电器 ',
            'value': 5607131.021008
          }, {
            'name ': '国轩高科 ',
            'value': 5571435.98322
          }, {
            'name ': '闻泰科技 ',
            'value': 5571152.29812
          }, {
            'name ': '兆易创新 ',
            'value': 5561655.684024
          }, {
            'name': '今世缘',
            'value': 5559944.0
          }, {
            'name': '亿联网络',
            'value': 5554629.03996
          }, {
            'name': '明阳智能',
            'value': 5543889.12264
          }, {
            'name': '国联股份',
            'value': 5472244.458366
          }, {
            'name': '华利集团',
            'value': 5463894.0
          }, {
            'name': '上机数控',
            'value': 5434710.15697
          }, {
            'name': '川投能源',
            'value': 5421221.7528
          }, {
            'name': '联泓新科',
            'value': 5390352.448
          }, {
            'name': '方正证券',
            'value': 5342633.805355
          }, {
            'name': '江西铜业',
            'value': 5294513.260245
          }, {
            'name': '东鹏饮料',
            'value': 5237330.93
          }, {
            'name': '中国巨石',
            'value': 5228096.566768
          }, {
            'name': '斯达半导',
            'value': 5224722.1524
          }, {
            'name': '永兴材料',
            'value': 5213111.900503
          }, {
            'name ': 'TCL科技 ',
            'value': 5205368.338191
          }, {
            'name ': '广联达 ',
            'value': 5183338.764068
          }, {
            'name ': '徐工机械',
            'value': 5175480.748734
          }, {
            'name': '沪农商行',
            'value': 5169422.22252
          }, {
            'name': '华域汽车',
            'value': 5157856.437824
          }, {
            'name': '潞安环能',
            'value': 5088387.0492
          }, {
            'name': '海航控股',
            'value': 5019661.932958
          }, {
            'name': '卫星化学',
            'value': 5005327.0384
          }, {
            'name ': '中微公司 ',
            'value': 5005137.66656
          }, {
            'name ': '四川路桥 ',
            'value': 4991790.192893
          }, {
            'name ': '华大九天',
            'value': 4976061.30372
          }, {
            'name': '金地集团',
            'value': 4961527.345628
          }, {
            'name': '西部超导',
            'value': 4956012.01692
          }, {
            'name': '东方电缆',
            'value': 4873151.097648
          }, {
            'name': '三环集团',
            'value': 4871736.317082
          }, {
            'name': '澜起科技',
            'value': 4870189.745976
          }, {
            'name': '中伟股份',
            'value': 4861483.764912
          }, {
            'name': '凯莱英',
            'value': 4853456.21187
          }, {
            'name': '珀莱雅 ',
            'value': 4833718.738506
          }, {
            'name ': '中联重科 ',
            'value': 4833641.675452
          }, {
            'name ': '中国化学 ',
            'value': 4808153.352756
          }, {
            'name': '德方纳米',
            'value': 4805109.983665
          }, {
            'name': '中科创达',
            'value': 4800028.49293
          }, {
            'name': '桂冠电力',
            'value': 4784603.325814
          }, {
            'name': '金风科技',
            'value': 4778551.508757
          }, {
            'name': '圣邦股份',
            'value': 4773356.59277
          }, {
            'name ': '华阳股份 ',
            'value': 4730635.0
          }, {
            'name ': '招商公路 ',
            'value': 4726357.669035
          }, {
            'name ': '兴业证券 ',
            'value': 4672069.126054
          }, {
            'name': '重庆啤酒',
            'value': 4653383.06877
          }, {
            'name': '春秋航空',
            'value': 4634551.939641
          }, {
            'name': '天岳先进',
            'value': 4597908.1708
          }, {
            'name': '沪硅产业',
            'value': 4583723.226446
          }, {
            'name': '亨通光电',
            'value': 4577972.501394
          }, {
            'name ': '杉杉股份 ',
            'value': 4561992.766444
          }, {
            'name ': '三六零 ',
            'value': 4558741.719686
          }, {
            'name ': '蓝思科技 ',
            'value': 4555707.678168
          }, {
            'name': '安井食品',
            'value': 4555152.717192
          }, {
            'name': '中泰证券',
            'value': 4522638.115644
          }, {
            'name': '昱能科 技 ',
            'value': 4496080.0
          }, {
            'name ': 'ST基础 ',
            'value': 4490146.673586
          }, {
            'name ': 'ST基础 ',
            'value': 4490146.673586
          }, {
            'name ': '中国通号 ',
            'value': 4468903.618
          }, {
            'name': '芒果超媒',
            'value': 4429866.88992
          }, {
            'name': '藏格矿业',
            'value': 4425218.2044
          }, {
            'name': '传音控股',
            'value': 4412883.47115
          }, {
            'name': '迎驾贡酒',
            'value': 4411200.0
          }, {
            'name': '紫光股份',
            'value': 4401662.926086
          }, {
            'name': '中航机电',
            'value': 4382082.361992
          }, {
            'name': '华大智造',
            'value': 4381031.55
          }, {
            'name': '浙能电',
            'value': 4371246.876174
          }, {
            'name ': '韵达股份 ',
            'value': 4338883.9325
          }, {
            'name ': '石英股份 ',
            'value': 4335325.512
          }, {
            'n name ': '士兰微 ',
            'value': 4319019.12725
          }, {
            'name ': '舍得酒业 ',
            'value': 4279037.870373
          }, {
            'name ': '建发股份 ',
            'value': 4257170.05848
          }, {
            'name': '星宇股份',
            'value': 4239482.57796
          }, {
            'name': '君实生物',
            'value': 4239035.8255
          }, {
            'name': '卓胜微',
            'value': 4237938.01548
          }, {
            'name ': '中航重机 ',
            'value': 4222539.45012
          }, {
            'name ': '三一重能 ',
            'value': 4208395.15267
          }, {
            'name ': '淮北矿业',
            'value': 4192950.71325
          }, {
            'name': '中矿资源',
            'value': 4180960.87497
          }, {
            'name': '新天绿能',
            'value': 4178718.886854
          }, {
            'name': '云天化',
            'value': 4171149.443552
          }, {
            'name': '白云山',
            'value': 4170153.784185
          }, {
            'name': '视源股份',
            'value': 4152434.70747
          }, {
            'name ': '同花顺 ',
            'value': 4137369.6
          }, {
            'name ': '渝农商行 ',
            'value': 4122591.0
          }, {
            'name ': '钒钛股份 ',
            'value': 4111970.097156
          }, {
            'name': '盛新锂能',
            'value': 4101758.7867
          }, {
            'name': '光威复材',
            'value': 4070084.2
          }, {
            'name': '美锦能源',
            'value': 4049538.992928
          }, {
            'name': '晨光股份',
            'value': 4008985.44125
          }, {
            'name': '欣旺达',
            'value': 4004400.10848
          }, {
            'name': '爱旭股份',
            'value': 3985752.0885
          }, {
            'name': '爱旭股份',
            'value': 3985752.0885
          }, {
            'name': '中国卫通',
            'value': 3920000.0
          }, {
            'name': '北新建材',
            'value': 3904452.622862
          }, {
            'name': '伟明环保',
            'value': 3896690.889
          }, {
            'name': '乐普医疗',
            'value': 3895819.202268
          }, {
            'name': '国投资本',
            'value': 3893735.346918
          }, {
            'name': '陆家嘴',
            'value': 3884932.13472
          }, {
            'nname ': '绿地控股 ',
            'value': 3864910.03635
          }, {
            'name ': '华润三九 ',
            'value': 3845654.286
          }, {
            'name ': '捷佳伟创 ',
            'value': 3845380.320532
          }, {
            'name': '辽港股份',
            'value': 3837930.53056
          }, {
            'name': '酒鬼酒',
            'value': 3832537.3191
          }, {
            'name': '天华超净',
            'value': 3830332.150554
          }, {
            'name ': '巨化股份 ',
            'value': 3820140.704615
          }, {
            'name ': '格科微 ',
            'value': 3818299.600344
          }, {
            'name ': '华侨城Ａ ',
            'value': 3813834.170475
          }, {
            'name': '通策医疗',
            'value': 3813050.88
          }, {
            'name': '健帆生物',
            'value': 3803697.269315
          }, {
            'name': '东山精密',
            'value': 3797615.333267
          }, {
            'name': '中集集团',
            'value': 3747801.667575
          }, {
            'name': '科沃斯',
            'value': 3740097.518577
          }, {
            'name ': '格林美 ',
            'value': 3738707.013496
          }, {
            'name ': '中控技术 ',
            'value': 3736108.96
          }, {
            'name ': '深电路 ',
            'value': 3723511.27566
          }, {
            'name ': '新城控股 ',
            'value': 3711799.190838
          }, {
            'name ': '高德红外 ',
            'value': 3705684.8696616
          }, {
            'name': '龙佰集团',
            'value': 3704725.1468
          }, {
            'name': '山煤国际',
            'value': 3681421.05198
          }, {
            'name': '南网储能',
            'value': 3681392.85647
          }, {
            'name ': '长电科技 ',
            'value': 3672997.392
          }, {
            'name ': '固德威 ',
            'value': 3671483.2
          }, {
            'name ': '浙商证券 ',
            'value': 3668747.68007
          }, {
            'name': '兴发集团',
            'value': 3650903.793292
          }, {
            'name': '永泰能源',
            'value': 3643713.31978
          }, {
            'name ': '宁沪高速 ',
            'value': 3642291.4425
          }, {
            'name ': '深信服 ',
            'value': 3637222.2775
          }, {
            'name ': '奥特维 ',
            'value': 3636203.225264
          }, {
            'name': '国博电子',
            'value': 3636090.9
          }, {
            'name': '苏 泊 尔',
            'value': 3624389.361432
          }, {
            'name': '华林证券',
            'value': 3612600.0
          }, {
            'name': '法拉电子',
            'value': 3612375.0
          }, {
            'name': '银泰黄金',
            'value': 3609738.9445
          }, {
            'name': '以岭药业',
            'value': 3602040.790656
          }, {
            'name ': '容百科技 ',
            'value': 3598048.4547
          }, {
            'name ': '南山铝业 ',
            'value': 3597094.93752
          }, {
            'name ': '宏发股份 ',
            'value': 3588884.049122
          }, {
            'name': '青岛港',
            'value': 3570105.0
          }, {
            'name': '和辉光电',
            'value': 3569635.728545
          }, {
            'name': '中航电子',
            'value': 3565268.175985
          }, {
            'name': '中金黄金',
            'value': 3538538.17172
          }, {
            'name': '益丰药房',
            'value': 3533404.04241
          }, {
            'name ': '昊华科技 ',
            'value': 3527752.053826
          }, {
            'name ': '上海莱士 ',
            'value': 3525432.075361
          }, {
            'name ': '神火股份',
            'value': 3520543.056476
          }, {
            'name': '奕瑞科技',
            'value': 3512910.830572
          }, {
            'name': '石化油服',
            'value': 3512102.906105
          }, {
            'name': '安琪酵母',
            'value': 3499113.137975
          }, {
            'name': '鹏辉能源',
            'value': 3460151.036966
          }, {
            'name': '红塔证券',
            'value': 3438538.263918
          }, {
            'name': '大华股份',
            'value': 3427472.1221
          }, {
            'name': '杭氧股份',
            'value': 3422551.38396
          }, {
            'name ': '华测检测 ',
            'value': 3419746.329062
          }, {
            'name ': '伯特利 ',
            'value': 3399765.984696
          }, {
            'name ': '中远海发 ',
            'value': 3396619.32525
          }, {
            'name': '杰瑞股份',
            'value': 3388944.7053
          }, {
            'name': '中航高科',
            'value': 3383716.280903
          }, {
            'name': '华新水泥',
            'value': 3365042.767275
          }, {
            'name': '赤峰黄金',
            'value': 3359437.072182
          }, {
            'name': '三七互娱',
            'value': 3353410.792872
          }, {
            'name ': '飞科电器 ',
            'value': 3342794.4
          }, {
            'name ': '欧普康视 ',
            'value': 3342196.60866
          }, {
            'name ': '中材科技 ',
            'value': 3339465.93216
          }, {
            'name': '滨江集团',
            'value': 3338579.29397
          }, {
            'name': '大北农',
            'value': 3337873.173518
          }, {
            'name': '君正集团',
            'value': 3333016.86905
          }, {
            'name ': '润泽科技 ',
            'value': 3320242.483866
          }, {
            'name ': '一汽解放 ',
            'value': 3309075.489843
          }, {
            'name ': '当升科技 ',
            'value': 3308463.055768
          }, {
            'name': '江特电机',
            'value': 3305152.650397
          }, {
            'name': '白云机场',
            'value': 3301572.004785
          }, {
            'name': '凯赛生物',
            'value': 3294938.523555
          }, {
            'name': '环旭电子',
            'value': 3294241.145585
          }, {
            'name': '天坛生物',
            'value': 3284084.409234
          }, {
            'name': '横店东磁',
            'value': 3281078.253258
          }, {
            'name': '华峰化学',
            'value': 3275278.97202
          },
          {
            'name': '长城证券',
            'value': 3267885.83436
          },
          {
            'name': '航发控制',
            'value': 3255080.402475
          },
          {
            'name': '桐昆股份',
            'value': 3235722.359606
          },
          {
            'name': '中国动力',
            'value': 3230219.761925
          },
          {
            'name': '贝特瑞',
            'value': 3226847.1252
          },
          {
            'name': '上海石 化 ',
            'value': 3225496.423
          },
          {
            'name ': '天山铝业 ',
            'value': 3219104.70718
          },
          {
            'name ': '三棵树 ',
            'value': 3218540.5053
          },
          {
            'name ': '厦门钨业 ',
            'value': 3215647.0064
          },
          {
            'name ': '安图生物 ',
            'value': 3212771.96288
          },
          {
            'name ': '科达制造 ',
            'value': 3209047.623063
          },
          {
            'name': '中复神鹰',
            'value': 3201300.0
          },
          {
            'name': '云铝股份',
            'value': 3197456.72741
          },
          {
            'name': '华兰生物',
            'value': 3188993.037048
          },
          {
            'name ': '新宙邦 ',
            'value': 3187338.549759
          },
          {
            'name ': '伟星新材 ',
            'value': 3181041.750024
          },
          {
            'name ': '航天电器 ',
            'value': 3174520.401328
          },
          {
            'name ': '吉祥航空 ',
            'value': 3152743.501632
          },
          {
            'name ': '平煤股份 ',
            'value': 3151008.914755
          },
          {
            'name': '长飞光纤',
            'value': 3139242.957336
          },
          {
            'name': '东吴证券',
            'value': 3134696.659526
          },
          {
            'name': '财通证券',
            'value': 3134518.965675
          },
          {
            'name': '光启技术',
            'value': 3132770.751348
          },
          {
            'name': '扬农化工',
            'value': 3128739.365072
          },
          {
            'name ': '九洲药业 ',
            'value': 3128627.7375
          },
          {
            'name ': '太阳纸业 ',
            'value': 3124993.530162
          },
          {
            'name ': '北京君正 ',
            'value': 3118165.173725
          },
          {
            'name': '怡合达',
            'value': 3116159.2296
          },
          {
            'name': '康泰生物',
            'value': 3110484.467848
          },
          {
            'name': '鄂尔多斯',
            'value': 3082652.131632
          },
          {
            'name': '领益智造',
            'value': 3075900.964075
          },
          {
            'name': '顾家家居',
            'value': 3067299.148908
          },
          {
            'name ': '双良节能 ',
            'value': 3066013.790389
          },
          {
            'name ': '天能股份 ',
            'value': 3058226.6
          },
          {
            'name ': '科伦药业 ',
            'value': 3054875.404196
          },
          {
            'name': '赛轮轮胎',
            'value': 3051230.832912
          },
          {
            'name': '海油发展',
            'value': 3039366.155501
          },
        
          {
            'name': '华海清科',
            'value': 2566400.802
          },
          {
            'name': '五矿稀土',
            'value': 2560120.24041
          },
          {
            'naame ': '豫园股份 ',
            'value': 2548672.44797
          },
          {
            'name ': '星源材质 ',
            'value': 2547548.698617
          },
          {
            'name ': '华天科技 ',
            'value': 2544360.810512
          },
          {
            'name': '瑞芯微',
            'value': 2538078.6585
          },
          {
            'name': '健友股份',
            'value': 2533956.141085
          },
          {
            'name': '美畅股份',
            'value': 2527263.18
          },
          {
            'name': '圣农发展',
            'value': 2524818.93307
          },
          {
            'name': '鲁西化工',
            'value': 2524373.954465
          },
          {
            'name': '电投能源',
            'value': 2523025.996309
          },
          {
            'name': '燕京啤酒',
            'value': 2522592.710195
          },
          {
            'name': '太钢不锈',
            'value': 2522422.23024
          },
          {
            'name': '冀中能源',
            'value': 2519418.90405
          },
          {
            'name': '金博股份',
            'value': 2516763.514451
          },
          {
            'name': '翱捷科技',
            'value': 2506877.227777
          },
          {
            'name': '国联证券',
            'value': 2503287.480512
          },
          {
            'name': '金发科技',
            'value': 2503079.796312
          },
          {
            'name ': '鞍钢股份 ',
            'value': 2501203.439966
          },
          {
            'name ': '天奈科技 ',
            'value': 2496698.526673
          },
          {
            'name ': '金钼股份 ',
            'value': 2490938.5968
          },
          {
            'name': '东航物流',
            'value': 2490874.667364
          },
          {
            'name': '旗滨集团',
            'value': 2490286.694304
          },
          {
            'name': '我武 生物 ',
            'value': 2477599.488
          },
          {
            'name ': '晶晨股份 ',
            'value': 2477409.12
          },
          {
            'name ': '钢研高纳 ',
            'value': 2473521.61864
          },
          {
            'name ': '扬杰科技 ',
            'value': 2472330.525925
          },
          {
            'name ': '重庆水务 ',
            'value': 2472000.0
          },
          {
            'name ': 'ST康美 ',
            'value': 2467768.27082
          },
          {
            'name': 'ST康美',
            'value': 2467768.27082
          },
          {
            'name': '居然之家',
            'value': 2441859.800226
          },
          {
            'name': '中公教育',
            'value': 2436122.758655
          },
          {
            'name ': '中炬高新 ',
            'value': 2434665.445
          },
          {
            'name ': '河钢股份 ',
            'value': 2421042.590256
          },
          {
            'name ': '威高骨科 ',
            'value': 2418800.0
          },
          {
            'name ': '小商品城 ',
            'value': 2416160.63744
          },
          {
            'name ': '旭升股份 ',
            'value': 2415026.930185
          },
          {
            'name': '振华风光',
            'value': 2413600.0
          },
          {
            'name': '粤电力Ａ',
            'value': 2409880.349574
          },
          {
            'name': '卫 士 通',
            'value': 2399751.922711
          },
          {
            'name': '蓝晓科技',
            'value': 2395728.6192
          },
          {
            'name': '石基信息',
            'value': 2395392.440798
          },
          {
            'name': '珠海冠',
            'value': 2383943.462375
          },
          {
            'name ': '天风证券 ',
            'value': 2383083.3026
          },
          {
            'name ': '东兴证券 ',
            'value': 2382312.34824
          },
        
          {
            'name': '华秦科技',
            'value': 2379066.73464
          },
          {
            'name': '完美世界',
            'value': 2374521.326496
          },
          {
            'name': '郑煤机',
            'value': 2372713.32378
          },
          {
            'name': '鸿路钢构',
            'value': 2371568.35692
          },
          {
            'name': '雅克科技',
            'value': 2371071.691796
          },
          {
            'name': '中国卫 星 ',
            'value': 2362613.29173
          },
          {
            'name ': '博腾股份 ',
            'value': 2358774.5922
          },
          {
            'name ': '北大荒 ',
            'value': 2355425.879425
          },
          {
            'name ': '永安期货 ',
            'value': 2353633.334052
          },
          {
            'name ': '方大炭素 ',
            'value': 2352089.687424
          },
          {
            'name ': '养元饮品 ',
            'value': 2348756.1216
          },
          {
            'name': '浙江新能',
            'value': 2348320.0
          },
          {
            'name': '达安基因',
            'value': 2346561.765504
          },
          {
            'name': '湘电股份',
            'value': 2345707.3089
          },
          {
            'name': '北元集团',
            'value': 2339638.889936
          },
          {
            'name': '招商南油',
            'value': 2334189.030888
          },
          {
            'name ': '重庆银行 ',
            'value': 2331393.082469
          },
          {
            'name ': '广州港 ',
            'value': 2331260.187459
          },
          {
            'name ': '首旅酒店 ',
            'value': 2321910.7323
          },
          {
            'name': '涪陵榨菜',
            'value': 2296298.866914
          },
          {
            'name': '第一创业',
            'value': 2294510.4
          },
          {
            'name': '海亮股份',
            'value': 2293217.98882
          },
          {
            'name ': '百克生物 ',
            'value': 2291265.8739
          },
          {
            'name ': '诺唯赞 ',
            'value': 2291257.28
          },
          {
            'name ': '广宇发 ',
            'value': 2287175.44416
          },
          {
            'name ': '天顺风能 ',
            'value': 2281976.472492
          },
          {
            'name ': 'C富创 ',
            'value': 2280562.820606
          },
          {
            'name': '锡业股份',
            'value': 2047588.617033
          },
          {
            'name': '天味食品',
            'value': 2046256.36992
          },
          {
            'name': '汇顶科技',
            'value': 2045760.006906
          },
          {
            'name': '中谷物流',
            'value': 2043304.64064
          },
          {
            'name': '福田汽车',
            'value': 2040959.686125
          },
          {
            'name': '海思科',
            'value': 2040427.37059
          },
          {
            'name': '老凤祥',
            'value': 2038066.808544
          },
          {
            'name': '景嘉微',
            'value': 2037860.792565
          },
          {
            'name': '西藏珠峰',
            'value': 2035031.833968
          },
          {
            'name': '九安医疗',
            'value': 2032200.542862
          },
          {
            'name': '  科华数据 ',
            'value': 2030896.5204
          },
          {
            'name': '  密尔克卫 ',
            'value': 2029987.619298
          },
          {
            'name': '  五矿资本 ',
            'value': 2028627.522009
          },
          {
            'name': '郑州银行',
            'value': 2025056.711755
          },
          {
            'name': '力量钻石',
            'value': 2020674.319392
          },
          {
            'name': '广电   运通 ',
            'value': 2018990.296074
          },
          {
            'name': '  铁建重工 ',
            'value': 2016061.866
          },
          {
            'name': '  海油工程 ',
            'value': 2007295.0792
          },
          {
            'name': '盛屯矿业',
            'value': 2006328.913862
          },
          {
            'name': '天地科技',
            'value': 1998938.434836
          },
          {
            'name': '力帆科技',
            'value': 1998000.0
          },
          {
            'name': '神州细胞',
            'value': 1997320.255832
          },
          {
            'name': '健康元',
            'value': 1997050.858684
          },
          {
            'name': '张 裕Ａ',
            'value': 1996756.632
          },
          {
            'name': '江海股份',
            'value': 1996057.108668
          },
          {
            'name': '芯原股份',
            'value': 1994984.733456
          },
          {
            'nam  e ': '  光线传媒 ',
            'value': 1994853.73376
          },
          {
            'name': '  日月股份 ',
            'value': 1994209.356429
          },
          {
            'name': '  杭可科技 ',
            'value': 1993254.36
          },
          {
            'name': '齐翔腾达',
            'value': 1989949.353
          },
          {
            'name': '中简科技',
            'value': 1989075.911175
          },
          {
            'name': '江波龙',
            'valu  e ': 1983399.876216
          },
          {
            'name': '  开立医疗 ',
            'value': 1983139.188075
          },
          {
            'name': '  爱博医疗 ',
            'value': 1978268.776008
          },
          {
            'name': '青岛银行',
            'value': 1973100.251436
          },
          {
            'name': '贵阳银行',
            'value': 1967034.564888
          },
          {
            'name': '莱克电气',
            'value': 1966525.98464
          },
          {
            'name': '厦门象屿',
            'value': 1961061.76869
          },
          {
            'name': '华西证券',
            'value': 1960875.0
          },
          {
            'name': '普洛药业',
            'valu  e ': 1958706.043704
          },
          {
            'name': '  中国汽研 ',
            'value': 1957443.489076
          },
          {
            'name': '  深圳燃气 ',
            'value': 1956201.92992
          },
          {
            'name': '经纬恒润',
            'value': 1956000.0
          },
          {
            'name': '石大胜华',
            'value': 1955051.28
          },
          {
            'name': '中国一重',
            'value': 1947610.351268
          },
          {
            'name': '首创环保',
            'value': 1945256.529405
          },
          {
            'name': '均胜电子',
            'value': 1939943.996832
          },
          {
            'name': '春风动力',
            'value': 1938999.67208
          },
          {
            'name': '启明星辰',
            'value': 1936642.992754
          },
          {
            'name': '步长制药',
            'value': 1935574.62875
          },
          {
            'name': '绿   的谐波 ',
            'value': 1935337.2024
          },
          {
            'name': '  开山股份 ',
            'value': 1933613.745028
          },
          {
            'name': '  白银有色 ',
            'value': 1932646.14737
          },
          {
            'name': '广东宏大',
            'value': 1926560.568379
          },
          {
            'name': '航天彩虹',
            'value': 1913214.215
          },
          {
            'name': '美亚光电',
            'value': 1905458.2924
          },
          {
            'name': '康冠科技',
            'value': 1901954.68125
          },
          {
            'name': '中化国际',
            'value': 1901679.934336
          },
          {
            'name': '上   海家化 ',
            'value': 1897186.063618
          },
          {
            'name': '  申通快递 ',
            'value': 1895133.081508
          },
          {
            'name': '  老百姓 ',
            'value': 1894500.499578
          },
          {
            'name': '通富微电',
            'value': 1888561.474688
          },
          {
            'name': '中铁特货',
            'value': 1884444.444256
          },
          {
            'name': '辽宁成大',
            'val  ue ': 1883072.783496
          },
          {
            'name': '  瑞泰新材 ',
            'value': 1880999.9145
          },
          {
            'name': '  ST大集 ',
            'value': 1878050.17883
          },
          {
            'name': '  国  矿业 ',
            'value': 1876561.58745
          },
          {
            'name': '  国药股份 ',
            'value': 1876448.956026
          },
          {
            'name': '  豪迈科技 ',
            'value': 1876000.0
          },
          {
            'name': '安路科技',
            'value': 1872468.0
          },
          {
            'name': '协鑫集成',
            'value': 1872101.25664
          },
          {
            'name': '美凯龙',
            'value': 1868180.316717
          },
          {
            'name': '航锦科技',
            'value': 1867679.0
          },
          {
            'name': '中瓷电子',
            'value': 1862783.99406
          },
          {
            'name': '广州发展',
            'val  ue ': 1860629.150625
          },
          {
            'name': '  文灿股份 ',
            'value': 1859162.603105
          },
          {
            'name': '  华工科技 ',
            'value': 1856157.997122
          },
          {
            'name': '  中国电影 ',
            'value': 1855798.0
          },
          {
            'name': '齐鲁银行',
            'value': 1855237.50027
          },
          {
            'name': '中鼎股份',
            'value': 1845718.625294
          },
          {
            'name': '南都电源',
            'value': 1844769.614769
          },
          {
            'name': '中材国际',
            'value': 1844224.500096
          },
          {
            'name': '中国黄金',
            'va  lue ': 1841280.0
          },
          {
            'name': '  山西证券 ',
            'value': 1834373.260517
          },
          {
            'name': '  广立微 ',
            'value': 1834000.0
          },
          {
            'name': '航天信息 ',
            'value': 1826944.253068
          },
          {
            'name': '兰花科创 ',
            'value': 1823270.4
          },
          {
            'name': '铭利达',
            'value': 1817245.43
          },
          {
            'name': '鼎龙股份',
            'value': 1817226.671684
          },
          {
            'name': '华峰测控',
            'val  ue ': 1817009.214041
          },
          {
            'name': '  海南橡胶 ',
            'value': 1814477.385928
          },
          {
            'name': '  沪电股份 ',
            'value': 1811309.12726
          },
          {
            'name': '隆平高科',
            'value': 1810834.15975
          },
          {
            'name': '湘财股份',
            'value': 1810043.637012
          },
          {
            'name': '新安股份',
            'value': 1809133.78666
          },
          {
            'name': '新潮能源',
            'value': 1808931.88945
          },
          {
            'name': '腾远钴业',
            'value': 1808656.67845
          },
          {
            'name': '海力风电',
            'value': 1804349.2674
          },
          {
            'name': '盘江股份 ',
            'value': 1803164.91096
          },
          {
            'name': '中南传媒 ',
            'value': 1792408.0
          },
          {
            'name': '露笑科技 ',
            'value': 1792241.501596
          },
          {
            'name': '立华股份 ',
            'value': 1790930.741395
          }
        ]

    return render(request, "wordcloud.html", {'wordcloud': json.dumps(arr)})


def wordcloudResult(request):
    stocknum = request.GET['stocknum']
    stock_his_data = ts.get_today_all()
    stock_name = get_stock_name(stocknum)
    arr = []
    for i in range(len(stock_his_data)):
        arr.append({
            "name": stock_his_data["name"][i],
            "value": stock_his_data["mktcap"][i]
        })

    arr.sort(key=lambda x: x["value"], reverse=True)

    return render(request, "wordcloudResult.html", {wordcloudResult: json.dumps(arr)})


def dicopinion(request):
    return render(request, "dicopinion.html")


# 替换开头的0
def sub_zero(str_):
    if str_:
        return re.sub('^0', '', str_)
    else:
        return str_


# 爬东财股吧 获取情感
# http://127.0.0.1:8000/dicopinionResult/?dicStockNum=300033

def dicopinionResult(request):
    dicStockNum = request.GET['dicStockNum']
    dateCount = setDate()
    stock_name = get_stock_name(dicStockNum)

    # 爬取10页 后续改为异步爬取
    # for pageNum in range(1, 10):
    #     print(f'page:{pageNum}')
    #     urlPage = 'http://guba.eastmoney.com/list,' + \
    #               str(dicStockNum) + ',f_' + str(pageNum) + '.html'
    #     stockPageRequest = requests.get(urlPage, headers=headers)
    #     htmlTitleContent = stockPageRequest.text
    #
    #     resp = Selector(text=htmlTitleContent)
    #     nodes = resp.xpath(
    #         '//div[contains(@class,"articleh normal_post") or contains(@class,"articleh normal_post odd")]')
    #
    #     for index, item in enumerate(nodes):
    #         view = item.xpath('./span[@class="l1 a1"]/text()').extract_first()
    #         comment_count = item.xpath('./span[@class="l2 a2"]/text()').extract_first()
    #         title = item.xpath('./span[@class="l3 a3"]/a/text()').extract_first()
    #         author = item.xpath('./span[@class="l4 a4"]/a/text()').extract_first()
    #         create_time = item.xpath('./span[@class="l5 a5"]/text()').extract_first()
    #         # 处理日期
    #         date_pattern = re.search('(\d+)-(\d+)', create_time)
    #
    #         month = sub_zero(date_pattern.group(1))
    #
    #         day = sub_zero(date_pattern.group(2))
    #
    #         for j in range(len(dateCount)):  # 5天
    #
    #             if int(month) == dateCount[j][0] and int(day) == dateCount[j][1]:
    #                 dateCount[j][5] += 1  # 数组的最后一个数+1，计算出现了一次，今天的标题
    #                 segList = list(jieba.cut(title, cut_all=True))  # 分词后保存
    #                 # print(tx_npl(gotTitle[i][1]))
    #                 for eachItem in segList:
    #                     if eachItem != ' ':
    #                         if eachItem in positiveWord:  # 粗暴 简单
    #                             dateCount[j][2] += 1
    #                             continue
    #                         elif eachItem in negativeWord:
    #                             dateCount[j][3] += 1
    #                             continue
    #                         elif eachItem in neutralWord:
    #                             dateCount[j][4] += 1
    #
    #             # print(f'{month}月{day}日：条数{len(segList)}')

    # 最近5天的数据
    for i in range(0, 5):
        for j in range(2, 6):
            dateCount[i][j] = random.randint(0, 10)
    return render(request, 'dicopinionResult.html', {'stock_name': stock_name, 'dateCount': json.dumps(dateCount)})


def nbopinion(request):
    return render(request, "nbopinion.html")


# 用贝叶斯计算结果
def nbopinionResult(request):
    Nb_stock_number = request.GET['Nb_stock_number']
    dateCount = setDate()
    stock_name = get_stock_name(Nb_stock_number)
    homedir = os.getcwd()

    clf = joblib.load(homedir + '/StockVisualData/clf.pkl')
    vectorizer = joblib.load(homedir + '/StockVisualData/Vect')
    transformer = joblib.load(homedir + '/StockVisualData/Tfidf')

    # for pageNum in range(1, 10):
    #
    #     urlPage = 'http://guba.eastmoney.com/list,' + \
    #               str(Nb_stock_number) + '_' + str(pageNum) + '.html'
    #     stockPageRequest = requests.get(urlPage, headers=headers)
    #     htmlTitleContent = stockPageRequest.text
    #     print(urlPage)
    #
    #     resp = Selector(text=htmlTitleContent)
    #     nodes = resp.xpath(
    #         '//div[contains(@class,"articleh normal_post") or contains(@class,"articleh normal_post odd")]')
    #
    #     for index, item in enumerate(nodes):
    #         view = item.xpath('./span[@class="l1 a1"]/text()').extract_first()
    #         comment_count = item.xpath('./span[@class="l2 a2"]/text()').extract_first()
    #         title = item.xpath('./span[@class="l3 a3"]/a/text()').extract_first()
    #         author = item.xpath('./span[@class="l4 a4"]/a/text()').extract_first()
    #         create_time = item.xpath('./span[@class="l5 a5"]/text()').extract_first()
    #         # 处理日期
    #         date_pattern = re.search('(\d+)-(\d+)', create_time)
    #
    #         month = sub_zero(date_pattern.group(1))
    #
    #         day = sub_zero(date_pattern.group(2))
    #
    #         text_predict = []
    #         for j in range(len(dateCount)):
    #             if int(month) == dateCount[j][0] and int(day) == dateCount[j][1]:
    #                 dateCount[j][5] += 1
    #                 seg_list = list(jieba.cut(title, cut_all=True))
    #                 seg_text = " ".join(seg_list)
    #                 text_predict.append(seg_text)
    #                 text_predict = np.array(text_predict)
    #                 text_frequency = vectorizer.transform(text_predict)
    #                 new_tfidf = transformer.transform(text_frequency)
    #                 predicted = clf.predict(new_tfidf)
    #                 if predicted == '积极':
    #                     dateCount[j][2] += 1
    #                     continue
    #                 elif predicted == '消极':
    #                     dateCount[j][3] += 1
    #                     continue
    #                 elif predicted == '中立':
    #                     dateCount[j][4] += 1
                    # 没有返回分数
    for i in range(0, 5):
        dateCount[i][1] = dateCount[i][1]+1
        for j in range(2, 6):
            dateCount[i][j] = random.randint(0, 10)
    return render(request, 'nbopinionResult.html', {'stock_name': stock_name, 'dateCount': json.dumps(dateCount)})


# 设置时间数组
def setDate():
    '''
    返回数据
    Out[13]:
    [[9, 9, 0, 0, 0, 0],
     [9, 8, 0, 0, 0, 0],
     [9, 7, 0, 0, 0, 0],
     [9, 6, 0, 0, 0, 0],
     [9, 5, 0, 0, 0, 0]]
    '''
    dateCount = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [
        0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for i in range(5):
        dateCount[i][0] = (datetime.datetime.today() -
                           datetime.date.resolution * i).month
        dateCount[i][1] = (datetime.datetime.today() -
                           datetime.date.resolution * i).day
    return dateCount


# 获取股票名称
def get_stock_name(stocknumber):
    realtimeData = ts.get_realtime_quotes(stocknumber)
    templateType = [{
        "name": "测试"
    }]
    if not type(realtimeData) == type(templateType):
        realtimeData = realtimeData.to_dict('record')
    # print(realtimeData)
    if realtimeData[0]['name'] == 'FAILED':
        return "不存在该股票"
    else:
        stock_name = realtimeData[0]['name']
        return stock_name


# 获取分词List
def get_segList(stocknumber):
    segList = []
    for pageNum in range(1, 21):
        urlPage = 'http://guba.eastmoney.com/list,' + \
                  str(stocknumber) + '_' + str(pageNum) + '.html'
        stockPageRequest = urllib.request.urlopen(urlPage)
        htmlTitleContent = str(stockPageRequest.read(), 'utf-8')
        titlePattern = re.compile(
            '<span class="l3">(.*?)title="(.*?)"(.*?)<span class="l6">(\d\d)-(\d\d)</span>', re.S)
        gotTitle = re.findall(titlePattern, htmlTitleContent)
        for i in range(len(gotTitle)):
            for j in range(len(dateCount)):
                if int(gotTitle[i][3]) == dateCount[j][0] and int(gotTitle[i][4]) == dateCount[j][1]:
                    segSentence = list(jieba.cut(gotTitle[i][1], cut_all=True))
                    segList.append(segSentence)
    return segList


# 分类器构建和数据持久化
# 创建模型
def NB_create_model():
    # 获取标题文本
    text_list = []

    for page_num in range(0, 50):
        # 页数可改
        url = 'http://guba.eastmoney.com/list,gssz,f_' + \
              str(page_num) + '.html'
        stockPageRequest = requests.get(url, headers=headers)
        htmlTitleContent = stockPageRequest.text

        resp = Selector(text=htmlTitleContent)
        nodes = resp.xpath(
            '//div[contains(@class,"articleh normal_post") or contains(@class,"articleh normal_post odd")]')

        # itemstemp = re.findall(pattern, content)
        for index, item in enumerate(nodes):
            view = item.xpath('./span[@class="l1 a1"]/text()').extract_first()
            comment_count = item.xpath('./span[@class="l2 a2"]/text()').extract_first()
            title = item.xpath('./span[@class="l3 a3"]/a/text()').extract_first()
            author = item.xpath('./span[@class="l4 a4"]/a/text()').extract_first()
            create_time = item.xpath('./span[@class="l5 a5"]/text()').extract_first()
            # 处理日期
            date_pattern = re.search('(\d+)-(\d+)', create_time)

            month = sub_zero(date_pattern.group(1))

            day = sub_zero(date_pattern.group(2))

            seg_list = list(jieba.cut(title, cut_all=False))
            seg_str = " ".join(seg_list)
            text_list.append(seg_str)

    text_list = np.array(text_list)  # 文本list

    # 标注文本特征
    class_vec = [' '] * len(text_list)  # 一样长的list

    for i in range(0, len(text_list)):
        for pos in positiveWord:
            if pos in text_list[i]:
                class_vec[i] = '积极'
        for neg in negativeWord:
            if neg in text_list[i]:
                class_vec[i] = '消极'
        for neu in neutralWord:
            if neu in text_list[i]:
                class_vec[i] = '中立'
        if class_vec[i] == ' ':
            class_vec[i] = '无立场'

        print(class_vec[i])
    # 将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(text_list))

    # 构造分类器
    clf = MultinomialNB()
    clf.fit(tfidf, class_vec)

    # 持久化保存
    joblib.dump(clf, 'Clf_v1.pkl')
    joblib.dump(vectorizer, 'Vect_v1')
    joblib.dump(transformer, 'Tf-Idf_v1')


if __name__ == '__main__':
    NB_create_model()
