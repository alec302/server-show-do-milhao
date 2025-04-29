from app import create_app

app = create_app()

if __name__ == "__main__":
    # usa o DEBUG vindo das configs
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
