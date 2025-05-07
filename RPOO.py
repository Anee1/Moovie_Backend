########### Class ############
#%%
class chien:
    pass
#%%
mon_chien = chien()
print(type(mon_chien))
# %%
class homme:
    def __init__(self, nom , fonction, age):
        self.nom = nom,
        self.fonction = fonction,
        self.age = age

    def signer(self):
        si = self.nom + self.fonction
        return si 
#%%
ressource = homme('Marcel', 'Actuaire', 30)


# %%
type(ressource)
# %%
ressource.fonction
# %%
ressource.age
# %%
ressource.signer()
# %%
class calculator:


    def __init__(self, a, b):
        if not isinstance(a ,(int ,float)) or not isinstance(b , (int , float)):
            raise TypeError('Les valeurs doivent etre des entier ou reel.')
        self.a = a
        self.b = b 
        
    def add(self):
        return self.a + self.b
        
    def multiply(self):
        return self.a * self.b
# %%
valeur = calculator(3,5)
# %%
valeur.add()
# %%
