#  orm models sqlalchemy

from application.database import db

class Admin(db.Model):
    __tablename__ = "admin"
    
    admin_username = db.Column(db.String(80), unique=True, primary_key=True, nullable=False)
    admin_password = db.Column(db.String(80), nullable=False)

    def to_json(self):
        return {"admin_username": self.admin_username,
                 "admin_password": self.admin_password}

class Client(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80), nullable=False)
    client_password = db.Column(db.String(80), nullable=False)
    client_address= db.Column(db.String(80))
    client_phone=db.Column(db.String(80))
    professionals = db.relationship('Professional', secondary='client_professional', backref='clients', cascade='all, delete')
    def to_json(self):
        professionals_json = []
        for professional in self.professionals:
            professional_json = professional.to_json()
            professionals_json.append(professional_json)
        return {"client_name": self.client_name,
                "client_password": self.client_password,
                "client_address": self.client_address,
                "client_phone": self.client_phone,
                "client_id": self.client_id, 
                "professionals": professionals_json
                }
    
class Professional(db.Model):
    __tablename__ = "professional"
    professional_id = db.Column(db.Integer, primary_key=True)
    professional_name = db.Column(db.String(80), nullable=False)
    professional_password = db.Column(db.String(80), nullable=False)
    professional_date_created = db.Column(db.String(80))
    professional_description = db.Column(db.String(80))
    professional_experience = db.Column(db.Integer)
    professional_rating = db.Column(db.Float , default=0)
    professional_service_type=db.Column(db.Integer, db.ForeignKey('service.service_id'))
    reviews = db.relationship('Review', backref='professional', lazy=True, cascade='all, delete')

   # clients = db.relationship('Client', secondary='client_professional', backref='professionals')

    def to_json(self):
        return {"professional_name": self.professional_name, 
                "professional_password": self.professional_password, 
                "professional_id": self.professional_id , 
                "professional_description": self.professional_description, 
                "professional_experience": self.professional_experience, 
                "professional_rating": self.professional_rating, 
                "professional_date_created": self.professional_date_created, 
                "professional_service_type": self.professional_service_type
               
                }
class Service(db.Model):
    __tablename__ = "service"
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(80), nullable=False)
    service_description = db.Column(db.String(80))
    service_time_required = db.Column(db.Integer)
    service_base_price = db.Column(db.Integer)
    def to_json(self):
        return {"service_name": self.service_name, 
                "service_description": self.service_description, 
                "service_id": self.service_id, 
                "service_time_required": self.service_time_required,
                "service_base_price": self.service_base_price
                }
    
class ServiceRequest(db.Model):
    __tablename__ = "service_request"
    service_request_id = db.Column(db.Integer, primary_key=True)
    service_request_date_of_request = db.Column(db.String(80), nullable=False)
    service_request_date_of_completion = db.Column(db.String(80))
    service_request_status = db.Column(db.String(80), nullable=False)
    service_request_remarks= db.Column(db.String(80))
    client_id= db.Column(db.Integer, db.ForeignKey('client.client_id'))
    service_id= db.Column(db.Integer, db.ForeignKey('service.service_id'))
    professional_id= db.Column(db.Integer, db.ForeignKey('professional.professional_id'))

    def to_json(self):
        return {"service_request_id":self.service_request_id,
                "service_request_date_of_request":self.service_request_date_of_request,
                "service_request_date_of_completion":self.service_request_date_of_completion,
                "service_request_status":self.service_request_status,
                "service_request_remarks":self.service_request_remarks,
                "client_id":self.client_id,
                "service_id":self.service_id,
                "professional_id":self.professional_id
                }

class Review(db.Model):
    __tablename__ = "review"
    review_id = db.Column(db.Integer, primary_key=True)
    review_rating = db.Column(db.Integer, nullable=False)
    review_comment= db.Column(db.String(80))
    client_id= db.Column(db.Integer, db.ForeignKey('client.client_id'))
    service_request_id= db.Column(db.Integer, db.ForeignKey('service_request.service_request_id'))
    professional_id= db.Column(db.Integer, db.ForeignKey('professional.professional_id'))

    def to_json(self):
        return {"review_id":self.review_id,
                "review_rating":self.review_rating,
                "review_comment":self.review_comment,
                "client_id":self.client_id,
                "service_request_id":self.service_request_id,
                "professional_id":self.professional_id
                }
    
class ClientProfessional(db.Model):
    __tablename__ = "client_professional"
    interaction_id = db.Column(db.Integer, primary_key=True)
    interaction_type = db.Column(db.String)
    interaction_date = db.Column(db.String)
    notes= db.Column(db.String)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.professional_id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))
  #  clients = db.relationship('Client', secondary='client_professional', backref='professionals')


    def to_json(self):
        return {"interaction_id":self.interaction_id,
                "interaction_type":self.interaction_type,
                "interaction_date":self.interaction_date,
                "notes":self.notes,
                "professional_id":self.professional_id,
                "client_id":self.client_id
            #    "clients": self.clients.to_json()
                }
    
class ServiceRequestHistory(db.Model):
    __tablename__ = "service_request_history"
    history_id= db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    timestamp = db.Column(db.String)
    remarks= db.Column(db.String)
    service_request_id= db.Column(db.Integer, db.ForeignKey('service_request.service_request_id'))
    service_request = db.relationship('ServiceRequest', backref='history', cascade='all, delete')

    def to_json(self):
        service_requests__json=[]
        for service_request in self.service_request:
            service_requests__json.append(service_request.to_json())
        return {"history_id":self.history_id,
                "status":self.status,
                "timestamp":self.timestamp,
                "remarks":self.remarks,
                "service_request_id":self.service_request_id,
                "service_requests":service_requests__json
                }