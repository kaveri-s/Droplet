import random
s=4
p=3
for name in ['Lina','Ursa','Luna','Kunkka','Abaddon','Axe','Bane','Clark','Kent','Lich','Harley','Mirana']:
    choice = random.choice(['prof','student'])
    if(choice[0]=='s'):
        if s>9:
            id = 'S0'+str(s)
        else:
            id = 'S00'+str(s)
        s+=1
    else:
        if p>9:
            id = 'P0'+str(p)
        else:
            id = 'P00'+str(p)
        p+=1
    print('insert into user values("'+id+'", "'+name+'" , "'+name+'@gmail.com" , "'+name+'" , "'+choice+'");')