from django.shortcuts import render, redirect
import json

# Create your views here.
import boto3
from boto3.dynamodb.conditions import Key,Attr
from django.contrib import messages

user={}
dynamodb = boto3.resource('dynamodb')
renterTable = dynamodb.Table('Renter')
maintenanceTable = dynamodb.Table('Maintenance')
amenitiesTable = dynamodb.Table('Amenities')
propertyTable = dynamodb.Table('Property')
floorplansTable = dynamodb.Table('floorplans')
documentsTable = dynamodb.Table('DocumentData')



def dashboard(request):
    global user
    global dynamodb
    #user = dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1})
    #user = json.dumps(dynamodb.Table('Renter').get_item(Key={'renter_id':1, 'property_id':1}))

    #print(user)

    return render(request, 'portal/dashboard.html', {'user': user})
    #return HttpResponse("Hello, world. You're at the dashboard index.")

def employeedashboard(request):
    global user
    global dynamodb
    renterTable = dynamodb.Table('Renter')
    maintenanceTable = dynamodb.Table('Maintenance')
    amenitiesTable = dynamodb.Table('Amenities')
    propertyTable = dynamodb.Table('Property')
    scanAllRenter = renterTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    scanAllRenter.get('Items')
    scanUnpaidRenter = renterTable.scan(
        FilterExpression=Attr('paid').eq("false")
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    scanMaintenanceRequest = maintenanceTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    updateFixedMaintenance = maintenanceTable.update_item(
        Key={
            'property_id': propid,
            'renter_id': resid
        },
        UpdateExpression = "set maintainence_fixed = true"
    )
    scanAmenities = amenitiesTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )

    scanProperty = propertyTable.scan(
         #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )

    # unoccupied properties
    scanUnoccupiedProp = propertyTable.scan(
        FilterExpression=Attr('property_availability').eq('true')
    )

    updateRentAmount = propertyTable.update_item(
        Key={
            'property_id': propid
        },
        UpdateExpression = "set rent " + rentamount
    )


def resident_register(request):
    if request.method == "POST":
        username = request.POST['uname']
        apartment_number = int(request.POST['aptnum'])
        password = request.POST['psw']
        email = request.POST['email']
        contact = request.POST['contact']
        table = dynamodb.Table('Renter')
        table.put_item(
            Item={
                'username': username,
                'renter_id': email,
                'property_id': apartment_number,
                'password': password,
                'contact': contact,
            }
        )
        response = table.get_item(
            Key={
                'renter_id': email,
                # 'property_id': apartment_number
            }
        )
        item = response['Item']
        print(item)
        return render(request, 'portal/index.html')

def reslogin(request):
    # template = loader.get_template('./login.html')
    global user
    if request.method == 'POST':
        email = request.POST['resemail']
        password = request.POST['psw']
        table = dynamodb.Table('Renter')
        scanattributes = table.scan(
            FilterExpression=Attr('renter_id').eq(email) & Attr('password').eq(password)
        )
        items = scanattributes['Items']
        print(items)
        if len(items) == 0:
            return render(request, "portal/index.html")
        else:
            response = table.get_item(
                Key={
                    'renter_id': email,
                }
            )
        user = response['Item']
        # return redirect("userpage")

        ################################################################################
        # Added following section to display user reservations/requests on user homepage
        amenitiesTable = dynamodb.Table('Amenities')
        scanAllmaintenance = amenitiesTable.scan()
        amenities = scanAllmaintenance.get('Items')
        maintenanceTable = dynamodb.Table('Maintenance')
        scanAllmaintenance = maintenanceTable.scan(
            #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
        )
        renters = scanAllmaintenance.get('Items')
        print("Here")
        print(request.POST)
        # End of section
        ################################################################################


        return render(request, "portal/userpage.html", {'user': user, 'amenities': amenities, 'renters':renters})

def employee_register(request):
    if request.method == "POST":
        ename = request.POST['ename']
        pswdd = request.POST['pswdd']
        emailid = request.POST['emailid']
        phone = int(request.POST['phone'])
        table = dynamodb.Table('Employee')
        table.put_item(
            Item={
                'username': ename,
                'password': pswdd,
                'contact': phone,
                'employee_id': emailid,
            }
        )
        response = table.get_item(
            Key={
                'employee_id': emailid,
            }
        )
        item = response['Item']
        print(item)
        return redirect('employeepage')

def employeelogin(request):
    global user
    if request.method == 'POST':
        email = request.POST['empemail']
        password = request.POST['psw']
        table = dynamodb.Table('Employee')
        scanattributes = table.scan(
            FilterExpression=Attr('employee_id').eq(email) & Attr('password').eq(password)
        )
        items = scanattributes['Items']
        if len(items) == 0:
            return render(request, "portal/index.html")
        else:
            user = items[0]
            print(user)
            print(email)
            return redirect('employeepage')
            #return render(request, 'portal/employeepage.html', {'user':user})

def userpage(request):
    return render(request, "userpage.html", {'user': user})

def employeepage(request):
    global user
    global dynamodb
    renterTable = dynamodb.Table('Renter')
    maintenanceTable = dynamodb.Table('Maintenance')
    amenitiesTable = dynamodb.Table('Amenities')
    propertyTable = dynamodb.Table('Property')
    scanAllRenter = renterTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    renters = scanAllRenter.get('Items')
    scanMaintenanceRequest = maintenanceTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    maintenance = scanMaintenanceRequest.get('Items')
    scanProperty = propertyTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    properties = scanProperty.get('Items')
    scanAmenities = amenitiesTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    amenities = scanAmenities.get('Items')
    scanFloorplans = floorplansTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    floorplans = scanFloorplans.get('Items')
    scanDocuments = documentsTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    documents = scanDocuments.get('Items')
    for r in renters:
        for p in properties:
            if r['property_id'] == p['property_id']:
                p['username'] = r['username']
                if 'rent' in p :
                    r['rent'] = p['rent']
            

    if('del_maint' in request.POST):
        print("Maintenance issue resolved.")
        deleteResponse = maintenanceTable.delete_item(
            Key={
                'request_description': request.POST['req_desc'],
                'property_id': int(request.POST['property_id'])
            }
        )
        scanMaintenanceRequest = maintenanceTable.scan(
            #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
        )
        maintenance = scanMaintenanceRequest.get('Items')
    elif('del_reserve' in request.POST):
        print("Deleting Reservation...")
        deleteResponse = amenitiesTable.delete_item(
            Key={
                'renter_id': request.POST['rid'],
                'Reserved_area': request.POST['res_area']
            },
            ConditionExpression="Reserved_slot=:slot",
            ExpressionAttributeValues={
               ':slot': request.POST['res_slot']
            }
        )
        scanAmenities = amenitiesTable.scan(
            #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
        )
        amenities = scanAmenities.get('Items')
    elif('del_floorplan' in request.POST):
        print("Deleting Reservation...")
        deleteResponse = floorplansTable.delete_item(
            Key={
                'email_id': request.POST['eid'],
            },
        )
        scanFloorplans = floorplansTable.scan(
            #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
        )
        floorplans = scanFloorplans.get('Items')
    elif('del_property' in request.POST):
        print("Deleting Property...")
        deleteResponse = propertyTable.delete_item(
            Key={
                'property_id': int(request.POST['pid']),
            },
        )
        scanProperties = propertyTable.scan(
            #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
        )
        properties = scanProperties.get('Items')

    return render(request, "employeepage.html", {'user':user, 'renters': renters, 'maintenance': maintenance, 'amenities': amenities, 'floorplans': floorplans, 'properties':properties, 'documents':documents})

def saveRow(request):
    global user
    global dynamodb
    global renterTable
    global maintenanceTable
    global amenitiesTable
    global propertyTable
    global floorplansTable

    data = json.loads(json.dumps(request.POST))
    del data['csrfmiddlewaretoken']
    if data['table'] == 'rentertable':
        propid=data['property_id']
        renterid=data['renter_id']
        username=data['username']
        contact=data['contact']
        rent=data['rent']

        # extract keys not in table
        del data['table']
        # update rent first then delete from table
        propertyTable.update_item(
            Key={
                'property_id': int(propid)
            },
            UpdateExpression= "set rent=:rent",
            ExpressionAttributeValues={
                ':rent': rent
            }
        )
        del data['rent']
        # update renters table
        tableKey = data['renter_id']
        del data['renter_id']
        # create update expr
        updExpr = 'set '
        exprAttrVal = {}
        for key in data:
            updExpr += key + "=:" + key + ", "
            exprAttrVal[":" + key ] = data[key]
        updExpr = updExpr[:-2]
        # keep property_id int
        exprAttrVal[':property_id'] = int(exprAttrVal[':property_id'])
        renterTable.update_item(
            Key={
                'renter_id': tableKey
            },
            UpdateExpression = updExpr,
            ExpressionAttributeValues=exprAttrVal
        )
    elif data['table'] == 'maintenancetable':
        useTable = maintenanceTable
    elif data['table'] == 'amenitiestable':
        useTable = amenitiesTable
    elif data['table'] == 'propertiestable':
        # del tablename
        del data['table']
        # get table key (Number) in properties
        tableKey = int(data['property_id'])
        del data['property_id']
        updExpr = 'set '
        exprAttrVal = {}
        for key in data:
            updExpr += key + "=:" + key + ", "
            exprAttrVal[":" + key ] = data[key]
        updExpr = updExpr[:-2]
        exprAttrVal[':rent'] = int(exprAttrVal[':rent'])
        # update request to properties table
        propertyTable.update_item(
            Key={
                'property_id': tableKey
            },
            UpdateExpression = updExpr,
            ExpressionAttributeValues= exprAttrVal
        )

    return render(request, "employeepage.html", {'user':user})

def payment_redirect(request):
    global property
    return render(request, 'portal/payment_redirect.html', {'user': user, 'property' : property})


def paymentInfo(request):
    # template = loader.get_template('./login.html')
    global user
    print("Here in payment too")
    if request.method == 'POST':
        cardholder = request.POST['cardholder']
        cardnumber = request.POST['cardnumber']
        verification = request.POST['verification']
        custAmount = 12345
        custAmount = request.POST['custAmount']
        date = request.POST['date']
        table = dynamodb.Table('Property')

        table.update_item(
            Key={
                'property_id': user['property_id'],
            },
            UpdateExpression='SET paymentAmount = :paymentAmount',
            ExpressionAttributeValues={
                ':paymentAmount': custAmount
            }
        )
        response = table.get_item(
            Key={
                'property_id': user['property_id'],
            }
        )
        item = response['Item']
        print(item)

        # return redirect("userpage")

        return render(request, "portal/userpage.html", {'user': user})


def pay(request):
    global property
    print("USER WOULD LIKE TO PAY")
    print(user)
    scanres = dynamodb.Table('Property').scan(
    FilterExpression=Attr('property_id').eq(user['property_id']))
    property = scanres['Items'][0]
    return render(request, 'portal/pay.html', {'user': user, 'property': property})

def info(request):
    return render(request, 'portal/info.html')

def maintenance_redirect(request):
    global user

    maintenanceTable = dynamodb.Table('Maintenance')
    scanAllmaintenance = maintenanceTable.scan(
        #ProjectionExpression= HANDLE PROJECTION HERE OR IN HTML
    )
    renters = scanAllmaintenance.get('Items')
    print("In redirect")
    print(request.POST)
    if('del_amen' in request.POST):
        print("RESOLVED CLICKED RESOLVE CLICKED")
        print(request.POST['request_description'])
        deleteResponse = maintenanceTable.delete_item(
            Key={
            'property_id': int(request.POST['property_id']),
            'request_description': request.POST['request_description']
            },
            )
        # ConditionExpression="request_description = " + request.POST['req_desc']

        return redirect('maintenance_redirect')
    return render(request, 'portal/maintenance.html', {'user': user, 'renters' : renters})


def maintenance(request):
    global user
    global maintenance
    if request.method == 'POST':
        aptnum = int(request.POST['apartmentnum'])
        description = request.POST['request']
        table = dynamodb.Table('Maintenance')
        table.put_item(
            Item={
                'property_id': aptnum,
                'renter_id': user['renter_id'],
                'request_description': description,
            }
        )
        response = table.get_item(
            Key={
                'request_description': description,
                'property_id': aptnum,
            }
        )
        item = response['Item']
        print(item)
        return redirect('maintenance_redirect')

def amenities_redirect(request):
    # retrieve the database for amenities request history and to redirect to amenities portal
    amenitiesTable = dynamodb.Table('Amenities')
    scanAllmaintenance = amenitiesTable.scan()
    amenities = scanAllmaintenance.get('Items')
    print("Here")
    print(request.POST)
    if('del_amen' in request.POST):
        print("RESOLVED CLICKED RESOLVE CLICKED")
        deleteResponse = amenitiesTable.delete_item(
            Key={
                'renter_id': request.POST['renter_id'],
                'Reserved_area': request.POST['Reserved_area']
            },
            # ConditionExpression="request_description = " + request.POST['req_desc']
        )
        return redirect('amenities_redirect')

    return render(request, 'portal/amenities_reservations.html', {'user': user, 'amenities': amenities})

def amenities_slot(request):
    global user

    # Book plot for community_area, gym_area , pool_area

    if 'book_slot_community_area' in request.POST:
        area = 'community_area'
        date = request.POST['slot']
    elif 'book_slot_gym_area' in request.POST:
        area = 'gym_area'
        date = request.POST["gymslot"]
    elif 'book_slot_pool_area' in request.POST:
        area = 'pool_area'
        date = request.POST["poolslot"]

    amenitiesTable = dynamodb.Table('Amenities')
    scanAllamenities = amenitiesTable.scan()
    amenities = scanAllamenities.get('Items')
    if (amenities == []):
        amenitiesTable.put_item(
            Item={
                'renter_id': user['renter_id'],
                'property_id': user['property_id'],
                'Reserved_slot': date,
                'Reserved_area': area,
            }
        )
        response = amenitiesTable.get_item(
            Key={
                'renter_id': user['renter_id'],
                'Reserved_area': area,
            }
        )
        item = response['Item']
        messages.success(request,"Plot is booked successfully", extra_tags=area)
        return redirect('amenities_redirect')

    for i in amenities:
        if i['Reserved_slot'] == date and i['Reserved_area'] == area:
            messages.error(request, 'slot is booked, please book for a different slot', extra_tags=area)
            return redirect('amenities_redirect')
    amenitiesTable.put_item(
        Item={
            'renter_id': user['renter_id'],
            'property_id': user['property_id'],
            'Reserved_slot': date,
            'Reserved_area': area,
        }
    )
    response = amenitiesTable.get_item(
        Key={
            'renter_id': user['renter_id'],
            'Reserved_area' : area,
        }
    )
    messages.success(request,"Plot is booked successfully", extra_tags=area)
    return redirect('amenities_redirect')

def important_numbers(request):
    return render(request, 'portal/important_numbers.html', {'user': user})

def floorplans(request):
    return render(request, 'portal/floorplans.html')

def gallery(request):
    return render(request, 'portal/gallery.html')

def faq(request):
    return render(request, 'portal/FAQ.html')

def amenities(request):
    return render(request, 'portal/amenities.html')
    
def index(request):
    return render(request, "index.html")

def applyForApartment(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        table = dynamodb.Table('floorplans')
        table.put_item(
            Item={
                'name': name,
                'email_id': email,
                'contact_num': phone,
            }
        )
        response = table.get_item(
            Key={
                'email_id': email,
            }
        )
        item = response['Item']
        print(item)
        return render(request, 'portal/floorplans.html')
    # return {"message": "submitted succesfully"}

def Documents(request):
    print('checking Documents function')
    return render(request, 'portal/Documents.html',{'user': user})

def documentsUpload(request):
    if request.method == "POST":
        current_add = request.POST['current_Address']
        ssn = request.POST['ssn']
        dlFile = request.POST['dlFile']
        table = dynamodb.Table('DocumentData')
        table.put_item(
            Item={
                'current_add': current_add,
                'ssn': ssn,
                'dlFile': dlFile,
            }
        )
        response = table.get_item(
            Key={
                'ssn': ssn
            }
        )
        item = response['Item']
        print(current_add)
        print(ssn)
        print(dlFile)
    return render(request, 'portal/Documents.html',{'user': user})
