import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class GerenciadorFinancas:
    def __init__(self):
        self.arquivo_categorias = "categorias.json"
        self.arquivo_transacoes = "transacoes.json"
        self.categorias = self.carregar_categorias()
        self.transacoes = self.carregar_transacoes()
    
    def carregar_categorias(self) -> List[str]:

        if os.path.exists(self.arquivo_categorias):
            try:
                with open(self.arquivo_categorias, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def salvar_categorias(self):

        with open(self.arquivo_categorias, 'w', encoding='utf-8') as f:
            json.dump(self.categorias, f, ensure_ascii=False, indent=2)
    
    def carregar_transacoes(self) -> List[Dict]:

        if os.path.exists(self.arquivo_transacoes):
            try:
                with open(self.arquivo_transacoes, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def salvar_transacoes(self):

        with open(self.arquivo_transacoes, 'w', encoding='utf-8') as f:
            json.dump(self.transacoes, f, ensure_ascii=False, indent=2)
    
    def adicionar_categoria(self, categoria: str):

        categoria = categoria.strip()
        if categoria and categoria not in self.categorias:
            self.categorias.append(categoria)
            self.salvar_categorias()
            print(f"Categoria '{categoria}' adicionada com sucesso!")
        elif categoria in self.categorias:
            print("Esta categoria já existe!")
        else:
            print("Nome de categoria inválido!")
    
    def listar_categorias(self):

        if not self.categorias:
            print("Nenhuma categoria cadastrada.")
            return
        
        print("\nCategorias cadastradas:")
        for i, categoria in enumerate(self.categorias, 1):
            print(f"  {i}. {categoria}")
    
    def adicionar_transacao(self, tipo: str, valor: float, categoria: str, descricao: str = ""):
 
        if valor <= 0:
            print("O valor deve ser maior que zero!")
            return
        
        if categoria not in self.categorias:
            print(f"Categoria '{categoria}' não encontrada!")
            return
        
        transacao = {
            "id": len(self.transacoes) + 1,
            "tipo": tipo,
            "valor": valor,
            "categoria": categoria,
            "descricao": descricao,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mes": datetime.now().strftime("%Y-%m")
        }
        
        self.transacoes.append(transacao)
        self.salvar_transacoes()
        print(f" {tipo.capitalize()} de R$ {valor:.2f} registrada com sucesso!")
    
    def registrar_entrada(self):

        print("\n REGISTRAR ENTRADA")
        print("-" * 40)
        
        try:
            valor = float(input("Valor (R$): "))
            self.listar_categorias()
            categoria = input("Categoria: ").strip()
            descricao = input("Descrição (opcional): ").strip()
            
            self.adicionar_transacao("entrada", valor, categoria, descricao)
        except ValueError:
            print("Valor inválido!")
    
    def registrar_saida(self):

        print("\nREGISTRAR SAÍDA")
        print("-" * 40)
        
        try:
            valor = float(input("Valor (R$): "))
            self.listar_categorias()
            categoria = input("Categoria: ").strip()
            descricao = input("Descrição (opcional): ").strip()
            
            self.adicionar_transacao("saida", valor, categoria, descricao)
        except ValueError:
            print("Valor inválido!")
    
    def gerar_relatorio(self):

        print("\nRELATÓRIO DO MÊS")
        print("=" * 50)
        
        mes_atual = datetime.now().strftime("%Y-%m")
        transacoes_mes = [t for t in self.transacoes if t.get("mes") == mes_atual]
        
        if not transacoes_mes:
            print("enhuma transação registrada neste mês.")
            return
        
        total_entradas = sum(t["valor"] for t in transacoes_mes if t["tipo"] == "entrada")
        total_saidas = sum(t["valor"] for t in transacoes_mes if t["tipo"] == "saida")
        saldo = total_entradas - total_saidas
        
        print(f"\nMês: {datetime.now().strftime('%B/%Y')}")
        print(f"Total de Entradas: R$ {total_entradas:.2f}")
        print(f"Total de Saídas: R$ {total_saidas:.2f}")
        print(f"Saldo: R$ {saldo:.2f}")
        

        if total_saidas > 0:
            print("\nGastos por Categoria (Saídas):")
            saidas_por_categoria = {}
            for t in transacoes_mes:
                if t["tipo"] == "saida":
                    saidas_por_categoria[t["categoria"]] = saidas_por_categoria.get(t["categoria"], 0) + t["valor"]
            
            for categoria, valor in sorted(saidas_por_categoria.items(), key=lambda x: x[1], reverse=True):
                porcentagem = (valor / total_saidas) * 100
                print(f"  {categoria}: R$ {valor:.2f} ({porcentagem:.1f}%)")
        

        print("\nÚltimas transações:")
        for t in transacoes_mes[-5:]:
            tipo_emoji = "$" if t["tipo"] == "entrada" else "-"
            print(f"  {tipo_emoji} {t['data'][:10]} - {t['categoria']}: R$ {t['valor']:.2f}")
            if t.get("descricao"):
                print(f" {t['descricao']}")
    
    def menu_principal(self):

        while True:
            print("\n" + "=" * 50)
            print("SISTEMA DE FINANÇAS PESSOAIS")
            print("=" * 50)
            print("1. Gerenciar Categorias")
            print("2. Registrar Entrada")
            print("3. Registrar Saída")
            print("4. Ver Relatório do Mês")
            print("5. Sair")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.menu_categorias()
            elif opcao == "2":
                self.registrar_entrada()
            elif opcao == "3":
                self.registrar_saida()
            elif opcao == "4":
                self.gerar_relatorio()
            elif opcao == "5":
                print("\nObrigado por usar o sistema de finanças pessoais!")
                break
            else:
                print("Opção inválida! Tente novamente.")
    
    def menu_categorias(self):

        while True:
            print("\nGERENCIAR CATEGORIAS")
            print("-" * 40)
            print("1. Ver categorias")
            print("2. Adicionar categoria")
            print("3. Voltar ao menu principal")
            print("-" * 40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.listar_categorias()
            elif opcao == "2":
                categoria = input("Nome da nova categoria: ").strip()
                self.adicionar_categoria(categoria)
            elif opcao == "3":
                break
            else:
                print("Opção inválida! Tente novamente.")

def main():


    if not os.path.exists("dados"):
        os.makedirs("dados")
    

    os.chdir("dados")
    
    app = GerenciadorFinancas()
    

    if not app.categorias:
        categorias_padrao = [
            "Alimentação", "Transporte", "Moradia", "Saúde",
            "Educação", "Lazer", "Salário", "Investimentos"
        ]
        for cat in categorias_padrao:
            app.adicionar_categoria(cat)
        print("Categorias padrão adicionadas!")
    
    app.menu_principal()

if __name__ == "__main__":
    main()
