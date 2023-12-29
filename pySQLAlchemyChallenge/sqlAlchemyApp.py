"""
    I am implementing an integration application with SQLite based on a relational schema provided by the challenge
    creator.
    These classes will represent the relational database tables within the application.

    programmed by: Kaíque Freire
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Float
)

from sqlalchemy.orm import (
    Session,
    declarative_base,
    relationship
)

# Criando uma engine para o banco de dados
engine = create_engine("sqlite://")

Base = declarative_base()  # Usando o declarative_base para fazer o mapeamento


class Client(Base):
    __tablename__ = "client"  # Nome da tabela

    id = Column(Integer, primary_key=True)  # Chave primária da tabela
    name = Column(String(40), nullable=False)  # Não pode ser nulo
    cpf = Column(String(9), nullable=False)
    address = Column(String(9))

    accounts = relationship("Account", backref="client", cascade="all, delete-orphan")  # Relação com a tabela Account

    """
    backref="client" cria um atributo client na classe Account. Este atributo permite que você acesse o objeto Client 
    associado a uma instância Account.
    
    cascade="all, delete-orphan" garante que todas as operações realizadas em um objeto Client 
    (como salvar, excluir ou atualizar) também sejam aplicadas aos objetos Account associados.
    
    """

    def __repr__(self):
        """
        Returns a string representation of the Client object, suitable for debugging and logging.

        The string includes the following information about the client:
        - ID: The unique identifier of the client.
        - Name: The client's name.
        - CPF: The client's CPF (Cadastro de Pessoa Física).
        - Address: The client's address.

        :return:
            str: A string representation of the Client object.
        """

        return f"client (id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address})"


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    agency = Column(String, nullable=False)
    num = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    balance = Column(Float)

    def __repr__(self):
        """
        Returns a string representation of the Account object, suitable for debugging and logging.

        The string includes the following information about the account:
        - ID: The unique identifier of the account.
        - Type: The type of account (e.g., "corrente", "poupança").
        - Agency: The account's agency number.
        - Number: The account's number.
        - Balance: The account's balance.

        :return:
            str: A string representation of the Account object.
        """

        return f"Account(id={self.id}, type={self.type}, agency={self.agency}, num={self.num}, balance={self.balance})"


# Criando as tabelas no banco de dados

Base.metadata.create_all(engine)

# Criando clientes

with Session(engine) as session:

    cliente_kaique = Client(
        name='Kaique Freire',
        cpf='785214569',
        address='Rua 3 Sta H',
        accounts=[Account(type="corrente", agency="3210-9", num=987654, balance=0.0),
                  Account(type="poupança", agency="6543-2", num=654321, balance=500.0)]
    )

    cliente_maria = Client(
        name='Maria Clara',
        cpf='745320168',
        address='Rua 8 J Paz',
        accounts=[Account(type="corrente", agency="9658-7", num=8452179, balance=0.0)]
    )

    cliente_victor = Client(name="Victor Peixoto", cpf="32109876543", address="Rua 20, 200")

    session.add_all([cliente_kaique, cliente_maria, cliente_victor])  # persistência de dados

    session.commit()  # Marca o fim da transação e envia para o DB

# Imprimindo todos os clientes
print("\nTodos os clientes:")
for client in session.query(Client).all():
    print(client)

# Imprimindo um cliente específico
cliente_id = 2  # Substitua pelo ID desejado
cliente = session.get(Client, cliente_id)
print(f"\nCliente com ID {cliente_id}:")
print(cliente)

# Imprimindo contas de um cliente específico
cliente_nome = "Maria Clara"  # Substitua pelo nome desejado
cliente = session.query(Client).filter_by(name=cliente_nome).first()
print(f"\nContas do cliente {cliente_nome}:")
for account in cliente.accounts:
    print(account)

# Imprimindo clientes com saldo zero em alguma conta
print("\nClientes com saldo zero em alguma conta:")
for client in session.query(Client).join(Account).filter(Account.balance == 0).all():
    print(client)

