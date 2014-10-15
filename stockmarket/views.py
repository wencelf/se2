from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from stockmarket.models import Investor, Startup, Bank
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from decimal import Decimal
from operator import itemgetter, attrgetter
import json
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2


# Create your views here.

def index(request):
    #return HttpResponse("Hello, Jefrey, You're at the SE stockmarket!")
	user_list = Investor.objects.all()
	return render_to_response('index.html',
		{'user_list':user_list}, #conection with template
		context_instance=RequestContext(request)  # for make work STATIC_URL 
		)   
def fblogin(request):
	response_data = {}
	try:
		if request.method == 'POST':
			this_email=request.POST['email']		
			this_img=request.POST['imagen']
		else:
			this_email=request.GET['email']			
			this_img=request.GET['imagen']	
		usuario=Investor.objects.get(email=this_email)
		#if usuario.imagen.url == 'undefined':
		#	img_temp = NamedTemporaryFile()
		#	img_temp.write(urllib2.urlopen(this_img).read())
		#	img_temp.flush()
		#	usuario.imagen.save('foto'+usuario.username+'.jpg', File(img_temp))
		#if usuario.imgurl == '':
		usuario.imgurl=this_img
		usuario.save()
		u = authenticate(username=usuario.username)
		login(request, u)
		request.session['member_id'] = u.id
		response_data['result'] = 'Usuario existente. Ingresara con su usuario de Facebook'		
	except Investor.DoesNotExist:
		if request.method == 'POST':
			this_email=request.POST['email'].lower()
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			this_img=request.POST['imagen']
		else:
			this_email=request.GET['email'].lower()
			first_name = request.GET['first_name']
			last_name = request.GET['last_name']
			this_img=request.GET['imagen']
		u = Investor.objects.create_user(username=this_email[:29], password="12345", email=this_email, first_name=first_name, last_name=last_name)
		#img_temp = NamedTemporaryFile()
		#img_temp.write(urllib2.urlopen(this_img).read())
		#img_temp.flush()
		#u.imagen.save('foto'+u.username+'.jpg', File(img_temp))
		u.imgurl=this_img
		u.set_unusable_password()
		u.save()
		request.session['member_id']=u.id
		response_data['result'] = 'Usuario no existente. Se creara una cuenta nueva con sus dtos de Facebook'
	return HttpResponse(json.dumps(response_data), content_type="application/json")
		
def signin(request):
    if request.method == 'POST': #if form has been submitted..
        email = request.POST['email'].lower()
        password = request.POST['password'] 
        this_username=Investor.objects.get(email=email).username
        u = authenticate(username=this_username, password=password)
        if u is not None:
            if u.is_active:
                 login(request,u)
                 request.session['member_id'] = u.id
                 #return HttpResponse("You are a Member!")
                 return HttpResponseRedirect('/home/')
            else:
                return HttpResponse("Your account has been disabled!")
        else:
            #return HttpResponseRedirect('/')
            return render_to_response('bad-login.html',
                {'u':u}, #conection with template
                context_instance=RequestContext(request)  # for make work STATIC_URL 
                )
    else:
        return HttpResponseRedirect('/')
    
def signup(request):
    if request.method == 'POST': #if form has been submitted..
        password = request.POST['password']
        email = request.POST['email'].lower()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        u = Investor.objects.create_user(username=email[:29], password=password, email=email, first_name=first_name, last_name=last_name)
        #i=Investor(user_id=u.id, cash=10)
        #i.save()
        request.session['member_id']=u.id
        #return HttpResponse("Thanks for joining. You are a member now!")
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/')
    
def home(request):

    try:
        u=Investor.objects.get(id=request.session['member_id'])
        startup_list = Startup.objects.all()
        return render_to_response('home.html',
            {'u':u,'startup_list':startup_list}, #conection with template
            context_instance=RequestContext(request)  # for make work STATIC_URL 
            )
    except KeyError:
        pass
        return HttpResponseRedirect('/')

        
def startup(request, startup_id):
    try:
        u=Investor.objects.get(id=request.session['member_id'])
        s = get_object_or_404(Startup, pk=startup_id)
        transaction_list=Bank.objects.filter(seller=s.id)
        #Following if statement check infor required to calcula company valuation 
        if not transaction_list:
            print "No records for this company"
            last_price = 0
            outstanding_shares=0
        else:
            last_price = transaction_list.order_by('-id')[0].price
            outstanding_shares=0
            for transaction in transaction_list:
                outstanding_shares += transaction.shares     
        valuation = s.askingPrice*outstanding_shares
        #following lines check if the current user is the ceo of the company. If so, the site will allow special persimissions
        if u.id == s.ceo.id:
            owner=1
        else:
            owner=0
        return render_to_response('startup.html', 
            {'u':u,'s':s,'valuation':valuation,'owner':owner},
            context_instance=RequestContext(request)
            )
    except KeyError:
        pass
        return HttpResponseRedirect('/')
    
def success(request):
    u=Investor.objects.get(id=request.session['member_id'])
    return render_to_response('startup.html', 
            {'u':u,'s':s},
            context_instance=RequestContext(request)
            )

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

def validate_purchase(request):
    if request.method == 'POST': #if form has been submitted..
        #s = request.POST['startup']
        shares = int(request.POST['shares'])
        u=Investor.objects.get(id=request.session['member_id'])
        s=Startup.objects.get(id=request.POST['startup'])
        print "Resultado de multiplicacion"
        print s.askingPrice*shares
        if u.investor.cash >= s.askingPrice*shares:
			u.investor.cash = u.investor.cash - s.askingPrice*shares
			u.investor.save() 
			b=Bank(buyer_id = u.id, seller_id = s.id, shares=shares, price = s.askingPrice )
			b.save()
			s.last_price=s.askingPrice
			s.save()
			return render_to_response('success.html', 
				{'u':u,'s':s, 'shares': shares},
				context_instance=RequestContext(request)
				)
            #return HttpResponseRedirect('/success')
        else:
            #return HttpResponse("You don't have enough money to buy this stock. Sorry")
            return render_to_response('fail.html', 
                {'u':u,'s':s, 'shares': shares},
                context_instance=RequestContext(request)
                )    
    else:
        return HttpResponseRedirect('/')
    
def edit_startup(request, startup_id):
    try:        
        u = Investor.objects.get(id=request.session['member_id'])
        s = get_object_or_404(Startup, pk=startup_id)
        #If user is not the company owner, it will be redirected to index
        if u.id == s.ceo.id:
            return render_to_response(
                'edit-startup.html', 
                {'u':u,'s':s},
                context_instance=RequestContext(request)
                )
        else:
            return HttpResponseRedirect('/')
    
    except KeyError:
        pass
        return HttpResponseRedirect('/')     

def validate_price(request):
    if request.method == 'POST': #if form has been submitted..
		new_price = (request.POST['new_price'])
		s=Startup.objects.get(id=request.POST['startup'])
		s.askingPrice = new_price
		s.save()
		return HttpResponseRedirect('/home')
		
    else:
        return HttpResponseRedirect('/')
    
def my_portafolio(request):
    
    try:        
        u = Investor.objects.get(id=request.session['member_id'])
        transaction_list=Bank.objects.filter(buyer=u.id)
        portfolio_value = 0
        for t in transaction_list:
            portfolio_value += t.shares*t.seller.last_price     
        return render_to_response(
                'my-portfolio.html', 
                {'u':u,'transaction_list':transaction_list,'portfolio_value':portfolio_value},
                context_instance=RequestContext(request)
                )
        
    except KeyError:
        pass
        return HttpResponseRedirect('/')  
'''    
def winner(request):
    u_list=User.objects.all()
    max=0
    winner="Nadie"
    for u in u_list:
        transaction_list=Bank.objects.filter(buyer=u.id)
        portfolio_value=0
        for t in transaction_list:
            portfolio_value += t.shares*t.seller.last_price
        if portfolio_value > max:
            max = portfolio_value    
            winner =  u.email
    
    return HttpResponse(winner)
'''
def winner(request):
    u_list = Investor.objects.filter(is_staff=0)
    #max=0
    winner="Nadie"
    i=0
    for u in u_list:
        transaction_list=Bank.objects.filter(buyer=u.id)
        portfolio_value=0
        for t in transaction_list:
            portfolio_value += t.shares*t.seller.last_price
        u_list[i].portfolio = portfolio_value
        i=i+1
    
    j_list=sorted(u_list, key=attrgetter('portfolio'), reverse=True)
    return render_to_response(
            'winner.html', 
            {'j_list':j_list},
            context_instance=RequestContext(request)
            )
    
