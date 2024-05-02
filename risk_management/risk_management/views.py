import json
from django.http import JsonResponse
import yfinance as yf
import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def risk(request):
    if request.method =="POST":
        data = json.loads(request.body)
        tickers = data["stock"]
        # print(tickers)
        def startDate(year,month,date):
            if(month==1):
                month = 12
                year = year-1
            elif (month>=2 and month<=12):
                month = month-1
            return datetime.date(year, month, date)
        s_year,s_month,s_date = map(int,data["start_date"].split("-"))
        e_year,e_month,e_date = map(int,data["end_date"].split("-"))
        start_date = datetime.date(s_year,s_month,s_date)
        eff_start_date = startDate(start_date.year,start_date.month,start_date.day)
        # print("Date",eff_start_date)
        end_date = datetime.date(e_year,e_month,e_date)
        # print("End date",end_date)
        mothly_data = yf.download(tickers, start=eff_start_date, end=end_date, interval='1mo')  
        # print(mothly_data)
        mr_l = []
        n =len(mothly_data)
        # print("Value of n is : ",n)
        for i in range(1,n):
            temp = ( ((mothly_data["Adj Close"][i]) - (mothly_data["Adj Close"][i-1]))/(mothly_data["Adj Close"][i-1]) )*100
            mr_l.append(temp)
        cummulative_returns = {
            "1M":"null",
            "3M":"null",
            "6M":"null",
            "1Y":"null",
            "2Y":"null",
            "3Y":"null",
            "5Y":"null"
        }


        def rebase_100(company):
            msft_100 = [100]
            for i in range(1,len(company)):
                msft_100.append((company[i]/company[0])*100)
            return msft_100
        
        monthly_return = mothly_data['Adj Close']
        rebase_100_list = rebase_100(monthly_return)
        # print(rebase_100_li
        # \st)

        new_n = len(mr_l)
        cum = [0]*new_n
        cumm_returns = 1
        for month in range(new_n-1,-1,-1):
            cumm_returns *=  (1+mr_l[month]/100)
            cum[month]= (cumm_returns-1)*100


        if(new_n-1>=0):
            cummulative_returns["1M"] = (cum[new_n-1])

        if(new_n-3>=0):
            cummulative_returns["3M"] = (cum[new_n-3])

        if(new_n-6>=0):
            cummulative_returns["6M"] = (cum[new_n-6])
            
        if(new_n-12>=0):
            cummulative_returns["1Y"] = (cum[new_n-12])

        if(new_n-24>=0):
            cummulative_returns["2Y"] = (cum[new_n-24])
            
        if(new_n-36>=0):
            cummulative_returns["3Y"] = (cum[new_n-36])

        if(new_n-60>=0):
            cummulative_returns["5Y"] = (cum[new_n-60])
        
        annualized_returns = {
            "1M":"null",
            "3M":"null",
            "6M":"null",
            "1Y":"null",
            "2Y":"null",
            "3Y":"null",
            "5Y":"null"
        }

        new_n = len(mr_l)
        ann = [0]*new_n
        ann_returns = 1

        for i in range(new_n-1,-1,-1):
            ann_returns *=  (1+mr_l[i]/100)
            #print(new_n-i)
            ann [i]= ( ( (ann_returns)**(12/(new_n-i)))  -1)*100
        for i in range(new_n-1,new_n-1-12,-1):
            ann[i]=cum[i]
        if(new_n-1>=0):
            annualized_returns["1M"] = (cum[new_n-1])

        if(new_n-3>=0):
            annualized_returns["3M"] = (cum[new_n-3])

        if(new_n-6>=0):
            annualized_returns["6M"] = (cum[new_n-6])
            
        if(new_n-12>=0):
            annualized_returns["1Y"] = (cum[new_n-12])

        if(new_n-24>=0):
            annualized_returns["2Y"] = (ann[new_n-24])
            
        if(new_n-36>=0):
            annualized_returns["3Y"] = (ann[new_n-36])

        if(new_n-60>=0):
            annualized_returns["5Y"] = (ann[new_n-60])
        ticker_symbo = 'NDX'
        dat = yf.download(ticker_symbo, start=eff_start_date, end=end_date)
        mothly_data_bench = yf.download("NDX", start=eff_start_date, end=end_date, interval='1mo') 
        mr_l_bench = []
        n =len(mothly_data_bench)
        for i in range(1,n):
            temp = ( ((mothly_data_bench["Adj Close"][i]) - (mothly_data_bench["Adj Close"][i-1]))/(mothly_data_bench["Adj Close"][i-1]) )*100
            mr_l_bench.append(temp)
        cummulative_returns_bench = {
            "1M":"null",
            "3M":"null",
            "6M":"null",
            "1Y":"null",
            "2Y":"null",
            "3Y":"null",
            "5Y":"null"
        }

        new_n_bench = len(mr_l_bench)
        cum_bench = [0]*new_n_bench
        cumm_returns_bench = 1
        for month in range(new_n_bench-1,-1,-1):
            cumm_returns_bench *=  (1+mr_l_bench[month]/100)
            cum_bench[month]= (cumm_returns_bench-1)*100
        print(cum_bench)

        if(new_n_bench-1>=0):
            cummulative_returns_bench["1M"] = (cum_bench[new_n_bench-1])

        if(new_n_bench-3>=0):
            cummulative_returns_bench["3M"] = (cum_bench[new_n_bench-3])

        if(new_n_bench-6>=0):
            cummulative_returns_bench["6M"] = (cum_bench[new_n_bench-6])
            
        if(new_n_bench-12>=0):
            cummulative_returns_bench["1Y"] = (cum_bench[new_n_bench-12])

        if(new_n_bench-24>=0):
            cummulative_returns_bench["2Y"] = (cum_bench[new_n_bench-24])
            
        if(new_n_bench-36>=0):
            cummulative_returns_bench["3Y"] = (cum_bench[new_n_bench-36])

        if(new_n_bench-60>=0):
            cummulative_returns_bench["5Y"] = (cum_bench[new_n_bench-60])
        # print(cummulative_returns_bench)
        annualized_returns_bench = {
            "1M":"null",
            "3M":"null",
            "6M":"null",
            "1Y":"null",
            "2Y":"null",
            "3Y":"null",
            "5Y":"null"
        }

        new_n_bench = len(mr_l_bench)
        ann_bench = [0]*new_n_bench
        ann_returns_bench = 1

        for i in range(new_n_bench-1,-1,-1):
            ann_returns_bench *=  (1+mr_l_bench[i]/100)
            #print(new_n-i)
            ann_bench [i]= ( ( (ann_returns_bench)**(12/(new_n_bench-i)))  -1)*100
        for i in range(new_n_bench-1,new_n_bench-1-12,-1):
            ann_bench[i]=cum_bench[i]
        print(ann_bench)

        if(new_n_bench-1>=0):
            annualized_returns_bench["1M"] = (ann_bench[new_n_bench-1])

        if(new_n_bench-3>=0):
            annualized_returns_bench["3M"] = (ann_bench[new_n_bench-3])

        if(new_n_bench-6>=0):
            annualized_returns_bench["6M"] = (ann_bench[new_n_bench-6])
            
        if(new_n_bench-12>=0):
            annualized_returns_bench["1Y"] = (ann_bench[new_n_bench-12])

        if(new_n_bench-24>=0):
            annualized_returns_bench["2Y"] = (ann_bench[new_n_bench-24])
            
        if(new_n_bench-36>=0):
            annualized_returns_bench["3Y"] = (ann_bench[new_n_bench-36])

        if(new_n_bench-60>=0):
            annualized_returns_bench["5Y"] = (ann_bench[new_n_bench-60])
        
        active_cum_returns_bench = {
            "1M":"null",
            "3M":"null",
            "6M":"null",
            "1Y":"null",
            "2Y":"null",
            "3Y":"null",
            "5Y":"null"
        }
        if(new_n>new_n_bench):
            nn=new_n_bench
        else:
            nn=new_n

        active_return_cum=[0]*nn
        cum1=cum[::-1]
        cum1_bench=cum_bench[::-1]
        print(cum1)
        print(cum1_bench)
        for i in range(0,nn):
            active_return_cum[i]=cum1[i]-cum1_bench[i]

        print(active_return_cum)
        if(0<nn):
            active_cum_returns_bench["1M"] = (active_return_cum[0])

        if(2<nn):
            active_cum_returns_bench["3M"] = (active_return_cum[2])

        if(5<nn):
            active_cum_returns_bench["6M"] = (active_return_cum[5])
            
        if(11<nn):
            active_cum_returns_bench["1Y"] = (active_return_cum[11])

        if(23<nn):
            active_cum_returns_bench["2Y"] = (active_return_cum[23])
            
        if(35<nn):
            active_cum_returns_bench["3Y"] = (active_return_cum[35])

        if(59<nn):
            active_cum_returns_bench["5Y"] = (active_return_cum[59])
        

        active_ann_returns_bench = {
            "1M":"null",
            "3M":"null",
            "6M":"null",
            "1Y":"null",
            "2Y":"null",
            "3Y":"null",
            "5Y":"null"
        }
        if(new_n>new_n_bench):
            nn=new_n_bench
        else:
            nn=new_n

        active_return_ann=[0]*nn
        ann1=ann[::-1]
        ann1_bench=ann_bench[::-1]
        print(ann1)
        print(ann1_bench)
        for i in range(0,nn):
            active_return_ann[i]=ann1[i]-ann1_bench[i]

        print(active_return_ann)
        if(0<nn):
            active_ann_returns_bench["1M"] = (active_return_ann[0])

        if(2<nn):
            active_ann_returns_bench["3M"] = (active_return_ann[2])

        if(5<nn):
            active_ann_returns_bench["6M"] = (active_return_ann[5])
            
        if(11<nn):
            active_ann_returns_bench["1Y"] = (active_return_ann[11])

        if(23<nn):
            active_ann_returns_bench["2Y"] = (active_return_ann[23])
            
        if(35<nn):
            active_ann_returns_bench["3Y"] = (active_return_ann[35])

        if(59<nn):
            active_ann_returns_bench["5Y"] = (active_return_ann[59])
        
                    
        return JsonResponse({ "annualized_returns":annualized_returns,"cummulative_returns":cummulative_returns,"annualized_returns_bench":annualized_returns_bench,"cummulative_returns_bench":cummulative_returns_bench,"active_cum_returns_bench":active_cum_returns_bench,"active_ann_returns_bench":active_ann_returns_bench,"data1":json.dumps(rebase_100_list)},safe=False)
    else:
        return JsonResponse({"message":"Get is not allowed"},safe=False)