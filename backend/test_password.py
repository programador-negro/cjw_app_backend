from passlib.context import CryptContext

# Configuración del hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash almacenado en la base de datos
stored_hash = "$2b$12$tGZZqZqz5kFTaZW6RzGU8e9MyZIzNiPWR/qr4/R/UTzwbDXdQHNcS"

# Función para verificar la contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Prueba una contraseña
def test_password(password: str):
    result = verify_password(password, stored_hash)
    print(f"Contraseña: {password}")
    print(f"¿Coincide?: {'Sí' if result else 'No'}")
    print("-" * 30)

# Pruebas
test_password("admin123")  # La contraseña que creemos que es
test_password("admin")     # Una prueba incorrecta
test_password("123456")    # Otra prueba incorrecta

# Permitir probar más contraseñas interactivamente
while True:
    test = input("\nIngresa una contraseña para probar (o 'q' para salir): ")
    if test.lower() == 'q':
        break
    test_password(test)