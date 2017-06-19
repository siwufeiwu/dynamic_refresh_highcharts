import pymysql as mysql
import json
from flask import Flask,request,render_template
app = Flask(__name__)

db = mysql.connect(host='10.165.124.46',
                   port=3306,
                   user='omptest',
                   passwd='omptest!@#$',
                   db='falcon',
                   charset='utf8')
db.autocommit(True)
c = db.cursor()

@app.route('/',methods=['GET','POST'])
def hello():
    sql = ''
    if request.method == 'POST':
        data = request.json
        try:
            sql = "insert into stat(host,mem_free,mem_usage,mem_total,load_avg,time) values ('%s',%d,%d,%d,'%s',%d)" % (data['Host'],data['MemFree'],data['MemUsage'],data['MemTotal'],data['LoadAvg'],int(data['Time']))
            ret = c.execute(sql)
        except mysql.IntegrityError:
            pass
        return 'OK'
    else:
        c.execute('select time,mem_usage from stat')
        ones = [[i[0]*1000,i[1]] for i in c.fetchall()]
        print ones
        return render_template('mon.html',data=json.dumps(ones))

@app.route('/new',methods=['GET'])
def getnew():
    c.execute('select time,mem_usage from stat order by id desc limit 1')
    v = c.fetchone()
    top = [v[0]*1000,v[1]]
    print top
    return json.dumps(top)

app.run(port=9999,debug=True)
