from flask import Flask, request, render_template, redirect, url_for, flash, session

from datetime import datetime

from mysql_db import (
    connect,
    disconnect,
    register_db,
    login_db,
    get_user,
    get_locations,
    add_locations,
    update_locations,
    get_locations_by_id,
    del_location,
    get_devices_by_location_id,
    get_devices_by_id,
    add_device,
    update_device,
    del_device,
    get_usage_by_device_id,
)

app = Flask(__name__)
app.secret_key = "smartdevice------------"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        row = []
        row.append(request.form.get("customer_name").strip())
        row.append(request.form.get("customer_phone").strip())
        row.append(request.form.get("billing_addr").strip())
        row.append(request.form.get("passwd").strip())
        if not row[0] or not row[1] or not row[2] or not row[3]:
            flash("please input infomation!")
            return redirect(url_for("register"))
        print(row)
        register_db(row)
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        customer_name = request.form.get("customer_name").strip()
        passwd = request.form.get("passwd").strip()
        if not customer_name or not passwd:
            flash("please input username and password!")
            return redirect(url_for("login"))

        reuslts = login_db(customer_name)
        print(reuslts)
        if reuslts:
            if reuslts[0][4] == passwd:
                session["id"] = reuslts[0][0]
                return redirect(url_for("index"))
            else:
                flash("wrong password!")
                return redirect(url_for("login"))
        else:
            flash("wrong name!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session["id"] = None
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    if request.method == "POST":
        customer_id = user[0]
        unit_and_street_address = request.form.get("unit_and_street_address").strip()
        city = request.form.get("city").strip()
        state = request.form.get("state").strip()
        zip_code = request.form.get("zip_code").strip()
        acquisitiondate = request.form.get("acquisitiondate").strip()
        square_footage = request.form.get("square_footage").strip()
        number_of_bedrooms = request.form.get("number_of_bedrooms").strip()
        number_of_occupants = request.form.get("number_of_occupants").strip()

        #check 
        if (
            not unit_and_street_address
            or not city
            or not state
            or not zip_code
            or not acquisitiondate
            or not square_footage
            or not number_of_bedrooms
            or not number_of_occupants
        ):
            flash("cannot be empty!")
            return redirect(url_for("index", user=user))
        if len(zip_code) > 10:
            flash("ZipCode must be no more than 10 characters!")
            return redirect(url_for("index", user=user))
        if (
            not square_footage.isdigit()
            or not number_of_bedrooms.isdigit()
            or not number_of_occupants.isdigit()
        ):
            flash(
                "SquareFootage,NumberOfBedrooms or NumberOfOccupants must be integer!"
            )
            return redirect(url_for("index", user=user))
        # save to db
        row = [
            customer_id,
            unit_and_street_address,
            city,
            state,
            zip_code,
            acquisitiondate,
            square_footage,
            number_of_bedrooms,
            number_of_occupants,
        ]
        add_locations(row)
        locations = get_locations(user[0])
        flash("Successfully added location")
        return render_template("index.html", user=user, locations=locations)

    locations = get_locations(user[0])
    print(locations)
    return render_template("index.html", user=user, locations=locations)


@app.route("/update/<location_id>", methods=["GET", "POST"])
def update(location_id):
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    if request.method == "POST":
        customer_id = user[0]
        unit_and_street_address = request.form.get("unit_and_street_address").strip()
        city = request.form.get("city").strip()
        state = request.form.get("state").strip()
        zip_code = request.form.get("zip_code").strip()
        acquisitiondate = request.form.get("acquisitiondate").strip()
        square_footage = request.form.get("square_footage").strip()
        number_of_bedrooms = request.form.get("number_of_bedrooms").strip()
        number_of_occupants = request.form.get("number_of_occupants").strip()

        if (
            not unit_and_street_address
            or not city
            or not state
            or not zip_code
            or not acquisitiondate
            or not square_footage
            or not number_of_bedrooms
            or not number_of_occupants
        ):
            flash("cannot be empty!")
            locations_res = get_locations_by_id(location_id)
            return render_template("update.html", user=user, location=locations_res[0])
        if len(zip_code) > 10:
            flash("ZipCode must be no more than 10 characters!")
            locations_res = get_locations_by_id(location_id)
            return render_template("update.html", user=user, location=locations_res[0])
        if (
            not square_footage.isdigit()
            or not number_of_bedrooms.isdigit()
            or not number_of_occupants.isdigit()
        ):
            flash(
                "SquareFootage,NumberOfBedrooms or NumberOfOccupants must be integer!"
            )
            locations_res = get_locations_by_id(location_id)
            return render_template("update.html", user=user, location=locations_res[0])
        row = [
            customer_id,
            unit_and_street_address,
            city,
            state,
            zip_code,
            acquisitiondate,
            square_footage,
            number_of_bedrooms,
            number_of_occupants,
        ]
        update_locations(location_id, row)
        locations = get_locations(user[0])
        flash("Successfully updated location")
        return render_template("index.html", user=user, locations=locations)

    locations_res = get_locations_by_id(location_id)
    return render_template("update.html", user=user, location=locations_res[0])


@app.route("/del/<location_id>")
def delete(location_id):
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    del_location(location_id)
    locations = get_locations(user[0])
    flash("Successfully deleted location")
    return render_template("index.html", user=user, locations=locations)


@app.route("/device/<location_id>", methods=["GET", "POST"])
def device(location_id):
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]
    location = get_locations_by_id(location_id)

    if request.method == "POST":
        device_type = request.form.get("device_type").strip()
        model_num = request.form.get("model_num").strip()
        if not device_type or not model_num:
            flash("cannot be empty!")
            devices = get_devices_by_location_id(location_id)
            return render_template(
                "device.html", user=user, location=location, devices=devices
            )
        if len(device_type) > 100 or len(model_num) > 100:
            flash("Device type or Model numbers must be no more than 100 characters!")
            devices = get_devices_by_location_id(location_id)
            return render_template(
                "device.html", user=user, location=location, devices=devices
            )
        add_device([location_id, device_type, model_num])
        flash("Successfully added device!")
        devices = get_devices_by_location_id(location_id)
        return render_template(
            "device.html", user=user, location=location, devices=devices
        )

    devices = get_devices_by_location_id(location_id)
    return render_template("device.html", user=user, location=location, devices=devices)

@app.route('/update_device/<device_id>',methods=['GET','POST'])
def update_device_(device_id):
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    if request.method=='POST':
        device_type = request.form.get("device_type").strip()
        model_num = request.form.get("model_num").strip()
        if not device_type or not model_num:
            flash("cannot be empty!")
            return redirect(url_for('update_device_',device_id=device_id))
        if len(device_type) > 100 or len(model_num) > 100:
            flash("Device type or Model numbers must be no more than 100 characters!")
            return redirect(url_for('update_device_',device_id=device_id))
        res = get_devices_by_id(device_id)
        location_id = res[0][1]
        update_device(device_id,[location_id, device_type, model_num])
        flash("Successfully updated device!")
        return redirect(url_for("device", location_id=location_id))

    res = get_devices_by_id(device_id)
    location_id = res[0][1]
    location=get_locations_by_id(location_id)
    return render_template('update_device.html',user=user,location=location)


@app.route("/del_device/<device_id>")
def del_device_(device_id):
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    res = get_devices_by_id(device_id)
    location_id = res[0][1]
    del_device(device_id)
    flash('Successfully deleted device!')
    return redirect(url_for("device", location_id=location_id))

@app.route("/charts")
def charts():
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    locations=get_locations(user[0])
    return render_template('charts.html',user=user,locations=locations)

@app.route('/energy_consumption',methods=['POST'])
def energy_consumption():
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]
    
    #get all device_id
    locations=get_locations(user[0])
    #print(locations)
    device_ids=[]
    for location in locations:
        devices=get_devices_by_location_id(location[0])
        for device in devices:
            device_ids.append(device[0])
    #print(device_ids)
    
    start_day=request.json.get('start_day').strip()
    end_day=request.json.get('end_day').strip()
    start_day=start_day+' 00:00:00'
    end_day=end_day+' 00:00:00'
    
    energy_usage_by_user=[]
    for device_id in device_ids:
        db = connect()
        cursor = db.cursor()
        sql = "SELECT * FROM energy_usage WHERE timestamp>=%s and timestamp<=%s and device_id=%s"
        results = None
        try:
            cursor.execute(sql, (start_day,end_day,device_id))
            results = cursor.fetchall()
            for result in results:
                energy_usage_by_user.append(result)
        except:
            print("Error: unable to fetch data")
        disconnect(db)
    #print(energy_usage_by_user)
    energy_usage_two_=[]
    for item in energy_usage_by_user:
        energy_usage_two_.append([item[1].strftime('%Y-%m-%d'),item[4]])
    #print(energy_usage_two_)
    usagecount = {}
    for item in energy_usage_two_:
        usagecount[item[0]] = usagecount.get(item[0], 0)+item[1]
    print(usagecount)

    return {
        'state':'success',
        'usagecount':usagecount
    }

@app.route('/devices_consumption',methods=['POST'])
def devices_consumption():
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]
    
    locations=get_locations(user[0])
    #print(locations)
    device_ids=[]
    for location in locations:
        devices=get_devices_by_location_id(location[0])
        for device in devices:
            device_ids.append(device[0])
    #print(device_ids)
    
    start_day=request.json.get('start_day').strip()
    end_day=request.json.get('end_day').strip()
    start_day=start_day+' 00:00:00'
    end_day=end_day+' 00:00:00'
    
    energy_usage_by_user=[]
    for device_id in device_ids:
        db = connect()
        cursor = db.cursor()
        sql = "SELECT * FROM energy_usage WHERE timestamp>=%s and timestamp<=%s and device_id=%s"
        results = None
        try:
            cursor.execute(sql, (start_day,end_day,device_id))
            results = cursor.fetchall()
            for result in results:
                energy_usage_by_user.append(result)
        except:
            print("Error: unable to fetch data")
        disconnect(db)
    #print(energy_usage_by_user)
    energy_usage_two_=[]
    for item in energy_usage_by_user:
        energy_usage_two_.append([item[0],item[4]])
    #print(energy_usage_two_)
    usagecount = {}
    for item in energy_usage_two_:
        usagecount[item[0]] = usagecount.get(item[0], 0)+item[1]
    #print(usagecount)
    usagecount_={}
    for key,val in usagecount.items():
        device_one=get_devices_by_id(key)
        key_=device_one[0][2]+'/'+device_one[0][3]
        usagecount_[key_]=val

    return {
        'state':'success',
        'usagecount':usagecount_
    }


@app.route('/location_compare',methods=['POST'])
def location_compare():
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]

    def get_location_total_usage(location_id):
        devices=get_devices_by_location_id(location_id)
        device_ids=[]
        for device in devices:
            device_ids.append(device[0])
        energy_usage_by_location=0
        for device_id in device_ids:
            db = connect()
            cursor = db.cursor()
            sql = "SELECT  SUM(event_value) FROM energy_usage WHERE device_id=%s"
            results = None
            try:
                cursor.execute(sql, (device_id,))
                results = cursor.fetchall()
                if results and results[0][0]:
                    energy_usage_by_location=energy_usage_by_location+results[0][0]
            except Exception as e:
                print(e)
            disconnect(db)
        #print(energy_usage_by_location)
        return energy_usage_by_location

    location_id=request.json.get('location_id').strip()
    location=get_locations_by_id(location_id)


    #other location average
    db=connect()
    cursor=db.cursor()
    sql="SELECT * FROM location WHERE location_id <> %s and square_footage>= %s and square_footage<=%s"
    other_locations = None
    try:
        cursor.execute(sql, (location_id,location[0][7]-200,location[0][7]+200))
        other_locations = cursor.fetchall()
    except:
        print("Error: unable to fetch data11")
    disconnect(db)
    other_locations_usage=[]
    for other_location in other_locations:
        one=get_location_total_usage(other_location[0])
        other_locations_usage.append(one)
    #print(other_locations_usage)
    averge=sum(other_locations_usage)/len(other_locations_usage)
    print(averge)

    location_usage=get_location_total_usage(location_id)

    return {
        'state':'success',
        'compare_data':[location_usage,averge]
    }

@app.route('/devices_consumption_cost',methods=['POST'])
def devices_consumption_cost():
    if not session.get("id"):
        return redirect(url_for("login"))
    reuslts = get_user(session.get("id"))
    user = reuslts[0]
    
    locations=get_locations(user[0])
    #print(locations)
    device_ids=[]
    for location in locations:
        devices=get_devices_by_location_id(location[0])
        for device in devices:
            device_ids.append(device[0])
    #print(device_ids)
    
    start_day=request.json.get('start_day').strip()
    end_day=request.json.get('end_day').strip()
    start_day=start_day+' 00:00:00'
    end_day=end_day+' 00:00:00'
    
    energy_usage_by_user=[]
    for device_id in device_ids:
        db = connect()
        cursor = db.cursor()
        sql = "SELECT * FROM energy_usage WHERE timestamp>=%s and timestamp<=%s and device_id=%s"
        results = None
        try:
            cursor.execute(sql, (start_day,end_day,device_id))
            results = cursor.fetchall()
            for result in results:
                energy_usage_by_user.append(result)
        except:
            print("Error: unable to fetch data")
        disconnect(db)
    #print(energy_usage_by_user)
    energy_costs=[]
    for item in energy_usage_by_user:
        devices=get_devices_by_id(item[0])
        location_=get_locations_by_id(devices[0][1])
        zipcode=location_[0][5]
        db=connect()
        cursor=db.cursor()
        sql="SELECT * FROM energy_price WHERE zip_code =%s AND start_time =%s"
        try:
            cursor.execute(sql, (zipcode,item[1]))
            results = cursor.fetchall()
            if results:
                energy_costs.append([item[0],results[0][2]*item[4]])
        except:
            print("Error: unable to fetch data")
        disconnect(db)
    #print(energy_costs)
    costs={}
    for energy_cost in energy_costs:
        costs[energy_cost[0]]=costs.get(energy_cost[0],0)+energy_cost[1]
    #print(costs)
    costs_={}
    for key,val in costs.items():
        device_one=get_devices_by_id(key)
        key_=device_one[0][2]+'/'+device_one[0][3]
        costs_[key_]=val

    return {
        'state':'success',
        'costs':costs_
    }


if __name__ == "__main__":
    app.run(debug=True)
