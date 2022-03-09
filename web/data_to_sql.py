import pymysql as pysql
import json
insert=r'''
INSERT INTO novel (name, ccount, pcount, ncount, rate, keyword) VALUES ("%s","%s","%s","%s","%s",'%s');
'''

if __name__=="__main__":
    connection = pysql.connect(host='104.43.19.221',port=3306,  user='root',password='root',db='aiotfinal',charset='utf8')
    cursor = connection.cursor()

    bnl=[]
    bhd={}
    with open('./novel_list.txt','r',encoding='utf-8') as nl:
        for n in nl.readlines():
            bnl.append(n.replace('\n','').split(',')[-1])
            bhd[n.replace('\n','').split(',')[-1]]=n.replace('\n','').split(',')[0]
    
    for bn in bnl:
        with open('./fin_predic_data/%s.json'%bn,'r') as file:
            json_data=json.loads(file.read())[bn]
            kw=' '
            if json_data['rate'] =='NaN':
                json_data['rate']=0
            for s in json_data['key_word']:
                if s =="None":
                    break
                else:
                    kw+=s+'  '
            cursor.execute(insert%(bn,json_data['ccount'],json_data['pcount'],json_data['ncount'],json_data['rate'],kw))
            # print(insert%(bn,json_data['ccount'],json_data['pcount'],json_data['ncount'],json_data['rate'],kw))
            # break
    connection.commit()
    cursor.close()
    connection.close()