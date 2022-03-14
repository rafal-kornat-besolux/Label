


def factories_specifications(self,package):

    factory_name = self.order[-3:]

    if factory_name == "":
        pass
    elif factory_name == "BEX":
        if package.orderProduct.order.factory_info != None:
            self.factory_details = 1
    elif factory_name == "CHX":
       if package.orderProduct.order.factory_info != None:
            self.factory_details = 1
    elif factory_name == "GAL":
        if package.orderProduct.order.factory_info != None:
            self.factory_details = 1
        # self = factories_specifications_GAL(self)
    elif factory_name == "MOD": #and self.order[:3] !="SAV":
       if package.orderProduct.order.factory_info != None:
            self.factory_details = 1
    elif factory_name == "KAL":
        pass
        # self = factories_specifications_KAL(self)
    elif factory_name=="DAS":
        self.factory_details = 1
        # self = factories_specifications_DAS(self)
    elif factory_name=="DOL":
        pass
        # self = factories_specifications_DOL(self)
    else:
        self.factory_details = 1

    return self