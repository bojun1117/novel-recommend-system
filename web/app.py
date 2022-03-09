from flask import Flask
from flask import render_template, jsonify,request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route("/getData", methods=['GET'])
def getData():
    myserver ="104.43.19.221"
    myuser="root"
    mypassword="root"
    mydb="aiotfinal"
    
    column=request.args.get('column')
    order=request.args.get('order')
    page=int(request.args.get('page'))
    
    from  pandas import DataFrame as df

    import pymysql.cursors
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    c = conn.cursor()
    
    c.execute("SELECT * FROM novel ORDER BY "+column+" "+order)
    results = c.fetchall()

    test_df = df(list(results),columns=['name','ccount','pcount','ncount','rate','keyword'])

    print(test_df.head(10))
    result = test_df.to_dict(orient='records')
    seq = [[item['name'], item['ccount'], item['pcount'], item['ncount'], item['rate'], item['keyword']] for item in result]
    
    start=(page-1)*10
    if(start>len(seq)):
        start=len(seq)-len(seq)%10
    
    infor=[int(math.ceil(len(seq)/10)),start/10+1,seq[start:start+10]]
    
    return jsonify(infor)
    c.close()
    conn.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088)