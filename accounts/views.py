from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
import psycopg2
#from config import config
#from .models import Department

# Create your views here.

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
        return redirect('search')
    else:
        return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                return redirect('login')
        else:
            messages.info(request,'Password not matching...')
        return redirect('/')


    else:
        return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def search(request):
    if request.method=='POST':
        answer1 = request.POST['answer1']
        if answer1=='YES':
            ip_address = request.POST['ip_address']
            try:
                    #params=config(host="localhost",database="logdb", user="postgres", password="123456")
                    conn = psycopg2.connect(host="localhost",database="logdb", user="postgres", password="123456")
                    cur = conn.cursor()
                    #cur.execute("BEGIN")
                    #να δώσουμε το όνομα της κάθε stored function
                    cur.callproc('name_of_our_stored_function', (ip_address,))
                    row = cur.fetchall()
                    while row is not None:
                        #Λογικά θα εμφανίζει τα αποτελέσματα
                        messages.info(request,row)
                        row = cur.fetchone()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while connecting to PostgreSQL",error)
            finally:
                if(conn):
                    cur.close()
                    conn.close()
                    print("PostgreSQL connection is closed")
            return render(request,'search.html')
        else:
            answer = request.POST['answer']
            if answer == 'YES':
                return redirect('/')
            else:
                return redirect('search')
    else:
        return render(request,'search.html')

def additems(request):
    if request.method=='POST':
        ip_address = request.POST['ip_address']
        user_id = request.POST['user_id']
        http_method = request.POST['http_method']
        resource = request.POST['resource']
        http_response = request.POST['http_response']
        date=request.POST['date']

        sql = """INSERT INTO accesslog (ip_address,user_id,http_method,resource,http_response,date)
             VALUES(%s,%s,%s,%s,%s,%s);"""
        try:
            conn = psycopg2.connect(host="localhost",database="logdb", user="postgres", password="123456")
            cur = conn.cursor()
            cur.execute(sql, (ip_address,user_id,http_method,resource,http_response,date))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL",error)
        finally:
            if conn is not None:
                conn.close()
        messages.info(request,[ip_address,user_id,http_method,resource,http_response,date])
        answer3 = request.POST['answer3']
        if answer3 == 'YES':
            return redirect('/')
        else:
            return redirect('additems')

    else:
        return render(request,'additems.html')

def update(request):
    if request.method=='POST':
        #ip_address = request.POST['ip_address']
        user_id = request.POST['user_id']
        #http_method = request.POST['http_method']
        resource = request.POST['resource']
        #http_response = request.POST['http_response']
        #date=request.POST['date']

        sql = """UPDATE accesslog
        SET resource=%s
        WHERE user_id=%s;"""
        try:
            conn = psycopg2.connect(host="localhost",database="logdb", user="postgres", password="123456")
            cur = conn.cursor()
            cur.execute(sql, (resource,user_id))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL",error)
        finally:
            if conn is not None:
                conn.close()
        messages.info(request,[user_id,resource])
        answer4 = request.POST['answer4']
        if answer4 == 'YES':
            return redirect('/')
        else:
            return redirect('update')

    else:
        return render(request,'update.html')
