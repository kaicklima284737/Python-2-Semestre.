import random
from profissoes import novas_profissoes
from nomes import novos_nomes

lista_usuarios = []
for n in range(1000):
    for nome in novos_nomes:
        idade = random.randint(17, 80)
        money = random.randint(-5000, 200000)

        novo_usuario = {
            "nome": nome,
            "profissao": random.choice(novas_profissoes),
            "idade": idade,
            "saldo R$": f"{money:.2f}",
        }
        lista_usuarios.append(novo_usuario)