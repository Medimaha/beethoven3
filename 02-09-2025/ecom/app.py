from product_manager import create_product,read_all,read_by_id
from product_manager import update,delete_by_id
from product import Product

def menu():
    message='''
     1-Create product
     2-Read All Products
     3-Read By id
     4-Update
     5-Delete
     6-Exit/Logout
     Enter Your choice:
    '''
    choice = int(input(message))
    if choice == 1:
        name=input('Name:')
        description=input('description:')
        category=input('Category:')
        tags=input('Tags:')
        stock=int(input('stock:'))
        price=int(input('price:'))
        id=-1

        product=Product(id,name,description,category,tags,stock,price)

        create_product(product)
        print('product created successfully...')
    elif choice==2:
          products=read_all()
          print('products are :')
          for product in products:
             print(product )
    elif choice ==3:
          id = int(input('search product ID'))
          product=read_by_id(id)
          if product == None:
           print('product is not found')
          else:
           print('product is not found')
    elif choice ==4:
        
        id=int(input('ID:'))
        old_product=read_by_id(id)
        if old_product == None:
            print('product not found')
        else:

          print(old_product)
          name=input('Name:')
          description=input('description:')
          category=input('Category:')
          tags=input('Tags:')
          stock=int(input('stock:'))
          price=int(input('price:'))

          new_product=product(id,name,description,category,tags,stock,price)
          update(new_product)

          print("product updated successfully....")

    elif choice == 5:
         
        id = int(input('ID:'))
        old_product=read_by_id(id)
        if old_product == None:
            print('product not found')
        else:
         
           print('old_product')
           if input('Are you sure to delete(Y/N)?') == 'y':
               delete_by_id(id)
               print('product Deleted Successfully....')
    return choice
   
   

def menu_provider():
    print("product Management App")
    choice=menu()
    while choice!=6:
        choice=menu()
    print("Thank yo for using App")

menu_provider()
