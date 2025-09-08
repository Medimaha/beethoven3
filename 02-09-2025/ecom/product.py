#id,name,description,category,stock,tags,price
#data  science-->form some LMS_model of data 
#data analyst --> the given job will be given by 
#data enginner-->all the insidents will be used by enginner
#product enginner-->
#product analyst-->making more anlysing in the products
#software analyst-->those who are using software develops

class Product:
    def __init__ (self,id,name,description,category,tags,stocks,price):
        self.id=id
        self.name=name
        self.description=description
        self.category=category
        self.tags=tags
        self.stocks=stocks
        self.price=price
    def __str__(self):
        return f'[id={self.id},name={self.name},description={self.description},category={self.category},tags={self.tags},stocks={self.stocks},price={self.price}]'
    def __repr__(self):
        return self.__str__()
'''mobile_vivo = Product(1001, 'Vivo Y22','good in camera.','mobile','electronics,smart phone,Andriod mobile',10,21000)
mobile_samsung = Product(1002, 'S24',description='good in camera.',category='mobile',tags='electronics,smart phone,Andriod mobile',stocks=10,price=120000)
print(mobile_vivo)
print(mobile_samsung)
'''