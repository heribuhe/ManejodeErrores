from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()




class Juego(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Juego {self.nombre}>'


        

    