from app import create_app

# Crear la aplicación usando la función create_app
app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación en el puerto 5000 (por defecto)
    app.run(debug=True)
