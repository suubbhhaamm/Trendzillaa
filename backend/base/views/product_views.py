from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Product, Review
from base.serializers import ProductSerializer

from rest_framework import status

import psycopg2


l = list()

def switch_User():
    global l
    l = []


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts



def get_TopProductsBySearching(SearchedProducts):
    result = list()
    if len(SearchedProducts) > 3:
        for i in range(0,3):
            TopSearchedProduct = max(SearchedProducts, key=SearchedProducts.get)
            print(TopSearchedProduct)
            result.append(TopSearchedProduct)
            print(result)
            del SearchedProducts[TopSearchedProduct]
    else:
        while len(SearchedProducts) != 0:
            TopSearchedProduct = max(SearchedProducts, key=SearchedProducts.get)
            print(TopSearchedProduct)
            result.append(TopSearchedProduct)
            print(result)
            del SearchedProducts[TopSearchedProduct]
    return result  



def get_favoriteProductsByReviews(user):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="student@postgres123",
                                      host="localhost",
                                      port="5432",
                                      database="proshop")

        cursor = connection.cursor()
        postgreSQL_select_Query = r"select * from (select base_product.category, count(base_product.category) as FavoriteProducts from base_review inner join base_product on base_product._id = base_review.product_id where (lower(base_review.comment) like '%nice%' or lower(base_review.comment) like '%good%') group by base_product.category) A order by A.FavoriteProducts desc"
        #postgreSQL_select_Query = r"select * from (select base_product.category, count(base_product.category) as FavoriteProducts from base_review inner join base_product on base_product._id = base_review.product_id left join auth_user on auth_user.id = base_review.user_id where auth_user.username = '" + user + r"'  and (lower(base_review.comment) like '%nice%' or lower(base_review.comment) like '%good%') group by base_product.category) A order by A.FavoriteProducts desc"

        cursor.execute(postgreSQL_select_Query)
        product_category = cursor.fetchmany(3)
        print("product",  product_category)

        if len(product_category) == 1:
            return [product_category[0][0]]
        
        elif len(product_category) == 2:
                return [product_category[0][0], product_category[1][0]]
        else:
            return [product_category[0][0], product_category[1][0], product_category[2][0]]

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")


@api_view(['GET'])
def getMensProducts(request):
    products = Product.objects.filter(
    description__icontains='Bluetooth').order_by('-createdAt') | Product.objects.filter(
    description__icontains=' men').order_by('-createdAt') | Product.objects.filter(
    description__icontains=' boy').order_by('-createdAt') | Product.objects.filter(
    description__icontains=' Boy').order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(products, 4)


    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})
    
@api_view(['GET'])
def getWomenProducts(request):
    products = Product.objects.filter(
    description__icontains='women').order_by('-createdAt') | Product.objects.filter(
    description__icontains='Women').order_by('-createdAt') | Product.objects.filter(
    description__icontains='Girl').order_by('-createdAt') | Product.objects.filter(
    description__icontains='girl').order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(products, 4)


    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def getRecommendedProducts(request):
    query = request.query_params.get('keyword')

    if query != '':
        products = Product.objects.filter(
        name__icontains=query).order_by('-createdAt')

        print(query)
        l2 = query.split(" ")
        global l
        print(l)
        l = l + l2
        l.reverse()
        print(l)
        


    elif query == '' and len(l) != 0:
        print(l)
        str2 = ' '.join(l)
        print( word_count(str2))
        SearchedProducts = word_count(str2)
        print(SearchedProducts)
        TopSearchedProducts = get_TopProductsBySearching(SearchedProducts)
        print(TopSearchedProducts)
        print(len(TopSearchedProducts))

        if len(TopSearchedProducts) == 1:
            product1 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[0]))

            remaing_products = list(Product.objects.filter(
            name__icontains = ''))

            for product in product1:
                remaing_products.remove(product)

            products = product1 + remaing_products

        elif len(TopSearchedProducts) == 2:
            product1 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[0]))

            product2 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[1]))

            remaing_products = list(Product.objects.filter(
            name__icontains = ''))

            for product in product1:
                remaing_products.remove(product)
            for product in product2:
                remaing_products.remove(product)

            products = product1 + product2 + remaing_products

            
    
        elif len(TopSearchedProducts) == 3:
            product1 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[0]))
            
            product2 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[1]))
            
            product3 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[2]))

            remaing_products = list(Product.objects.filter(
            name__icontains = ''))

            for product in product1:
                remaing_products.remove(product)

            for product in product2:
                remaing_products.remove(product)

            for product in product3:
                remaing_products.remove(product)

            products = product1 + product2 + product3 + remaing_products

        elif len(TopSearchedProducts) == 4:
            product1 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[0]).order_by('-createdAt'))
            product2 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[1]).order_by('-createdAt'))
            product3 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[2]).order_by('-createdAt'))
            product4 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[3]).order_by('-createdAt'))

            remaing_products = list(Product.objects.filter(
            name__icontains = ''))

            for product in product1:
                remaing_products.remove(product)

            for product in product2:
                remaing_products.remove(product)

            for product in product3:
                remaing_products.remove(product)

            for product in product4:
                remaing_products.remove(product)

            products = product1 + product2 + product3 + product4 + remaing_products
            

        else:
            product1 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[0]).order_by('-createdAt'))
            product2 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[1]).order_by('-createdAt'))
            product3 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[2]).order_by('-createdAt'))
            product4 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[3]).order_by('-createdAt'))
            product5 = list(Product.objects.filter(
            name__icontains = TopSearchedProducts[4]).order_by('-createdAt'))

            remaing_products = list(Product.objects.filter(
            name__icontains = ''))

            for product in product1:
                remaing_products.remove(product)

            for product in product2:
                remaing_products.remove(product)

            for product in product3:
                remaing_products.remove(product)

            for product in product4:
                remaing_products.remove(product)

            for product in product5:
                remaing_products.remove(product)

            products = product1 + product2 + product3 + product4 + product5 + remaing_products

    page = request.query_params.get('page')
    paginator = Paginator(products, 4)


    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})



@api_view(['GET'])
def getProducts(request):
    
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    

    products = Product.objects.filter(
        name__icontains = '').order_by('-createdAt') 
    
    user = request.user
    print('hi', user)

    products = list()

    if query != '':
        products = Product.objects.filter(
        name__icontains=query).order_by('-createdAt')

        print(query)
        l2 = query.split(" ")
        global l
        print(l)
        l = l + l2
        l.reverse()
        print(l)
        

    else:
        print(request.user)
        products = Product.objects.filter(
        name__icontains = '').order_by('-createdAt') 
        user = request.user
        category = get_favoriteProductsByReviews(user)

        print(category)
  
    #     # # if len(category) == 1:
    #     # #     product1 = list(Product.objects.filter(
    #     # #     category__icontains = category[0]).order_by('-createdAt'))

    #     # #     remaing_products = list(Product.objects.filter(
    #     # #     name__icontains = ''))

    #     # #     for product in product1:
    #     # #         remaing_products.remove(product)

    #     # #     products  = product1 + remaing_products

    #     # if len(category) == 2:
    #     #     product1 = list(Product.objects.filter(
    #     #     category__icontains = category[0]).order_by('-createdAt'))  
    #     #     product2 = list(Product.objects.filter(
    #     #     category__icontains = category[1]).order_by('-createdAt'))

    #     #     remaing_products = list(Product.objects.filter(
    #     #     name__icontains = ''))

    #     #     for product in product1:
    #     #         remaing_products.remove(product)
            
    #     #     for product in product2:
    #     #         remaing_products.remove(product)

    #     #     products  = product1 + product2 + remaing_products


    #     if len(category) == 3:
    #         product1 = list(Product.objects.filter(
    #         category__icontains = category[0]).order_by('-createdAt'))
    #         product2 = list(Product.objects.filter(
    #         category__icontains = category[1]).order_by('-createdAt'))
    #         product3 = list(Product.objects.filter(
    #         category__icontains = category[2]).order_by('-createdAt'))


    #         remaing_products = list(Product.objects.filter(
    #         name__icontains = ''))

    #         for product in product1:
    #             remaing_products.remove(product)

    #         for product in product2:
    #             remaing_products.remove(product)
                
    #         for product in product3:
    #             remaing_products.remove(product)
            

    #         products  = product1 + product2 + product3 + remaing_products


    page = request.query_params.get('page')
    paginator = Paginator(products, 8)


    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user

    product = Product.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Producted Deleted Successfully!')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(_id=pk)
    data = request.data
    print(user)

    # 1 - Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'Product already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 - No Rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')



