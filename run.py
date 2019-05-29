from app import app , db 

if __name__ == "__main__":
    db.create_all()
    app.run(host= '0.0.0.0')    