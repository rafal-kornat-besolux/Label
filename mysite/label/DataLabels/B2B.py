def function_B2B(description):
        if case_basic(description)!=False:
            description=case_basic(description)
        else: 
            description = False

        return description

def case_basic(value):
    set = ["IN&OUT DESIGN", "GALAXUS", "DECOVRY", "ART-STYLE", "L&F", 
    "SETTIMO", "STK: BONAMI", "BONAMI","Mezoni","DESIGN_AG", 
    "VIVRE_RO", "MYSTORE", "VEMZU", "PIGU", "MUZZA", "10DX",
    "NAPRIJED", "AIO_LIVING", "CRISTINA POPESCU","SPECIAL EVENTS",
    "LIMANGO","MEZONI","INTELLIGENT DESIGN"]
    
    for i in set:
        if i in value:
            return value
        
    return False