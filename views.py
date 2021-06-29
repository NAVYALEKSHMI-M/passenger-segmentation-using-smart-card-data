from django.shortcuts import render
from .models import user_login,user_details,category_master,location_master,pic_pool,user_search_history,public_user_details
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from .algo_impl import orb_compute,selfile,get_kp
from datetime import datetime
import os
# Create your views here.
def index(request):
    return render(request,'./myapp/index.html')

def about(request):
    return render(request,'./myapp/about.html')

def contact(request):
    return render(request,'./myapp/contact.html')

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd)

        if len(ul) == 1:
            request.session['user_id'] = ul[0].uname
            context = {'uname': request.session['user_id']}
            return render(request, 'myapp/admin_home.html',
                          context)
        else:
            context={'msg':'Login Error'}
            return render(request, 'myapp/admin_login.html',context)
    else:
        return render(request, 'myapp/admin_login.html')

def admin_home(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_home.html',context)

def admin_settings(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_settings.html',context)

def admin_settings_404(request):

    context = {'uname':request.session['user_id']}
    return render(request,'./myapp/admin_settings_404.html',context)

def admin_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_id']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                return render(request, './myapp/admin_settings.html')
            else:
                return render(request, './myapp/admin_settings.html')
        except user_login.DoesNotExist:
            return render(request, './myapp/admin_changepassword.html')
    else:
        return render(request, './myapp/admin_changepassword.html')


def admin_category_master_add(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')

        cm = category_master(category_name=category_name)
        cm.save()
        context={'msg':'Category Added'}
        return render(request, 'myapp/admin_category_master_add.html',context)

    else:
        return render(request, 'myapp/admin_category_master_add.html')

def admin_category_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    cm = category_master.objects.get(id=int(id))
    cm.delete()

    cm_l = category_master.objects.all()
    context ={'category_list':cm_l,'msg':'Record Deleted'}
    return render(request,'myapp/admin_category_master_view.html',context)

def admin_category_master_view(request):
    cm_l = category_master.objects.all()
    context = {'category_list': cm_l}
    return render(request, 'myapp/admin_category_master_view.html', context)

def admin_location_master_add(request):
    if request.method == 'POST':
        loc_name =request.POST.get('loc_name')
        addr1 = request.POST.get('addr1')
        addr2 = request.POST.get('addr2')
        addr3 = request.POST.get('addr3')
        pin = request.POST.get('pin')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        radius = request.POST.get('radius')
        remarks = request.POST.get('remarks')
        lm = location_master(loc_name=loc_name,addr1=addr1,addr2=addr2,addr3=addr3,pin=pin,lat=lat,lng=lng,radius=radius,remarks=remarks)
        lm.save()
        context={'msg':'Record added'}
        return render(request, 'myapp/admin_location_master_add.html',context)

    else:
        return render(request, 'myapp/admin_location_master_add.html')

def admin_location_master_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    lm = location_master.objects.get(id=int(id))
    lm.delete()

    lm_l = location_master.objects.all()
    context ={'location_list':lm_l}
    return render(request,'myapp/admin_location_master_view.html',context)

def admin_location_master_view(request):
    lm_l = location_master.objects.all()
    context = {'location_list': lm_l}
    return render(request, 'myapp/admin_location_master_view.html', context)


def admin_pic_pool_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)

        category_master_id = int(request.POST.get('category_master_id'))
        location_master_id = int(request.POST.get('location_master_id'))
        pic_obj = pic_pool(pic_path=pic_path,category_master_id=category_master_id,location_master_id=location_master_id)
        pic_obj.save()
        category_list = category_master.objects.all()
        location_list = location_master.objects.all()

        context = {'category_list': category_list, 'location_list': location_list,'msg':'Uploaded'}

        return render(request, 'myapp/admin_pic_pool_add.html',context)
    else:
        category_list = category_master.objects.all()
        location_list = location_master.objects.all()

        context = {'category_list': category_list,'location_list':location_list}

        return render(request, 'myapp/admin_pic_pool_add.html',context)


def admin_pic_pool_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    lm = pic_pool.objects.get(id=int(id))
    lm.delete()

    pp_l = pic_pool.objects.all()

    lm_l = location_master.objects.all()
    lmd = {}
    for nm in lm_l:
        lmd[nm.id] = nm.loc_name

    cm_l = category_master.objects.all()
    cmd = {}
    for nm in cm_l:
        cmd[nm.id] = nm.category_name

    context = {'pic_list':pp_l,'location_list': lmd,'category_list':cm_l}
    return render(request,'myapp/admin_pic_pool_view.html',context)

def admin_pic_pool_view(request):
    pp_l = pic_pool.objects.all()

    lm_l = location_master.objects.all()
    lmd = {}
    for nm in lm_l:
        lmd[nm.id] = nm.loc_name

    cm_l = category_master.objects.all()
    cmd = {}
    for nm in cm_l:
        cmd[nm.id] = nm.category_name

    context = {'pic_list': pp_l, 'location_list': lmd, 'category_list': cmd}
    return render(request, 'myapp/admin_pic_pool_view.html', context)


########USER#############
def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            context = {'uname': request.session['user_name']}
            return render(request, 'myapp/user_home.html',context)
        else:
            context={'msg':'Login Error'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = '1234'
        uname=email
        status = "new"

        ul = user_login(uname=uname, password=password, utype='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, addr=addr, pin=pin, contact=contact,
                               status=status,email=email )
        ud.save()

        print(user_id)

        return render(request, 'myapp/user_login.html')

    else:
        return render(request, 'myapp/user_details_add.html')


def user_search_history_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()

        pic_path = fs.save(randomString(10)+uploaded_file.name, uploaded_file)
        print(pic_path)

        pic_list = pic_pool.objects.all()
        cnt = 0
        cnt1= 0
        selfile=''
        selcat=0
        selcnt=0
        for pic in pic_list:
            file1 = f'./myapp/static/myapp/media/{pic.pic_path}'
            file2 = f'./myapp/static/myapp/media/{pic_path}'
            cnt1 = orb_compute(file1,file2,cnt)
            if cnt1 >= cnt:
                selfile=file1
                selcat=pic.category_master_id
                selcnt=cnt1
            cnt = cnt1
            print(f"{file1},{file2},{cnt}")

        m_cnt = get_kp(selfile)
        print(selfile)
        print(f'{selcnt} -- {m_cnt}')
        print(selcat)


        cm = category_master.objects.get(id=int(selcat))

        user_id = int(request.session['user_id'])
        result = cm.category_name
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        status = str((selcnt/m_cnt)*100)

        ud = user_search_history(user_id=user_id, pic_path=pic_path, result=result, dt=dt, tm=tm, status=status,
                                 )
        ud.save()

        context = {'category_name': cm.category_name,'percentage':status}
        return render(request, 'myapp/user_search_result.html',context)
    else:
        context = {}

        return render(request, 'myapp/user_search_history_add.html',context)

def user_search_history_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    lm = user_search_history.objects.get(id=int(id))
    lm.delete()
    return user_search_history_view(request)

def user_search_history_view(request):
    ush_l = user_search_history.objects.all()

    context = {'search_list': ush_l}
    return render(request, 'myapp/user_search_history_view.html', context)

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                return render(request, './myapp/user_settings.html')
            else:
                return render(request, './myapp/user_settings.html')
        except user_login.DoesNotExist:
            return render(request, './myapp/user_changepassword.html')
    else:
        return render(request, './myapp/user_changepassword.html')

def user_settings(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_settings.html',context)

def feedback_add(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        feedback = request.POST.get('feedback')
        location = request.POST.get('location')
        hname = request.POST.get('hname')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')



        #user_id = int(request.session['user_id'])
        ####################
        km = user_feedback(fname=fname,lname=lname,feedback=feedback,location=location,hname=hname,dt=dt,tm=tm)
        km.save()
        context = {'msg': 'feedback posted'}
        return render(request, './myapp/feedback_add.html', context)
    else:

        context = {}

        return render(request, './myapp/feedback_add.html',context)


from .models import user_feedback

def feedback_add_view(request):
    ush_l = user_feedback.objects.all()

    context = {'message_list': ush_l}
    return render(request, './myapp/feedback_add_view.html', context)


##############public user##################
def public_user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, password=passwd,utype='puser')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            context = {'uname': request.session['user_name']}
            return render(request, 'myapp/public_user_home.html',context)
        else:
            context={'msg':'Login Error'}
            return render(request, 'myapp/public_user_login.html',context)
    else:
        return render(request, 'myapp/public_user_login.html')

def public_user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/public_user_home.html',context)

def public_user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = '1234'
        uname=email
        status = "new"

        ul = user_login(uname=uname, password=password, utype='puser')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = public_user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, addr=addr, pin=pin, contact=contact,
                               status=status,email=email )
        ud.save()

        print(user_id)

        return render(request, 'myapp/public_user_login.html')

    else:
        return render(request, 'myapp/public_user_details_add.html')



###########################################
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

