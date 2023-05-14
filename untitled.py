from flask import *
from DBConnection import *
app = Flask(__name__)
app.secret_key="abcd"
static_path="C:\\Users\\hp\\PycharmProjects\\untitled\\static"

@app.route('/')
def login():
    return render_template('index.html')



@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `login` WHERE `username`='"+username+"' AND `password`='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['loginid']
        if res['type']=="hr":
            return redirect('/hrhome')
        if res['type']=="manager":
            return redirect('/mngrhome')
        elif res['type']=="employee":
            return redirect('/emphome')
        else:
            return'''<script>alert('Invalid Username or Password');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid Username or Password');window.location='/'</script>'''

@app.route('/change_password',methods=['post'])
def change_password():
    current_password=request.form['currentpassword']
    new_password=request.form['newpassword']
    confirm_password=request.form['renewpassword']
    db=Db()
    qry="SELECT * FROM `login` WHERE `password`='"+current_password+"' AND `loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        if new_password==confirm_password:
            qry2="UPDATE `login` SET `password`='"+confirm_password+"' WHERE `loginid`='"+str(session['lid'])+"'"
            res2=db.update(qry2)
            return '''<script>alert('Password Change Successfull');window.location='/'</script>'''
        else:
            return '''<script>alert('Invalid Username or Password');window.location='/change_password'</script>'''
    else:
         return '''<script>alert('Invalid Username or Password');window.location='/change_password'</script>'''



@app.route('/empsignup')
def empsignup():
    return render_template('empsignup.html')

@app.route('/empsignup_post' ,methods=['post'])
def empsignup_post():
    name=request.form['name1']
    dept=request.form['dept']
    post=request.form['post']
    dob=request.form['dob']
    address=request.form['address']
    #FOTO------------------
    photo = request.files['foto']
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save(r"C:\\Users\\hp\\PycharmProjects\\untitled\\static\\employee\\" + date + ".jpg")
    path = "/static/employee/" + date + ".jpg"
    db=Db()
    username = request.form['username']
    confpass = request.form['conf']
    qry2 = "INSERT INTO `login` (`username`,`password`,`type`) VALUES ('" + username + "','" + confpass + "','employee')"
    res1 = db.insert(qry2)
    qry="INSERT INTO `employee` (`loginid`,`dept`,`name`,`post`,`address`,`dob`,`empstatus`,`photo`,`working`)VALUES('"+str(res1)+"','"+dept+"','"+name+"','"+post+"','"+address+"','"+dob+"','pending','"+str(path)+"','not working')"
    res=db.insert(qry)
    return '''<script>alert("signup successful please logic again");window.location='/'</script>'''



#hr===================================================================
@app.route('/hrhome')
def hrhome():
    return render_template('hr/hrhome.html')

@app.route('/viewsignup')
def viewsignup():
    db=Db()
    qry="SELECT * FROM `employee` WHERE `empstatus`='pending'"
    res=db.select(qry)
    return render_template('hr/viewsignup.html',data=res)
@app.route('/acceptsignup/<id>')
def acceptsignup(id):
    db=Db()
    qry="UPDATE `employee` SET `empstatus`='accepted' WHERE `empid`='"+id+"'"
    res=db.update(qry)
    return redirect('/viewsignup')

@app.route('/workingstatus/<id>')
def workingstatus(id):
    db=Db()
    qry = "UPDATE `employee` SET `working`='working' WHERE `empid`='" + id + "'"
    res=db.update(qry)
    return redirect('/manageemp')

@app.route('/rejectemp/<id>')
def rejectemp(id):
    db=Db()
    qry="UPDATE `employee` SET `empstatus`='rejected' WHERE  `empid`='"+id+"'"
    res=db.update(qry)
    return redirect('/viewsignup')

@app.route('/deleteappl/<id>')
def deleteappl(id):
    db=Db()
    qry="DELETE FROM `employee` WHERE `empid`='"+id+"'"
    res=db.delete(qry)
    return redirect('/applrejected')

@app.route('/applrejected')
def applrejected():
    db=Db()
    qry="SELECT * FROM `employee` WHERE `empstatus`='rejected'"
    res=db.select(qry)
    return render_template('hr/applrejected.html',data=res)

@app.route('/manageemp')
def manageemp():
    db = Db()
    qry = "SELECT * FROM `employee` WHERE `empstatus`='accepted'"
    res = db.select(qry)
    return render_template('hr/manageemp.html',data=res)

@app.route('/addleave/<id>')
def addleave(id):
    db=Db()
    qry="SELECT * FROM `employee` WHERE  `empid`='"+id+"'"
    res=db.selectOne(qry)
    return render_template('hr/addleave.html',data=res)
@app.route('/addleave_post',methods=['post'])
def addleave_post():
    loginid=request.form['loginid']
    empid=request.form['empid']
    normal=request.form['annual']
    emergency=request.form['emer']
    medical=request.form['medical']
    db=Db()
    qry="INSERT INTO `leave` (`loginid`,`empid`,`normal`,`ntaken`,`medical`,`mtaken`,`emergency`,`etaken`)VALUES('"+loginid+"','"+empid+"','"+normal+"','0','"+medical+"','0','"+emergency+"','0')"
    res=db.insert(qry)

    return '''<script>confirm("Are sure to submit");window.location='/manageemp'</script>'''

@app.route('/viewleave')
def viewleave():
    db=Db()
    qry="SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`empid`=`employee`.`empid` "
    res=db.select(qry)
    return render_template('hr/viewleave.html',data=res)
@app.route('/filterby',methods=['post'])
def filterby():
    dept=request.form['filter']
    db=Db()
    qry="SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`empid`=`employee`.`empid` WHERE `dept` LIKE '"+dept+"'"
    res=db.select(qry)
    return render_template('hr/viewleave.html',data=res)

@app.route('/viewleaveappl')
def viewleaveappl():
    db=Db()
    qry="SELECT *  FROM `request` INNER JOIN `employee` ON `request`.`empid`= `employee`.`empid` "
    res=db.select(qry)
    return render_template('hr/viewleaveappl.html',data=res)
@app.route('/totleavemp/<id>')
def totleavemp(id):
    db=Db()
    qry="SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`empid`=`employee`.`empid` WHERE `leave`.`empid`='"+id+"' "
    res=db.select(qry)
    return render_template('hr/viewleave.html',data=res)

@app.route('/acceptappl/<id>')
def acceptappl(id):
    db=Db()
    qry="UPDATE `request` SET `leavestatus`='accepted' WHERE `empid`='"+id+"'"
    res=db.update(qry)
    return redirect('/viewleaveappl')

@app.route('/rejectappl/<id>')
def rejectappl(id):
    db=Db()
    qry="UPDATE `request` SET `leavestatus`='rejected' WHERE `empid`='"+id+"'"
    res=db.update(qry)
    return redirect('/viewleaveappl')

@app.route('/filterrequest',methods=['post'])
def filterrequest():
    db=Db()
    status=request.form['filter']
    qry="SELECT *  FROM `request` INNER JOIN `employee` ON `request`.`empid`= `employee`.`empid` WHERE `leavestatus` LIKE '"+status+"'"
    res=db.select(qry)
    return render_template('hr/viewleaveappl.html',data=res)
#manager=================================================================

@app.route('/mngrhome')
def mngrhome():
    return render_template('manager/mngrhome.html')
@app.route('/mansignup_post' ,methods=['post'])
def mansignup_post():
    name=request.form['name1']
    dept=request.form['dept']
    post=request.form['post']
    dob=request.form['dob']
    address=request.form['address']
    #FOTO------------------
    photo = request.files['foto']
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save(r"C:\\Users\\hp\\PycharmProjects\\untitled\\static\\employee\\" + date + ".jpg")
    path = "/static/employee/" + date + ".jpg"
    db=Db()
    username = request.form['username']
    confpass = request.form['conf']
    qry2 = "INSERT INTO `login` (`username`,`password`,`type`) VALUES ('" + username + "','" + confpass + "','manager')"
    res1 = db.insert(qry2)
    qry="INSERT INTO `manager` (`loginid`,`name`,`department`,`post`,`address`,`photo`,`dob`,`manstatus`) VALUES ('"+str(res1)+"','"+name+"','"+dept+"','"+post+"','"+address+"','"+path+"','"+dob+"','pending')"
    res=db.insert(qry)
    return '''<script>alert("singnup succesfful please logic again");window.location='/'</script>'''

@app.route('/mansignup')
def mansignup():
    return render_template('manager/mansignup.html')

@app.route('/leavereq')
def leavereq():
    db=Db()
    qry="SELECT *  FROM `request` INNER JOIN `employee` ON `request`.`loginid`=`employee`.`loginid` WHERE `leavestatus`='pending'"
    res=db.select(qry)
    return render_template('manager/leavereq.html',data=res)

@app.route('/acceptappl2/<id>')
def acceptappl2(id):
    db=Db()
    # qry="UPDATE `request` SET `leavestatus`='accepted' WHERE `requestid`='"+id+"'"
    # res=db.update(qry)
    qry2 = "SELECT *  FROM `request` WHERE `leavestatus`='pending' AND `requestid`='"+id+"'"
    res2= db.select(qry2)
    if res2 is not None:
        if res2['type']=="normal":
            qry3="UPDATE `leave` SET `ntaken`=`ntaken`+ res2['days'] WHERE `leaveid`=res2['leaveid']"
            res3=db.update(qry3)
            return '''<script>alert('annual leave updated');window.location='/leavereq'</script>'''
        elif res2['type']=="medical":
            qry3 = "UPDATE `leave` SET `mtaken`=`mtaken`+ res2['days']  WHERE `leaveid`=res2['leaveid']"
            res3 = db.update(qry3)
            return '''<script>alert('medical leave updated');window.location='/leavereq'</script>'''
        elif res2['type']=="emergency":
            qry3 = "UPDATE `leave` SET `etaken`=`etaken`+ res2['days'] WHERE `leaveid`=res2['leaveid']"
            res3 = db.update(qry3)
            return '''<script>alert('emergency leave updated');window.location='/leavereq'</script>'''
        else:
            return'''<script>alert('Leave Not Updated');window.location='/'</script>'''


    return redirect('/leavereq')
@app.route('/rejectappl2/<id>')
def rejectappl2(id):
    db=Db()
    qry="UPDATE `request` SET `leavestatus`='rejected' WHERE `empid`='"+id+"'"
    res=db.update(qry)
    return redirect('/leavereq')

@app.route('/mngremp')
def mngremp():
    db = Db()
    qry = "SELECT * FROM `employee` WHERE `empstatus`='accepted'"
    res = db.select(qry)
    return render_template('manager/mangremp.html',data=res)

@app.route('/viewprofile')
def viewprofile():
    db=Db()
    qry="SELECT * FROM `manager` WHERE `loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('manager/viewProfile.html',data=res)

@app.route('/editprofile',methods=['post'])
def editprofile():
    name=request.form['fullname']
    birth=request.form['dob']
    address=request.form['address']
    photo=request.files['foto']
    from datetime import datetime
    date=datetime.now().strftime("%Y%m%d-%H%M%S")
    photo.save(r"C:\\Users\\hp\\PycharmProjects\\untitled\\static\\employee\\" + date + ".jpg")
    path="/static/employee/" + date + ".jpg"

    db=Db()
    qry="UPDATE `manager` SET `name`='"+name+"',`address`='"+address+"',`photo`='"+path+"',`dob`='"+birth+"' WHERE `loginid`='"+str(session['lid'])+"'"
    res=db.update(qry)
    return redirect('/viewprofile')

@app.route('/viewleavemn/<id>')
def viewleavemn(id):
    db=Db()
    qry="SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`empid`=`employee`.`empid` WHERE `leave`.`empid`='"+id+"' "
    res=db.selectOne(qry)
    return render_template('manager/viewleavemn.html',data=res)


#employee====================================================================
@app.route('/emphome')
def emphome():
    return render_template('employee/emphome.html')

@app.route('/viewempleave')
def viewempleave():
    db=Db()
    qry="SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`loginid`=`employee`.`loginid` WHERE `employee`.`loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('employee/viewempleave.html',data=res)

@app.route('/applyleave')
def applyleave():
    db=Db()
    qry="SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`loginid`=`employee`.`loginid` WHERE `employee`.`loginid`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template('employee/applyleave.html',data=res)

@app.route('/applyleave_post',methods=['post'])
def applyleave_post():
    empid=request.form['empid']
    leaveid=request.form['leaveid']
    type=request.form['type']
    datefrom=request.form['date1']
    dateto=request.form['date2']
    days=request.form['days']
    reason=request.form['rsn']
    db=Db()
    qry = "SELECT * FROM `leave` INNER JOIN `employee` ON `leave`.`loginid`=`employee`.`loginid` WHERE `employee`.`loginid`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        session['lid']=res['loginid']
        if (type=="normal") and (res['ntaken']==res['normal']):
            return '''<script>alert('You maxed out your annual leave');window.location='/emphome'</script>'''
        elif  (type=="medical")and(res['mtaken']==res['medical']):
            return '''<script>alert('You maxed out your medical leave');window.location='/emphome'</script>'''
        elif (type=="emergency")and (res['etaken']==res['emergency']):
            return '''<script>alert('You maxed out your emergency leave');window.location='/emphome'</script>'''
        else:
            qry2="INSERT INTO `request` (`empid`,`loginid`,`leaveid`,`type`,`leavestatus`,`datefrom`,`dateto`,`reason`,`days`) VALUES ('"+leaveid+"','"+str(session['lid'])+"','"+leaveid+"','"+type+"','pending','"+datefrom+"','"+dateto+"','"+reason+"','"+days+"')"
            res=db.insert(qry2)
            return '''<script>alert('Your Request  successfully forwarded');window.location='/emphome'</script>'''


if __name__ == '__main__':
    app.run(debug=True)
