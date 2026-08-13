"""
#Teste de Matriz para Ecommerce, 1 teste.

catalogo = [
    ["Camiseta Azul", 59.90, 120, [38,40,42,44]],
    ["Tênis Runner", 199.90, 40, [38,40,42,44]],
]

print(f"{catalogo[0][1]} - {catalogo[0][2]} - {catalogo[0][3][0]}")
print(f"Produto: {catalogo[0][0]}\nEstoque: {catalogo[0][2]}\nPreço: {catalogo[0][1]}")
"""
# Eccomerce Básico.
def cadastrar_produto(catalogo, nome,preco,estoque):
    produto = [nome,preco,estoque]
    catalogo.append(produto)
    return catalogo

def exibir_catalogo(catalogo):
    for produto in catalogo:
        print(f"{produto[0]} - R${produto[1]:.2f} - estoque: ({produto[2]})")

if __name__ == '__main__':
    novos_produtos = []
    novos_produtos = cadastrar_produto(novos_produtos, 'Camiseta Azul', 79.99, 100)
    novos_produtos = cadastrar_produto(novos_produtos, 'Tênis Runner', 199.90, 40)
    novos_produtos = cadastrar_produto(novos_produtos, 'Boné Preto', 39.90, 50)
    exibir_catalogo(novos_produtos)
