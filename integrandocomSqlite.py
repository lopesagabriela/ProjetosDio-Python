import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine, inspect, select, func,Numeric


Base = declarative_base()

class Cliente(Base):
    """
    Classe de Cliente a ser utilizada na aplicação 

    """
    __tablename__ = "cliente"
    # atributos
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String)
    fullname = Column(String)
    cpf = Column(String(9), unique = True)
    address = Column(String(30), unique = True)

    conta = relationship(
        "Conta", back_populates="cliente", cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"User(id= {self.id}, name= {self.name}, fullname= {self.fullname}, cpf= {self.cpf})"

class Conta(Base):
    """ Classe de Conta bancária a ser utilizada na aplicação 

    """
    __tablename__ = "conta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_account = (Column(String))
    agencia = (Column(String))
    numero = Column(Integer, unique=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    saldo = Column(Integer)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta (id={self.id}, Tipo_conta={self.type_account}, agencia={self.agencia}, numero={self.numero}) "
    
    

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

insp = inspect(engine)

with Session(engine) as session:
    cliente1 = Cliente(
        name = 'Carlos',
        fullname = 'Carlos Silva',
        cpf = '11111111111',
        address = 'carlossilva@mail.com',
        conta= [Conta(type_account="conta corrente", agencia = '0001', numero = 1000, saldo = 1500)]
               
    )
    cliente2 = Cliente(
        name = 'Maria',
        fullname = 'Maria Souza ',
        cpf = '22222222222',
        address = 'mariasouza@mail.com',
        conta= [Conta(type_account="conta corrente", agencia = '0001', numero = 1001, saldo = 12000)]
    )
    
    cliente3 = Cliente(
        name = 'Samara',
        fullname = 'Samara Silva',
        cpf = '33333333333',
        address = 'samarasilva@mail.com',
        conta= [Conta(type_account="poupanca", agencia = '0001', numero = 1002, saldo = 600)]
    )
    
    session.add_all([cliente1,cliente2,cliente3]) #enviando para o BD
    
    session.commit()
    
    
    stmt = select(Cliente).where(Cliente.name.in_(['Carlos','Samara']))
    
    for user in session.scalars(stmt):
        print(user)
        
# Recuperação de informações de maneira ordenada

order_stmt = select(Cliente).order_by(Cliente.fullname )
print("\n")
print(order_stmt)

print("Recuperando informações de maneira ordenada ")

for result in session.scalars(order_stmt):
    print(result)
    
join_stmt = select(Cliente.cpf,Conta.saldo).join_from(Conta,Cliente)

print("Operação de Joint: ")
for result in session.scalars(join_stmt):

    print(result)

connection = engine.connect()
results = connection.execute(join_stmt).fetchall()

print("Executando statment a partir da connection ")

for result in results:
    print(result)
    
    
