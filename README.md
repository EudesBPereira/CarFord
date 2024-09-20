# CarFord

## Descrição

O CarFord é um sistema de gerenciamento de veículos desenvolvido com Flask, Docker e um banco de dados SQL. Este aplicativo permite que os usuários gerenciem informações sobre clientes e seus veículos de forma eficiente, oferecendo funcionalidades como:

- **Registro de Clientes**: Adicionar, visualizar, atualizar e excluir informações dos clientes.
- **Gerenciamento de Veículos**: Cada cliente pode ter até 3 veículos registrados, com informações detalhadas sobre cada veículo, incluindo cor e modelo.
- **Oportunidade de Venda**: Clientes podem ser marcados como oportunidades de venda, permitindo uma melhor gestão do relacionamento com o cliente.
- **Segurança**: O sistema implementa autenticação e autorização usando JWT para proteger as rotas da API.

## Tecnologias Utilizadas

- Flask
- Docker
- SQLAlchemy
- Azure SQL
- Flask-JWT-Extended

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/EudesBPereira/CarFord.git
