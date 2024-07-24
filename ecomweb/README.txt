def index(request):
    if request.POST:
        category=request.POST.get('category')
        if category=="all":
            products = product.objects.all()
            return render(request,'index.html',{'products': products})
        else:    
            products = product.objects.filter(category=category)
            return render(request,'index.html',{'products': products})

       

    products = product.objects.all()
    return render(request,'index.html',{'products': products})






    def addproduct(request):
    if request.POST:
        productname=request.POST.get("productname")
        prize=request.POST.get("prize")
        offer=request.POST.get("offer")
        speed=request.POST.get("speed")
        color=request.POST.get("color")
        description=request.POST.get("description")
        category=request.POST.get("category")
        image=request.FILES.get("image")
        seller=request.user
        if not productname or not prize or not offer or not speed or not color or not description or not category or not image:
            messages.error(request,"all fields are required")
            print(productname,prize,offer,speed,color,description,category)
            if image is not None:
                  print("hello")
        

        else:
            probj=product(productname=productname,prize=prize,offer=offer,speed=speed,color=color,description=description,category=category,seller=seller,image=image)
            probj.save()
            messages.success(request,"product added")    
            return redirect("additem")
        
    products = product.objects.filter(category=category)
    return render (request,"addpro.html",{"products":products})