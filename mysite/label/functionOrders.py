from .models import  Order, Factory
from .client.clientType import CWR

def checkFactoryApproval(allOrders):
    for order in allOrders:
        if order.factory.requirements == False:
            order.factoryApproval = True
            order.save()

def checkClientApproval(allOrders):
    for order in allOrders:
        for element in CWR:
            if element in order.description:
                order.clientApproval = True
                order.save()