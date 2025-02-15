from flask import current_app as app, request , Response
from application.models import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime  
from flask import jsonify
from flask import Blueprint, request
from application.cache import cache

routers = Blueprint('routers', __name__)
# /service-request
@app.route("/admin_login", methods=["POST"])
def admin_login():
    print("admin_login endpoint hit")  # Check if the endpoint is reached

    data = request.get_json()
    print(data)
    # Ensure the request contains the expected keys
    if not data or "admin_username" not in data or "admin_password" not in data:
        return {"message": "Missing credentials"}, 400
    

    admin_username = data["admin_username"]
    admin_password = data["admin_password"]
    # Query by primary key
    
    admin_from_db = Admin.query.get(admin_username)
    # Check credentials
    if admin_from_db and admin_from_db.admin_password == admin_password:
        
        token = create_access_token(identity=admin_username, additional_claims={"type": "admin"})

        return {"access_token": token}, 200
    
    return {"message": "invalid  credentials"}, 401

# @app.route("/admin_dashboard", methods=["GET", "POST"])
# @jwt_required()
# def admin_dashboard():
#     professions=Professional.query.all()
#     clients=Client.query.all()
#     services=Service.query.all()
#     ServiceRequests=ServiceRequest.query.all()

#     json_response_clients=[]
#     for client in clients:
#         json_response_clients.append(client.to_json())

#     json_response_services=[]
#     for service in services:
#         json_response_services.append(service.to_json())

#     json_response_service_requests=[]
#     for service_request in ServiceRequests:
#         json_response_service_requests.append(service_request.to_json())

#     json_respons=[]
#     for profession in professions:
#         json_respons.append(profession.to_json())
#     return {"profession":json_respons,"clients":json_response_clients,"services":json_response_services,"serviceRequests":json_response_service_requests}, 200

@app.route("/admin_dashboard", methods=["GET"])
@jwt_required()
@cache.memoize(timeout=50)
def admin_dashboard():
    services = Service.query.all()
    
    # Fetch all professionals
    professionals = Professional.query.all()
    
    # Group professionals by their service type (professional_service_type)
    service_professionals = {service.service_id: [] for service in services}
    
    # Assign professionals to their respective services
    for professional in professionals:
        service_id = professional.professional_service_type
        if service_id in service_professionals:
            service_professionals[service_id].append(professional.to_json())

    # Prepare the final response by adding professionals to each service
    service_data = []
    for service in services:
        service_json = service.to_json()
        service_json['professionals'] = service_professionals.get(service.service_id, [])
        service_data.append(service_json)

    return jsonify({"services": service_data})

 # Flask route for fetching professionals
@app.route('/professionals', methods=['GET'])
def get_professionals():
    try:
        professionals = Professional.query.all()
        professionals_data = [prof.to_json() for prof in professionals]
        return jsonify({"professionals": professionals_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin_new_service", methods=["POST"])
@jwt_required()
def admin_new_service():
    data = request.get_json()
    if not data or 'service_name' not in data or 'service_description' not in data or 'service_base_price' not in data:
        return {"message": "All feilds are required"}, 400
    
    service_name = data["service_name"]
    service_description = data["service_description"]
    service_base_price = data["service_base_price"]

    service_from_db = Service.query.filter_by(service_name=service_name).first()
    if service_from_db:
        return {"message": "Service already exists"}, 400
    
    service = Service(service_name=service_name, service_description=service_description, service_base_price=service_base_price)
    db.session.add(service)
    db.session.commit()
    return {"message": "Service created successfully"}, 200

@app.route("/admin_search", methods=["POST"])
@jwt_required()
def admin_search():

    
    # Get the search par
    # ameters from the request
    data = request.get_json()
    search_query = data.get("search_query", "")
    search_type = data.get("search_type", "")  # could be "client", "professional", or "service"
    status = data.get("status", "")  # optional: "open", "closed", etc.

    # Ensure search_type is provided
    if not search_type:
        return {"message": "Please provide a search type (client, professional, service)"}, 400

    # Searching based on the search_type
    if search_type == "client":
        query = Client.query
        if search_query:
            query = query.filter(Client.client_name.ilike(f"%{search_query}%"))
        if status:
            query = query.filter(Client.client_status.ilike(f"%{status}%"))
        results = query.all()
        json_results = [client.to_json() for client in results]

    elif search_type == "professional":
        query = Professional.query
        if search_query:
            query = query.filter(Professional.professional_name.ilike(f"%{search_query}%"))
        if status:
            query = query.filter(Professional.service_status.ilike(f"%{status}%"))
        results = query.all()
        json_results = [professional.to_json() for professional in results]

    elif search_type == "service":
        query = Service.query
        if search_query:
            query = query.filter(Service.service_name.ilike(f"%{search_query}%"))
        if status:
            query = query.filter(Service.service_status.ilike(f"%{status}%"))
        results = query.all()
        json_results = [service.to_json() for service in results]

    else:
        return {"message": "Invalid search type"}, 400

    # Check if no results found
    if not json_results:
        return {"message": "No results found"}, 404

    return {"results": json_results}, 200


# @app.route("/client_login", methods=["POST"])
# def client_dashboard():
#     data = request.get_json()
#     if not data or 'client_name' not in data or 'client_password' not in data:

#         return {"message": "client_name and client_password are required"}, 400
#     client_name = data["client_name"]
#     client_password = data["client_password"]
#     client_from_db = Client.query.filter_by(client_name=client_name).first()


#     if client_from_db and client_from_db.client_password == client_password:
#         token = create_access_token(identity=client_name, additional_claims={"type": "client"})
#         return {"access_token": token}, 200
#     return {"message": "invalid credentials"},401  delete_professiona


from werkzeug.security import generate_password_hash

@app.route('/professional_signup', methods=['POST'])
def professional_signup():
    data = request.get_json()

    # Get the data from the request
    professional_name = data.get('professional_name')
    professional_password = data.get('professional_password')
    professional_description = data.get('professional_description')
    professional_experience = data.get('professional_experience')

    # Hash the password before storing it
    hashed_password = generate_password_hash(professional_password)

    # Create a new professional instance
    new_professional = Professional(
        professional_name=professional_name,
        professional_password=hashed_password,
        professional_description=professional_description,
        professional_experience=professional_experience
    )

    # Add the new professional to the database
    db.session.add(new_professional)
    db.session.commit()

    # Return the created professional with a professional_id
    return jsonify({
        'professional_id': new_professional.professional_id,
        'professional_name': new_professional.professional_name,
    })




@app.route('/client_signup', methods=['POST'])
def client_signup():
    data = request.get_json()

    # Get the data from the request
    client_name = data.get('client_name')
    client_password = data.get('client_password')
    client_address = data.get('client_address')
    client_phone = data.get('client_phone')

    # Create a new client
    new_client = Client(
        client_name=client_name,
        client_password=client_password,
        client_address=client_address,
        client_phone=client_phone
    )

    # Add to database
    db.session.add(new_client)
    db.session.commit()

    # Return the created client with a client_id
    return jsonify({
        'client_id': new_client.client_id,
        'client_name': new_client.client_name,
    })


# @app.route("/client_login", methods=["POST"])
# def client_login():
#     data = request.get_json()
    
#     if not data or 'client_name' not in data or 'client_password' not in data:
#         return {"message": "client_name and client_password are required"}, 400

#     client_name = data["client_name"]
#     client_password = data["client_password"]
    
#     client_from_db = Client.query.filter_by(client_name=client_name).first()

#     if client_from_db and client_from_db.client_password == client_password:
#         # Create a JWT token
#         token = create_access_token(identity=client_name, additional_claims={"type": "client"})
        
#         # Return the access token and client_id
#         return {
#             "access_token": token,
#             "client_id": client_from_db.client_id  # Assuming `id` is the field for the client ID
#         }, 200

#     return {"message": "invalid credentials"}, 401

@app.route("/client_register", methods=["POST"])
def client_register():
    data = request.get_json()
    if not data or 'client_name' not in data or 'client_password' not in data  or 'client_address' not in data  or 'client_phone' not in data:

        return {"message": "All fields are required"}, 400
    
    client_name = data["client_name"]
    client_password = data["client_password"]
    client_address = data["client_address"]
    client_phone = data["client_phone"]

    client_from_db = Client.query.filter_by(client_name=client_name).first()
    if client_from_db:
        return {"message": "client already exists"}, 400
    
    new_client = Client(client_name=client_name, client_password=client_password, client_address=client_address, client_phone=client_phone)
    db.session.add(new_client)
    db.session.commit()
    return {"message": "client created successfully"}, 201


@app.route("/professional_register", methods=["POST"])
def professional_register():
    data = request.get_json()
    if not data or 'professional_name' not in data or 'professional_password' not in data  or 'professional_date_created' not in data  or 'professional_description' not in data or 'professional_experience' not in data  or 'professional_service_type' not in data:

        return {"message": "All fields are required"}, 400
    
    professional_name = data["professional_name"]
    professional_password = data["professional_password"]
    professional_date_created = data["professional_date_created"]
    professional_description = data["professional_description"]
    professional_experience = data["professional_experience"]
    professional_service_type = data["professional_service_type"]
    


    professional_from_db = Professional.query.filter_by(professional_name=professional_name).first()
    if professional_from_db:
        return {"message": "professional already exists"}, 400
    
    new_professional = Professional(professional_name=professional_name, professional_password=professional_password, professional_date_created=professional_date_created, professional_description=professional_description, professional_experience=professional_experience, professional_service_type=professional_service_type)
    db.session.add(new_professional)
    db.session.commit()
    return {"message": "professional created successfully"}, 201


 

#delete_professional
@app.route('/get_professionals_list', methods=['GET'])
def get_professionals_list():
    professionals = Professional.query.all()
    return jsonify([prof.to_json() for prof in professionals])




@app.route("/professional_home_page", methods=["GET"])
@jwt_required()
def professional_home_page():


    professional_name = get_jwt_identity()
    professional = Professional.query.filter_by(professional_name=professional_name).first()
    if not professional:
        return {"message": "Professional not found"}, 404

    # Fetch all pending service requests for the professional
    pending_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional.professional_id,
        ServiceRequest.service_request_status == "pending"
    ).all()

    # Fetch all selected service requests for the professional
    selected_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional.professional_id,
        ServiceRequest.service_request_status == "selected"
    ).all()

    # Fetch all rejected service requests for the professional
    rejected_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional.professional_id,
        ServiceRequest.service_request_status == "rejected"
    ).all()

    # Convert service requests to JSON format
    def requests_to_json(requests):
        result = []
        for req in requests:
            client = Client.query.get(req.client_id)
            if client:
                result.append({
                    "service_request_id": req.service_request_id,
                    "service_request_date_of_request": req.service_request_date_of_request,
                    "service_request_date_of_completion": req.service_request_date_of_completion,
                    "service_request_status": req.service_request_status,
                    "service_request_remarks": req.service_request_remarks,
                    "client_name": client.client_name,
                    "client_contact": client.client_phone,
                    "client_address": client.client_address
                })
        return result

    response = {
        "pending_requests": requests_to_json(pending_requests),
        "selected_requests": requests_to_json(selected_requests),
        "rejected_requests": requests_to_json(rejected_requests)
    }

    return (response), 200

@app.route("/professional_search", methods=["POST"])
@jwt_required()
def professional_search():
    data=request.get_json()
    search_query = data.get("search_query", "").strip()
    location = data.get("location", "").strip()
    address = data.get("address", "").strip()
    status = data.get("status", "").strip()
    professional_name = get_jwt_identity()
    professional = Professional.query.filter_by(professional_name=professional_name).first()
    if not professional:
        return {"message": "Professional not found"}, 404
    service_requests = ServiceRequest.query.filter_by(professional_id=professional.professional_id).all()
    client_ids = {req.client_id for req in service_requests}
    query = Client.query.filter(Client.client_id.in_(client_ids))

    if search_query:
        query = query.filter(Client.client_name.ilike(f"%{search_query}%"))
    if location:
        query = query.filter(Client.client_address.ilike(f"%{location}%"))
    if address:
        query = query.filter(Client.client_address.ilike(f"%{address}%"))
    
    results = query.all()
    
    # Convert clients to JSON format
    def clients_to_json(clients):
        result = []
        for client in clients:
            result.append({
                "client_name": client.client_name,
                "client_contact": client.client_phone,
                "client_address": client.client_address
            })
        return result

    json_results = clients_to_json(results)

    # Check if no results found
    if not json_results:
        return {"message": "No results found"}, 404

    return {"results": json_results}, 200



# @app.route("/client_dashboard", methods=["GET", "POST"])
# @jwt_required()
# def client_home_page():
#     client_name = get_jwt_identity()

#     # Fetch client record
#     client = Client.query.filter_by(client_name=client_name).first()
#     if not client:
#         return {"message": "Client not found"}, 404

#     if request.method == "POST":
#         # Handle search for professionals
#         data = request.get_json()
#         service_name = data.get("service_name", "")
#         search_query = data.get("search_query", "")

#         if not service_name:
#             return {"message": "Service name is required for searching professionals"}, 400
        
#         service = Service.query.filter_by(service_name=service_name).first()
#         if not service:
#             return {"message": "Service not found"}, 404

#         # Fetch professionals based on the service_name
#         service_id = service.service_id

#         # Fetch professionals based on the service_id
#         professionals_query = Professional.query.filter_by(professional_service_type=service_id)

#         if search_query:
#             professionals_query = professionals_query.filter(Professional.professional_name.ilike(f"%{search_query}%"))

#         professionals = professionals_query.all()

#         def professionals_to_json(professionals):
#             result = []
#             for prof in professionals:
#                 result.append({
#                     "professional_id": prof.professional_id,
#                     "professional_name": prof.professional_name,
#                     "professional_description": prof.professional_description,
#                     "professional_experience": prof.professional_experience
#                 })
#             return result

#         json_professionals = professionals_to_json(professionals)
#         return {"professionals": json_professionals}, 200

#     # Handle GET request to fetch all available services
#     services = Service.query.all()

#     def services_to_json(services):
#         result = []
        

#         for service in services:
#             result.append({
#                 "service_name": service.service_name, 
#                 "service_description": service.service_description, 
#                 "service_id": service.service_id, 
#                 "service_time_required": service.service_time_required,
#                 "service_base_price": service.service_base_price
#             })
#         return result
#     json_services = services_to_json(services)

#     ServiceRequests=ServiceRequest.query.all()
#     json_response_service_requests=[]
#     for service_request in ServiceRequests:
#         json_response_service_requests.append(service_request.to_json())

#     professions=Professional.query.all()
#     json_respons=[]
#     for profession in professions:
#         json_respons.append(profession.to_json())
    
#     clients=Client.query.all()
#     json_response_clients=[]
#     for client in clients:
#         json_response_clients.append(client.to_json())

    

#     return {"profession":json_respons,"clients":json_response_clients,"services":json_services,"serviceRequests":json_response_service_requests}, 200

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route("/client_<service_name>", methods=["GET", "POST"])
@jwt_required()
def client_service_page(service_name):
    client_name = get_jwt_identity()
    
    # Fetch client record
    client = Client.query.filter_by(client_name=client_name).first()
    if not client:
        return jsonify({"message": "Client not found"}), 404

    # Fetch the service
    service = Service.query.filter_by(service_name=service_name).first()
    if not service:
        return jsonify({"message": "Service not found"}), 404

    service_id = service.service_id

    if request.method == "POST":
        data = request.get_json()
        professional_id = data.get("professional_id")

        if not professional_id:
            return jsonify({"message": "Professional ID is required to book the service"}), 400

        # Check if the professional is available for the selected service
        professional = Professional.query.filter_by(professional_id=professional_id, professional_service_type=service_id).first()
        if not professional:
            return jsonify({"message": "Professional not available for the selected service"}), 400

        # Create a new service request
        new_request = ServiceRequest(
            client_id=client.client_id,
            professional_id=professional_id,
            service_id=service_id,
            service_request_status="pending",
            service_request_date_of_request=datetime.utcnow()
        )
        db.session.add(new_request)
        db.session.commit()

        return jsonify({"message": "Service booked successfully"}), 201

    # Handle GET request to fetch all available professionals for the selected service
    professionals = Professional.query.filter_by(professional_service_type=service_id).all()

    def professionals_to_json(professionals):
        result = []
        for prof in professionals:
            result.append({
                "professional_id": prof.professional_id,
                "professional_name": prof.professional_name,
                "professional_description": prof.professional_description,
                "professional_experience": prof.professional_experience
            })
        return result

    json_professionals = professionals_to_json(professionals)

    # Fetch previously booked services
    booked_requests = ServiceRequest.query.filter_by(client_id=client.client_id, service_id=service_id).all()

    def booked_requests_to_json(requests):
        result = []
        for req in requests:
            professional = Professional.query.get(req.professional_id)
            if professional:
                result.append({
                    "service_request_id": req.service_request_id,
                    "professional_name": professional.professional_name,
                    "service_request_date_of_request": req.service_request_date_of_request,
                    "service_request_date_of_completion": req.service_request_date_of_completion,
                    "service_request_status": req.service_request_status
                })
        return result

    json_booked_requests = booked_requests_to_json(booked_requests)

    response = {
        "available_professionals": json_professionals,
        "booked_requests": json_booked_requests
    }

    return jsonify(response), 200


@app.route("/client_booked_services", methods=["GET", "POST"])
@jwt_required()
def client_booked_services():
    client_name = get_jwt_identity()

    client = Client.query.filter_by(client_name=client_name).first()
    if not client:
        return jsonify({"message": "Client not found"}), 404

    if request.method == "POST":
        data = request.get_json()
        service_request_id = data.get("service_request_id")
        new_status = data.get("new_status")

        if not service_request_id or not new_status:
            return jsonify({"message": "service_request_id and new_status are required"}), 400

        service_request = ServiceRequest.query.get(service_request_id)
        if not service_request:
            return jsonify({"message": "Service request not found"}), 404

        if service_request.client_id != client.client_id:
            return jsonify({"message": "Unauthorized to update this service request"}), 403

        service_request.service_request_status = new_status
        if new_status == "completed":
            service_request.service_request_date_of_completion = datetime.utcnow()
        db.session.commit()

        # Redirect to review page
        professional = Professional.query.get(service_request.professional_id)
        if professional:
            return jsonify({"redirect_url": f"/{professional.professional_name}_review"}), 200

        return jsonify({"message": "Professional not found"}), 404

    booked_requests = ServiceRequest.query.filter_by(client_id=client.client_id).filter(
        ServiceRequest.service_request_status.in_(["pending", "completed"])
    ).all()

    def booked_requests_to_json(requests):
        result = []
        for req in requests:
            professional = Professional.query.get(req.professional_id)
            if professional:
                result.append({
                    "service_request_id": req.service_request_id,
                    "professional_name": professional.professional_name,
                    "service_request_date_of_request": req.service_request_date_of_request,
                    "service_request_date_of_completion": req.service_request_date_of_completion,
                    "service_request_status": req.service_request_status
                })
        return result

    json_booked_requests = booked_requests_to_json(booked_requests)

    response = {
        "booked_requests": json_booked_requests
    }

    return jsonify(response), 200



# client-details


@app.route("/<professional_name>_review", methods=["GET", "POST"])
@jwt_required()
def professional_review(professional_name):
    client_name = get_jwt_identity()

    # Fetch client record
    client = Client.query.filter_by(client_name=client_name).first()
    if not client:
        return jsonify({"message": "Client not found"}), 404

    # Fetch the professional
    professional = Professional.query.filter_by(professional_name=professional_name).first()
    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    if request.method == "POST":
        data = request.get_json()
        rating = data.get("rating")
        review_text = data.get("review_text")

        if rating is None or review_text is None:
            return jsonify({"message": "Rating and review_text are required"}), 400

        if not (1 <= rating <= 5):
            return jsonify({"message": "Rating must be between 1 and 5"}), 400

        # Create a new review
        review = Review(
            client_id=client.client_id,
            professional_id=professional.professional_id,
            review_rating=rating,
            review_comment=review_text
        )
        db.session.add(review)
        db.session.commit()

        # Update the professional's average rating
        reviews = Review.query.filter_by(professional_id=professional.professional_id).all()
        if reviews:
            average_rating = sum(r.review_rating for r in reviews) / len(reviews)
        else:
            average_rating = 0  # Handle case with no reviews

        professional.rating = average_rating
        db.session.commit()

        return jsonify({"message": "Review submitted successfully"}), 201


@app.route("/<professional_name>_profile", methods=["GET"])
@jwt_required()
def professional_profile(professional_name):
    # Fetch the professional record
    professional = Professional.query.filter_by(professional_name=professional_name).first()
    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    # Fetch all reviews for this professional
    reviews = Review.query.filter_by(professional_id=professional.professional_id).all()

    def reviews_to_json(reviews):
        result = []
        for review in reviews:
            result.append({
                "review_id": review.review_id,
                "review_rating": review.review_rating,
                "review_comment": review.review_comment,
                "client_id": review.client_id,
                "service_request_id": review.service_request_id
            })
        return result

    json_reviews = reviews_to_json(reviews)

    response = {
        "professional_id": professional.professional_id,
        "professional_name": professional.professional_name,
        "professional_date_created": professional.professional_date_created,
        "professional_description": professional.professional_description,
        "professional_experience": professional.professional_experience,
        "professional_service_type": professional.professional_service_type,
        "professional_rating": professional.professional_rating,
        "reviews": json_reviews
    }

    return jsonify(response), 200


@app.route("/profile_<client_name>", methods=["GET"])
@jwt_required()
def client_profile(client_name):
    # Fetch the client record
    client = Client.query.filter_by(client_name=client_name).first()
    if not client:
        return jsonify({"message": "Client not found"}), 404

    # Fetch all service requests for this client
    service_requests = ServiceRequest.query.filter_by(client_id=client.client_id).all()

    def service_requests_to_json(service_requests):
        result = []
        for request in service_requests:
            service = Service.query.get(request.service_id)
            if service:
                result.append({
                    "service_request_id": request.service_request_id,
                    "service_name": service.service_name,
                    "service_request_status": request.service_request_status,
                    "service_request_date_of_request": request.service_request_date_of_request,
                    "service_request_date_of_completion": request.service_request_date_of_completion
                })
        return result

    json_service_requests = service_requests_to_json(service_requests)

    response = {
        "client_name": client.client_name,
        "client_address": client.client_address,
        "client_phone": client.client_phone,
        "services_availed": json_service_requests
    }

    return jsonify(response), 200


@app.route("/create_service_request", methods=["POST"])
@jwt_required()
def create_a_service_request():
    data = request.get_json()
    service_id = data.get("service_id")
    remarks = data.get("remarks")

    client_name = get_jwt_identity()
    client = Client.query.filter_by(client_name=client_name).first()
    if not client:
        return jsonify({"message": "Client not found"}), 404

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"message": "Service not found"}), 404

    new_request = ServiceRequest(
        client_id=client.client_id,
        service_id=service_id,
        service_request_date_of_request=datetime.now(),
        service_request_status="pending",
        service_request_remarks=remarks
    )
    
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Service request created successfully"}), 201

@app.route("/edit_service_request/<int:request_id>", methods=["PUT"])
@jwt_required()
def edit_service_request(request_id):
    data = request.get_json()
    date_of_request = data.get("date_of_request")
    service_request_status = data.get("service_request_status")
    remarks = data.get("remarks")

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"message": "Service request not found"}), 404

    if date_of_request:
        service_request.service_request_date_of_request = datetime.strptime(date_of_request, "%Y-%m-%d")
    if service_request_status:
        service_request.service_request_status = service_request_status
    if remarks:
        service_request.service_request_remarks = remarks

    db.session.commit()

    return jsonify({"message": "Service request updated successfully"}), 200

@app.route("/create_service", methods=["POST"])
@jwt_required()
def create_service():
    token = get_jwt()
    if token["type"] != "admin":
        return jsonify({"message": "Not authorized"}), 401
    data = request.get_json()
    service_name = data["service_name"]
    service_description = data["service_description"]
    service_time_required = data["service_time_required"]
    service_base_price = data["service_base_price"]
    new_service = Service(
        service_name=service_name,
        service_description=service_description,
        service_time_required=service_time_required,
        service_base_price=service_base_price
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service created successfully"}), 201


@app.route("/delete_service", methods=["POST"])
@jwt_required()
def delete_service():
    token = get_jwt()
    if token["type"] != "admin":
        return jsonify({"message": "Not authorized"}), 401
    
    data = request.get_json()
    service_id = data["service_id"]

    # Find the service by ID
    service = Service.query.get(service_id)
    
    # If service does not exist, return an error
    if not service:
        return jsonify({"message": "Service not found"}), 404

    # Delete the service from the database
    db.session.delete(service)
    db.session.commit()
    
    return jsonify({"message": "Service deleted successfully"}), 200

@app.route("/delete_professional", methods=["POST"])
@jwt_required()
def delete_professional():
    token = get_jwt()
    if token["type"] != "admin":
        return jsonify({"message": "Not authorized"}), 401
    
    data = request.get_json()
    professional_id = data["professional_id"]

    # Find the professional by ID
    professional = Professional.query.get(professional_id)
    
    # If professional does not exist, return an error
    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    # Delete the professional from the database
    db.session.delete(professional)
    db.session.commit()
    
    return jsonify({"message": "Personnel Banned successfully"}), 200

# rating

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if service:
        return jsonify({
            'id': service.service_id,
            'name': service.service_name,
            'description': service.service_description,  # Include any other fields you need
        })
    else:
        return jsonify({'error': 'Service not found'}), 404

# @app.route("/admin_clients", methods=["GET"])
# @jwt_required()
# def get_clients_with_services():
#     try:
#         # Fetch all clients
#         clients = Client.query.all()
        
#         result = []
#         for client in clients:
#             # Query the ServiceRequest table to get all services for each client
#             service_requests = ServiceRequest.query.filter_by(client_id=client.client_id).all()
            
#             services = []
#             for service_request in service_requests:
#                 service = Service.query.get(service_request.service_id)  # Get service details
                
#                 # Ensure the service exists before calling to_json()
#                 if service:
#                     services.append(service.to_json())
#                 else:
#                     # If no service is found, you can handle it in a way you prefer
#                     services.append({"service_id": service_request.service_id, "message": "Service not found"})
            
#             result.append({
#                 "client_id": client.client_id,
#                 "client_name": client.client_name,
#                 "services": services
#             })
        
#         return jsonify(result), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 500 /professionals
from sqlalchemy.orm import joinedload

@app.route('/admin_clients', methods=['GET'])
def get_clients():
    try:
        # Fetch all clients and join with the services and service requests
        clients = Client.query.all()
        client_data = []
        
        for client in clients:
            services = []
            # Fetch the associated services and service requests
            service_requests = db.session.query(ServiceRequest, Service).filter(
                ServiceRequest.client_id == client.client_id,
                ServiceRequest.service_id == Service.service_id
            ).all()
            
            for service_request, service in service_requests:
                services.append({
                    'service_id': service.service_id,
                    'service_name': service.service_name,
                    'service_request_status': service_request.service_request_status
                })
            
            client_data.append({
                'client_id': client.client_id,
                'client_name': client.client_name,
                'client_address': client.client_address,
                'client_phone': client.client_phone,
                'services': services
            })
        
        return jsonify(client_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete_client', methods=['DELETE'])
def delete_client():
    try:
        client_id = request.json.get('client_id')
        client = Client.query.get(client_id)
        if not client:
            return jsonify({"error": "Client not found"}), 404

        # Delete associated data, such as services and requests, if necessary
        ServiceRequest.query.filter_by(client_id=client_id).delete()
        
        # Delete the client
        db.session.delete(client)
        db.session.commit()

        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# @app.route("/services", methods=["GET"])
# def get_services():
#     services = Service.query.all()
#     return jsonify([service.to_json() for service in services])

@app.route("/clients/<int:client_id>/history", methods=["GET"])
def get_client_service_history(client_id):
#     service_requests = ServiceRequest.query.filter_by(client_id=client_id).all()
    return jsonify([service_request.to_json() for service_request in service_requests])

from datetime import datetime

@app.route("//service-request", methods=["POST"])
def create_service_request():
    try:
        data = request.get_json()
        required_fields = ["client_id", "service_id", "professional_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        new_service_request = ServiceRequest(
            client_id=data["client_id"],
            service_id=data["service_id"],
            professional_id=data["professional_id"],
            service_request_status=data.get("service_request_status", "pending"),
            service_request_remarks=data.get("remarks", "No Special Remarks"),
            service_request_date_of_request=str(datetime.now()),
        )

        # Add to database
        db.session.add(new_service_request)
        db.session.commit()

        # Add the service request to history
        history_entry = ServiceRequestHistory(
            status=new_service_request.service_request_status,
            timestamp=str(datetime.now()),
            remarks=new_service_request.service_request_remarks,
            service_request_id=new_service_request.service_request_id,
        )
        db.session.add(history_entry)

        # Add an entry to ClientProfessional table
        client_professional_entry = ClientProfessional(
            client_id=data["client_id"],
            professional_id=data["professional_id"],
            interaction_type="Service Request",
            interaction_date=str(datetime.now()),
            notes=new_service_request.service_request_remarks,
        )
        db.session.add(client_professional_entry)

        # Commit all changes
        db.session.commit()

        return jsonify(new_service_request.to_json()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# /client_login

@app.route("/services/<int:service_id>/professionals", methods=["GET"], endpoint="ServiceDetails")
def serviceDetails(service_id):
    try:
        # Fetch professionals linked to the given service_id
        professionals = (
            db.session.query(Professional)
            .filter(Professional.professional_service_type == service_id)  # Filtering professionals by service_id
            .all()
        )

        # Format the response with relevant fields
        result = [
            {
                "professional_id": professional.professional_id,
                "name": professional.professional_name,  # Corrected field name to match the model
                "description": professional.professional_description,  # Corrected field name to match the model
                "experience": professional.professional_experience,  # Corrected field name to match the model
                "rating": professional.professional_rating,  # Corrected field name to match the model
            }
            for professional in professionals
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("//service-request", methods=["POST"])
def create_service_request_for_professional():
    data = request.get_json()

    # Extract the required fields
    professional_id = data.get('professional_id')
    client_id = data.get('client_id')
    remarks = data.get('remarks')
    service_id = data.get('service_id')  # Ensure this is included

    print(f"Received data: professional_id={professional_id}, client_id={client_id}, remarks={remarks}, service_id={service_id}")

    if not all([professional_id, client_id, remarks, service_id]):
        return jsonify({"error": "Missing required fields"}), 400

    # Process the data, such as inserting into ServiceRequest table
    try:
        # Create the service request object
        service_request = ServiceRequest(
            professional_id=professional_id,
            client_id=client_id,
            service_id=service_id,  # Assign service_id to the request
            service_request_remarks=remarks,  # Assign remarks to the service request
            service_request_status="Requested",  # You may want to default the status
            service_request_date_of_request=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Optional: set the date of request
        )
        
        # Add to the database session and commit
        print(service_request_remarks)
        db.session.add(service_request)
        db.session.commit()

        # Create a service request history entry
        service_request_history = ServiceRequestHistory(
            service_request_id=service_request.service_request_id,
            status="Requested",
            timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            remarks=remarks  # Assign the same remarks to the history
        )
        db.session.add(service_request_history)
        db.session.commit()

        return jsonify({"message": "Request sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import traceback
from flask import jsonify


# @app.route("/service-log", methods=["GET"])
# @jwt_required()
# def get_service_log():
#     client_id = get_jwt_identity()  # This assumes that the client_id is stored in the JWT payload

#     if not client_id:
#         return jsonify({"error": "Client ID not found in token"}), 401
#     try:
#         # Fetch service requests associated with the client
#         service_requests = db.session.query(ServiceRequest, ServiceRequestHistory, Professional, Service).\
#             join(ServiceRequestHistory, ServiceRequest.service_request_id == ServiceRequestHistory.service_request_id).\
#             join(Professional, ServiceRequest.professional_id == Professional.professional_id).\
#             join(Service, ServiceRequest.service_id == Service.service_id).\
#             filter(ServiceRequest.client_id == client_id).all()

#         # Format the data for response
#         service_log = []
#         for service_request, history, professional, service in service_requests:
#             status_color = "bg-danger" if service_request.service_request_status != "Completed" else "bg-success"
#             service_log.append({
#                 "professional_name": professional.professional_name,  # Corrected professional name
#                 "service_type": service.service_name,  # Corrected service name reference
#                 "service_request_date": service_request.service_request_date_of_request,
#                 "service_completion_date": service_request.service_request_date_of_completion or 'Not Completed Yet',
#                 "status": service_request.service_request_status,
#                 "status_color": status_color,
#                 "professional_id": professional.professional_id
#             })

#         return jsonify(service_log), 200

#     except Exception as e:
#         # Log detailed error message and traceback for debugging
#         error_message = str(e)
#         app.logger.error(f"Error occurred in /service-log endpoint: {error_message}")
#         app.logger.error(traceback.format_exc())  # This will log the full stack trace

#         return jsonify({"error": f"An error occurred on the server: {error_message}"}), 500

@app.route("/service-log", methods=["GET"])
def get_service_log():
    client_id = request.args.get("client_id")
    
    # Log the received client_id for debugging purposes
    app.logger.info(f"Received client_id: {client_id}")

    if not client_id:
        app.logger.error("Client ID is missing in the request.")
        return jsonify({"error": "Client ID is required"}), 400

    try:
        # Fetch service requests associated with the client
        service_requests = db.session.query(ServiceRequest, ServiceRequestHistory, Professional, Service).\
            join(ServiceRequestHistory, ServiceRequest.service_request_id == ServiceRequestHistory.service_request_id).\
            join(Professional, ServiceRequest.professional_id == Professional.professional_id).\
            join(Service, ServiceRequest.service_id == Service.service_id).\
            filter(ServiceRequest.client_id == client_id).all()

        # Format the data for response
        service_log = []
        for service_request, history, professional, service in service_requests:
            status_color = "bg-danger" if service_request.service_request_status != "Completed" else "bg-success"
            service_log.append({
                "professional_name": professional.professional_name,
                "service_type": service.service_name,
                "service_request_date": service_request.service_request_date_of_request,
                "service_completion_date": service_request.service_request_date_of_completion or 'Not Completed Yet',
                "status": service_request.service_request_status,
                "status_color": status_color,
                "professional_id": professional.professional_id
            })

        return jsonify(service_log), 200

    except Exception as e:
        # Log detailed error message and traceback for debugging
        error_message = str(e)
        app.logger.error(f"Error occurred in /service-log endpoint: {error_message}")
        app.logger.error(traceback.format_exc())  # This will log the full stack trace

        return jsonify({"error": f"An error occurred on the server: {error_message}"}), 500
# service_log

@app.route('/write-review/<int:professional_id>', methods=['POST'])
def write_review(professional_id):
    try:
        # Get the data from the request
        data = request.get_json()
        rating = int(data.get('rating'))  # Ensure rating is an integer
        review_comment = data.get('review')
        client_id = data.get('client_id')
        service_request_id = data.get('service_request_id')

        if rating is None or review_comment is None or client_id is None or service_request_id is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Fetch professional, client, and service request
        professional = Professional.query.get(professional_id)
        service_request = ServiceRequest.query.get(service_request_id)
        client = Client.query.get(client_id)

        if not professional or not service_request or not client:
            return jsonify({"error": "Invalid references"}), 404

        # Check for existing review
        existing_review = Review.query.filter_by(
            professional_id=professional_id,
            service_request_id=service_request_id
        ).first()

        if existing_review:
            existing_review.review_rating = rating
            existing_review.review_comment = review_comment
        else:
            new_review = Review(
                review_rating=rating,
                review_comment=review_comment,
                client_id=client_id,
                service_request_id=service_request_id,
                professional_id=professional_id
            )
            db.session.add(new_review)

        # Update professional rating
        total_reviews = len(professional.reviews)
        current_rating = float(professional.professional_rating or 0)  # Handle None
        professional.professional_rating = (current_rating * total_reviews + rating) / (total_reviews + 1)

        db.session.commit()
        return jsonify(existing_review.to_json() if existing_review else new_review.to_json()), 201

    except ValueError as ve:
        db.session.rollback()
        return jsonify({"error": "Invalid data type in request: " + str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# @app.route('/write-review/<int:professional_id>', methods=['POST'])
# def write_review(professional_id):
#     try:
#         # Get the data from the request
#         data = request.get_json()
#         print(data)
#         # Extract values from the request body
#         rating = data.get('rating')
#         review_comment = data.get('review')
#         client_id = data.get('client_id')
#         service_request_id = data.get('service_request_id')

#         # Check if all required fields are present
#         if rating is None or review_comment is None or client_id is None or service_request_id is None:
#             return jsonify({"error": "Missing required fields"}), 400

#         # Check if the professional and service request exist
#         professional = Professional.query.get(professional_id)
#         service_request = ServiceRequest.query.get(service_request_id)
#         client = Client.query.get(client_id)

#         if not professional:
#             return jsonify({"error": "Professional not found"}), 404
#         if not service_request:
#             return jsonify({"error": "Service Request not found"}), 404
#         if not client:
#             return jsonify({"error": "Client not found"}), 404

#         # Check if a review already exists for the service request and professional
#         existing_review = Review.query.filter_by(
#             professional_id=professional_id,
#             service_request_id=service_request_id
#         ).first()

#         if existing_review:
#             # If a review exists, update it
#             existing_review.review_rating = rating
#             existing_review.review_comment = review_comment
#             db.session.commit()
#             return jsonify(existing_review.to_json()), 200
#         else:
#             # If no review exists, create a new one
#             new_review = Review(
#                 review_rating=rating,
#                 review_comment=review_comment,
#                 client_id=client_id,
#                 service_request_id=service_request_id,
#                 professional_id=professional_id
#             )
#             db.session.add(new_review)
#             db.session.commit()
#             return jsonify(new_review.to_json()), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


@app.route("/professionals/<int:professional_id>", methods=["GET"])
def get_professional_profile(professional_id):
    try:
        # Fetch professional details based on the ID
        professional = db.session.query(Professional).filter_by(professional_id=professional_id).first()

        if not professional:
            return jsonify({"error": "Professional not found"}), 404

        # Return professional details including experience
        return jsonify({
            "professional_name": professional.professional_name,
            "professional_rating": professional.professional_rating,
            "professional_description": professional.professional_description,
            "professional_experience": professional.professional_experience  # Added experience field
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/professionals-in-contact", methods=["GET"])
def get_professionals_in_contact():
    client_id = 1  # Or get from session/token
    try:
        # Query to fetch all professionals the client is in contact with, along with service details
        professionals = db.session.query(Professional, Service).\
            join(Service, Professional.professional_service_type == Service.service_id).\
            filter(Professional.professional_id.in_(
                db.session.query(ClientProfessional.professional_id).filter(ClientProfessional.client_id == client_id)
            )).all()

        # Prepare data with existing reviews
        professionals_data = []
        for professional, service in professionals:
            existing_review = db.session.query(Review).filter_by(client_id=client_id, professional_id=professional.professional_id).first()
            professionals_data.append({
                "professional_id": professional.professional_id,
                "professional_name": professional.professional_name,
                "service_name": service.service_name,
                "professional_experience": professional.professional_experience,
                "existingReview": {
                    "rating": existing_review.review_rating if existing_review else None,
                    "comment": existing_review.review_comment if existing_review else ''
                } if existing_review else None
            })

        return jsonify(professionals_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('//service-requests/<int:service_id>/professionals', methods=['GET'])
def get_professionals_by_service(service_id):
    try:
        # Query ServiceRequest table for professionals linked to this service_id
        service_requests = ServiceRequest.query.filter_by(service_id=service_id).all()

        if not service_requests:
            return jsonify({"error": "No professionals found for this service"}), 404

        # Fetch professional details
        professional_ids = [sr.professional_id for sr in service_requests]
        professionals = Professional.query.filter(Professional.id.in_(professional_ids)).all()

        # Format the response
        response = [
            {
                "professional_id": prof.id,
                "name": prof.name,
                "description": prof.description,
                "experience": prof.experience,
                "rating": prof.rating,
            }
            for prof in professionals
        ]
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500







@app.route('/service_request/<int:service_request_id>/reject', methods=['PUT'])
@jwt_required()
def reject_service_request(service_request_id):
    # Fetch the service request by ID
    service_request = ServiceRequest.query.get(service_request_id)
    
    if not service_request:
        return jsonify({"message": "Service request not found"}), 404
    
    # Update the status and completion date
    service_request.service_request_status = "Rejected"
    service_request.service_request_date_of_completion = datetime.utcnow().isoformat()

    try:
        db.session.commit()
        return jsonify(service_request.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500






@app.route('/<int:client_id>/reviewable-professionals', methods=['GET'])
def get_reviewable_professionals():
    client_id = 1  # Replace with actual client ID retrieval logic (e.g., from session or token)

    try:
        # Fetch all service requests for the client
        service_requests = ServiceRequest.query.filter_by(client_id=client_id).all()

        if not service_requests:
            return jsonify({"error": "No service requests found for this client."}), 404

        # Get unique professional IDs from service requests
        professional_ids = list(set(sr.professional_id for sr in service_requests))

        # Fetch professional details
        professionals = Professional.query.filter(Professional.professional_id.in_(professional_ids)).all()

        # Prepare response data with existing reviews
        professionals_data = []
        for prof in professionals:
            # Fetch the service request associated with this professional (assuming one-to-one; adjust if many)
            service_requests_for_prof = ServiceRequest.query.filter_by(client_id=client_id, professional_id=prof.professional_id).all()

            # Fetch existing reviews for this professional by the client
            existing_review = Review.query.filter_by(client_id=client_id, professional_id=prof.professional_id).first()

            professionals_data.append({
                "professional_id": prof.professional_id,
                "professional_name": prof.professional_name,
                "service_name": Service.query.get(prof.professional_service_type).service_name if prof.professional_service_type else "",
                "professional_experience": prof.professional_experience,
                "professional_rating": prof.professional_rating,
                "existingReview": {
                    "review_rating": existing_review.review_rating,
                    "review_comment": existing_review.review_comment
                } if existing_review else None
            })

        return jsonify(professionals_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to submit or update a review
# @app.route("/client/submit-review", methods=["POST"])
# def submit_review():
#     client_id = 1  # Replace with actual client ID retrieval logic
#     data = request.get_json()

#     try:
#         professional_id = data.get("professional_id")
#         rating = data.get("rating")
#         comment = data.get("comment")

#         if not professional_id or not rating:
#             return jsonify({"error": "Professional ID and rating are required."}), 400

#         # Check if a review already exists
#         existing_review = Review.query.filter_by(client_id=client_id, professional_id=professional_id).first()

#         if existing_review:
#             # Update the existing review
#             existing_review.review_rating = rating
#             existing_review.review_comment = comment
#             db.session.commit()
#             return jsonify({"message": "Review updated successfully."}), 200
#         else:
#             # Create a new review
#             new_review = Review(
#                 review_rating=rating,
#                 review_comment=comment,
#                 client_id=client_id,
#                 professional_id=professional_id,
#                 service_request_id=None  # If linking to a specific service request, include it here
#             )
#             db.session.add(new_review)
#             db.session.commit()
#             return jsonify({"message": "Review submitted successfully."}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/professional_login", methods=["POST"])
# def professional_login():
#     data = request.get_json()
#     if not data or 'professional_name' not in data or 'professional_password' not in data:

#         return {"message": "professional_name and professional_password are required"}, 400
    

#     professional_name = data["professional_name"]
#     professional_password = data["professional_password"]
#     professional_from_db = Professional.query.filter_by(professional_name=professional_name).first()


#     if professional_from_db and professional_from_db.professional_password == professional_password:
#         token = create_access_token(identity=professional_name, additional_claims={"type": "professional"})
#         return {"access_token": token}, 200
#     return {"message": "invalid credentials"},401

@app.route("/professional_login", methods=["POST"])
def professional_login():
    data = request.get_json()

    # Validate request data
    if not data or "professional_name" not in data or "professional_password" not in data:
        return {"message": "Missing credentials"}, 400

    professional_name = data["professional_name"]
    professional_password = data["professional_password"]

    # Find professional by name
    professional = Professional.query.filter_by(professional_name=professional_name).first()

    if not professional or professional.professional_password != professional_password:
        return {"message": "Invalid credentials"}, 401

    # Generate JWT token
    token = create_access_token(identity=professional.professional_id, additional_claims={"type": "professional"})

    return {
        "access_token": token,
        "professional_id": professional.professional_id,
    }, 200

@app.route("/professional/details", methods=["GET"])
@jwt_required()
def get_professional_details():
    current_identity = get_jwt_identity()
    professional = Professional.query.filter_by(professional_name=current_identity).first()
    if professional:
        return professional.to_json(), 200
    return {"message": "Professional not found"}, 404

@app.route('/professional_dashboard', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated
def professional_dashboard():
    try:
        # Get the current professional's id from the JWT token
        professional_id = get_jwt_identity()

        # Fetch service requests related to the professional and their clients
        requests = db.session.query(ServiceRequest, Client) \
            .join(Client, ServiceRequest.client_id == Client.client_id) \
            .filter(ServiceRequest.professional_id == professional_id) \
            .filter(ServiceRequest.service_request_status.in_(['active', 'pending'])) \
            .order_by(ServiceRequest.service_request_date_of_request.desc()) \
            .all()

        # Prepare the data to return as JSON
        response_data = []
        for request, client in requests:
            response_data.append({
                'service_request_id': request.service_request_id,  # Add service_request_id to the response
                'client_name': client.client_name,
                'service_request_date_of_request': request.service_request_date_of_request,
                'service_request_remarks': request.service_request_remarks,
                'client_id': client.client_id,
            })

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/service_request/<int:service_request_id>/complete', methods=['PUT'])
def complete_service_request(service_request_id):
    service_request = ServiceRequest.query.get(service_request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    # Update the status and completion date
    service_request.service_request_status = "Completed"
    service_request.service_request_date_of_completion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        db.session.commit()
        return jsonify({"message": "Service request marked as completed"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




@app.route('/completed_services', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated
def completed_services():
    try:
        # Get the current professional's id from the JWT token
        professional_id = get_jwt_identity()

        # Fetch completed service requests related to the professional and their clients
        completed_requests = db.session.query(ServiceRequest, Client) \
            .join(Client, ServiceRequest.client_id == Client.client_id) \
            .filter(ServiceRequest.professional_id == professional_id) \
            .filter(ServiceRequest.service_request_status == 'Completed') \
            .order_by(ServiceRequest.service_request_date_of_completion.desc()) \
            .all()

        # Prepare the data to return as JSON
        response_data = []
        for request, client in completed_requests:
            response_data.append({
                'service_request_id': request.service_request_id,
                'client_name': client.client_name,
                'service_request_date_of_request': request.service_request_date_of_request,
                'service_request_date_of_completion': request.service_request_date_of_completion,
                'service_request_remarks': request.service_request_remarks,
                'client_id': client.client_id,
            })

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/client_reviews', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated
def client_reviews():
    try:
        # Get the current professional's id from the JWT token
        professional_id = get_jwt_identity()

        # Get optional search parameters from query string
        client_name = request.args.get('client_name', '')
        service_request_date = request.args.get('service_request_date', '')

        # Build the base query
        query = db.session.query(Review, ServiceRequest, Client) \
            .join(ServiceRequest, Review.service_request_id == ServiceRequest.service_request_id) \
            .join(Client, Review.client_id == Client.client_id) \
            .filter(Review.professional_id == professional_id)

        # Apply filters based on client_name and service_request_date if provided
        if client_name:
            query = query.filter(Client.client_name.ilike(f'%{client_name}%'))
        if service_request_date:
            query = query.filter(ServiceRequest.service_request_date_of_request == service_request_date)

        reviews = query.all()

        # Prepare the data to return as JSON
        response_data = []
        for review, service_request, client in reviews:
            response_data.append({
                'client_name': client.client_name,
                'service_request_date_of_request': service_request.service_request_date_of_request,
                'review_comment': review.review_comment,
                'review_rating': review.review_rating,
                'service_request_id': service_request.service_request_id,
            })

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/professional_profile', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated
def get_professional_profile_page():
    try:
        professional_id = get_jwt_identity()

        # Fetch professional details from the database
        professional = Professional.query.filter_by(professional_id=professional_id).first()

        if professional:
            # Return professional details excluding the password
            response_data = {
                'professional_name': professional.professional_name,
                'professional_description': professional.professional_description,
                'professional_experience': professional.professional_experience,
                'professional_rating': professional.professional_rating,
                'professional_date_created': professional.professional_date_created,
                'professional_service_type': professional.professional_service_type
            }
            return jsonify(response_data), 200
        else:
            return jsonify({'error': 'Professional not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/professional_profile/update', methods=['PUT'])
@jwt_required()  # Ensure the user is authenticated
def update_professional_profile():
    try:
        professional_id = get_jwt_identity()

        # Fetch the professional from the database
        professional = Professional.query.filter_by(professional_id=professional_id).first()

        if professional:
            # Get updated details from request
            data = request.get_json()
            professional.professional_name = data.get('professional_name', professional.professional_name)
            professional.professional_description = data.get('professional_description', professional.professional_description)
            professional.professional_experience = data.get('professional_experience', professional.professional_experience)

            # Commit the changes to the database
            db.session.commit()

            return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Professional not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/client-professionals', methods=['GET'])
# def get_professionals():
#     try:
#         client_id = request.args.get('client_id')  # Get client_id from query parameters
        
#         # Query the ClientProfessional table to get professional IDs associated with the client
#         client_professionals = ClientProfessional.query.filter_by(client_id=client_id).all()
        
#         # Extract the professional IDs
#         professional_ids = [cp.professional_id for cp in client_professionals]
        
#         # Now, join with ServiceRequest to get the request date
#         professionals_data = []
#         for professional_id in professional_ids:
#             service_request = ServiceRequest.query.filter_by(client_id=client_id, professional_id=professional_id).first()
#             if service_request:
#                 request_date = service_request.request_date
#             else:
#                 request_date = None  # If no request is found, set it to None
                
#             # Fetch professional details
#             professional = Professional.query.get(professional_id)
#             if professional:
#                 professionals_data.append({
#                     'professional_id': professional.professional_id,
#                     'professional_name': professional.professional_name,
#                     'professional_description': professional.professional_description,
#                     'professional_experience': professional.professional_experience,
#                     'professional_rating': professional.professional_rating,
#                     'professional_service_type': professional.professional_service_type,
#                     'request_date': request_date  # Add the request date to the data
#                 })
        
#         # Return the data as a JSON response
#         return jsonify(professionals_data), 200
    
#     except Exception as e:
#         # Handle any potential errors (e.g., database connection issues)
#         print(f"Error: {e}")
#         return jsonify({"error": "Internal Server Error"}), 500

# @app.route('/review/<int:professional_id>', methods=['POST', 'PUT'])
# def submit_review(professional_id):
#     try:
#         professional = Professional.query.get(professional_id)
#         if not professional:
#             return jsonify({'error': 'Professional not found'}), 404
        
#         # Get the review data from the request body
#         review_data = request.get_json()
#         rating = review_data.get('rating')
#         comment = review_data.get('comment')
        
#         # Validate the data
#         if not rating or not comment:
#             return jsonify({'error': 'Rating and comment are required'}), 400
        
#         # If review already exists, update it
#         if professional.has_review:
#             professional.review_rating = rating
#             professional.review_comment = comment
#         else:
#             professional.review_rating = rating
#             professional.review_comment = comment
#             professional.has_review = True
        
#         # Commit the changes to the database
#         db.session.commit()
        
#         return jsonify({'message': 'Review submitted successfully'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500




# @app.route('/client-professionals', methods=['GET'])
# def get_client_professionals(current_user):
#     client_id = request.args.get('client_id')
#     client = Client.query.get(client_id)
    
#     if not client:
#         return jsonify({"message": "Client not found"}), 404

#     professionals = []
#     for professional in client.professionals:
#         professionals.append({
#             "professional_id": professional.professional_id,
#             "professional_name": professional.professional_name,
#             "professional_service_type": professional.professional_service_type,
#             "professional_date_created": professional.professional_date_created,
#         })

#     return jsonify({"professionals": professionals})


# @app.route('/submit-review', methods=['POST'])
# def submit_reviewss(current_user):
#     data = request.get_json()

#     rating = data.get('rating')
#     comment = data.get('comment')
#     professional_id = data.get('professional_id')

#     if not rating or not comment:
#         return jsonify({"message": "Rating and comment are required."}), 400

#     review = Review(
#         review_rating=rating,
#         review_comment=comment,
#         client_id=current_user.client_id,
#         professional_id=professional_id,
#     )
#     db.session.add(review)
#     db.session.commit()

#     return jsonify({"message": "Review submitted successfully."}), 201
################
# @app.route("/add_review", methods=["POST"])
# @jwt_required()
# def add_review():
#     """
#     Add a review for a professional related to a service request.
#     """
#     data = request.get_json()
#     # Validate the required fields
#     if not data or 'review_rating' not in data or 'client_id' not in data or 'service_request_id' not in data or 'professional_id' not in data:
#         return {"message": "Missing required fields"}, 400

#     review_rating = data["review_rating"]
#     review_comment = data.get("review_comment", "")  # Optional field
#     client_id = data["client_id"]
#     service_request_id = data["service_request_id"]
#     professional_id = data["professional_id"]

#     try:
#         # Check if the service request exists
#         service_request = ServiceRequest.query.get(service_request_id)
#         if not service_request:
#             return {"message": "Invalid service request ID"}, 404

#         # Create a new review
#         new_review = Review(
#             review_rating=review_rating,
#             review_comment=review_comment,
#             client_id=client_id,
#             service_request_id=service_request_id,
#             professional_id=professional_id
#         )
#         db.session.add(new_review)
#         db.session.commit()

#         return {"message": "Review added successfully"}, 201
#     except Exception as e:
#         db.session.rollback()
#         return {"message": f"An error occurred: {str(e)}"}, 500


# @app.route("/get_reviews", methods=["GET"])
# @jwt_required()
# def get_reviews():
#     """
#     Fetch all reviews or reviews filtered by professional ID.
#     """
#     professional_id = request.args.get("professional_id", None)
#     try:
#         if professional_id:
#             reviews = Review.query.filter_by(professional_id=professional_id).all()
#         else:
#             reviews = Review.query.all()

#         if not reviews:
#             return {"message": "No reviews found"}, 404

#         # Convert reviews to JSON format
#         json_reviews = [review.to_json() for review in reviews]
#         return {"reviews": json_reviews}, 200
#     except Exception as e:
#         return {"message": f"An error occurred: {str(e)}"}, 500


# @app.route("/update_review/<int:review_id>", methods=["PUT"])
# @jwt_required()
# def update_review(review_id):
#     """
#     Update an existing review by review ID.
#     """
#     data = request.get_json()
#     try:
#         review = Review.query.get(review_id)
#         if not review:
#             return {"message": "Review not found"}, 404

#         # Update review fields
#         review.review_rating = data.get("review_rating", review.review_rating)
#         review.review_comment = data.get("review_comment", review.review_comment)

#         db.session.commit()
#         return {"message": "Review updated successfully"}, 200
#     except Exception as e:
#         db.session.rollback()
#         return {"message": f"An error occurred: {str(e)}"}, 500


# @app.route("/delete_review/<int:review_id>", methods=["DELETE"])
# @jwt_required()
# def delete_review(review_id):
#     """
#     Delete a review by review ID.
#     """
#     try:
#         review = Review.query.get(review_id)
#         if not review:
#             return {"message": "Review not found"}, 404

#         db.session.delete(review)
#         db.session.commit()
#         return {"message": "Review deleted successfully"}, 200
#     except Exception as e:
#         db.session.rollback()
#         return {"message": f"An error occurred: {str(e)}"}, 500


# @app.route("/review", methods=["POST", "GET", "PUT", "DELETE"])
# @jwt_required()
# def review():
#     """
#     Handle all review-related actions based on HTTP methods.
#     """
#     if request.method == "POST":
#         # Adding a new review
#         data = request.get_json()
#         if not data or 'review_rating' not in data or 'client_id' not in data or 'service_request_id' not in data or 'professional_id' not in data:
#             return {"message": "Missing required fields"}, 400

#         review_rating = data["review_rating"]
#         review_comment = data.get("review_comment", "")
#         client_id = data["client_id"]
#         service_request_id = data["service_request_id"]
#         professional_id = data["professional_id"]

#         try:
#             service_request = ServiceRequest.query.get(service_request_id)
#             if not service_request:
#                 return {"message": "Invalid service request ID"}, 404

#             new_review = Review(
#                 review_rating=review_rating,
#                 review_comment=review_comment,
#                 client_id=client_id,
#                 service_request_id=service_request_id,
#                 professional_id=professional_id,
#             )
#             db.session.add(new_review)
#             db.session.commit()

#             return {"message": "Review added successfully"}, 201
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"An error occurred: {str(e)}"}, 500

#     elif request.method == "GET":
#         # Fetching reviews
#         professional_id = request.args.get("professional_id", None)
#         try:
#             if professional_id:
#                 reviews = Review.query.filter_by(professional_id=professional_id).all()
#             else:
#                 reviews = Review.query.all()

#             if not reviews:
#                 return {"message": "No reviews found"}, 404

#             json_reviews = [review.to_json() for review in reviews]
#             return {"reviews": json_reviews}, 200
#         except Exception as e:
#             return {"message": f"An error occurred: {str(e)}"}, 500

#     elif request.method == "PUT":
#         # Updating a review
#         data = request.get_json()
#         review_id = data.get("review_id")
#         if not review_id:
#             return {"message": "Review ID is required"}, 400

#         try:
#             review = Review.query.get(review_id)
#             if not review:
#                 return {"message": "Review not found"}, 404

#             review.review_rating = data.get("review_rating", review.review_rating)
#             review.review_comment = data.get("review_comment", review.review_comment)
#             db.session.commit()

#             return {"message": "Review updated successfully"}, 200
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"An error occurred: {str(e)}"}, 500

#     elif request.method == "DELETE":
#         # Deleting a review
#         data = request.get_json()
#         review_id = data.get("review_id")
#         if not review_id:
#             return {"message": "Review ID is required"}, 400

#         try:
#             review = Review.query.get(review_id)
#             if not review:
#                 return {"message": "Review not found"}, 404

#             db.session.delete(review)
#             db.session.commit()

#             return {"message": "Review deleted successfully"}, 200
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"An error occurred: {str(e)}"}, 500

#     return {"message": "Invalid method"}, 405



@app.route('/client-details', methods=['GET'])
@jwt_required()
def client_details():
    client_id = get_jwt_identity()
    client = Client.query.get(client_id)
    if client:
        return jsonify(client.to_json()), 200
    return jsonify({"error": "Client not found"}), 404

@app.route('/services', methods=['GET'])
def services():
    services = Service.query.all()
    return jsonify([service.to_json() for service in services]), 200

@app.route('/service-log', methods=['GET'])
@jwt_required()
def service_log():
    client_id = get_jwt_identity()
    service_requests = ServiceRequest.query.filter_by(client_id=client_id).all()
    return jsonify([request.to_json() for request in service_requests]), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


# Update or Create Review
@app.route('/review', methods=['POST', 'PUT'])
def handle_review():
    try:
        data = request.json

        # Ensure the required fields are provided
        required_fields = ['review_id', 'review_rating', 'client_id', 'service_request_id', 'professional_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 422

        # Retrieve the review by ID (for update)
        review = Review.query.filter_by(review_id=data['review_id']).first()

        if request.method == 'PUT':  # Update existing review
            if not review:
                return jsonify({"error": "Review not found"}), 404

            review.review_rating = data['review_rating']
            review.review_comment = data.get('review_comment', review.review_comment)
            review.client_id = data['client_id']
            review.service_request_id = data['service_request_id']
            review.professional_id = data['professional_id']

            db.session.commit()
            return jsonify({"message": "Review updated successfully", "review": review.to_json()}), 200

        elif request.method == 'POST':  # Create new review
            if review:
                return jsonify({"error": "Review with this ID already exists"}), 409

            new_review = Review(
                review_id=data['review_id'],
                review_rating=data['review_rating'],
                review_comment=data.get('review_comment'),
                client_id=data['client_id'],
                service_request_id=data['service_request_id'],
                professional_id=data['professional_id']
            )
            db.session.add(new_review)
            db.session.commit()
            return jsonify({"message": "Review created successfully", "review": new_review.to_json()}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/service_requests', methods=['GET'])
def get_service_requests():
    service_requests = db.session.query(ServiceRequest, Client.client_name, Service.service_name, Professional.professional_name)\
        .join(Client, Client.client_id == ServiceRequest.client_id)\
        .join(Service, Service.service_id == ServiceRequest.service_id)\
        .join(Professional, Professional.professional_id == ServiceRequest.professional_id)\
        .all()

    result = []
    for service_request, client_name, service_name, professional_name in service_requests:
        result.append({
            "service_request_id": service_request.service_request_id,
            "service_request_date_of_request": service_request.service_request_date_of_request,
            "service_request_date_of_completion": service_request.service_request_date_of_completion,
            "service_request_status": service_request.service_request_status,
            "service_request_remarks": service_request.service_request_remarks,
            "client_name": client_name,  # Include client name
            "service_name": service_name,  # Include service name
            "professional_name": professional_name  # Include professional name
        })
    
    return jsonify(result)





@app.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        reviews = Review.query.all()
        reviews_list = []
        for review in reviews:
            client = Client.query.get(review.client_id)
            professional = Professional.query.get(review.professional_id)
            reviews_list.append({
                'review_id': review.review_id,
                'client_name': client.client_name,
                'professional_name': professional.professional_name,
                'review_rating': review.review_rating,
                'review_comment': review.review_comment
            })
        return jsonify(reviews_list), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching reviews', 'error': str(e)}), 500


















@app.route("/client_login", methods=["POST"])
def client_login():
    data = request.get_json()
    if not data or 'client_name' not in data or 'client_password' not in data:
        return {"message": "client_name and client_password are required"}, 400

    client_name = data["client_name"]
    client_password = data["client_password"]

    client_from_db = Client.query.filter_by(client_name=client_name).first()
    if client_from_db and client_from_db.client_password == client_password:
        token = create_access_token(identity=client_name, additional_claims={"type": "client"})
        return {
            "access_token": token,
            "client_id": client_from_db.client_id
        }, 200

    return {"message": "invalid credentials"}, 401


@app.route("/client_dashboard", methods=["GET"])
@jwt_required()
def client_dashboard():
    client_name = get_jwt_identity()
    return {"message": f"Welcome, {client_name}!"}, 200
# /service-request  create_service_request service-log

@app.route('/service-request', methods=['POST'])
def create_service_request_from_client():
    data = request.get_json()
    
    try:
        # Extract the data from the request
        professional_id = data.get('professional_id')
        client_id = data.get('client_id')
        remarks = data.get('remarks')
        service_id = data.get('service_id')
        
        # Create a new service request record
        new_request = ServiceRequest(
            service_request_date_of_request=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            service_request_status="requested",
            service_request_remarks=remarks,
            client_id=client_id,
            service_id=service_id,
            professional_id=professional_id
        )
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify(new_request.to_json()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        













@app.route("/services", methods=["GET"])
@jwt_required()
def get_services():
    services = Service.query.all()
    if not services:
        return {"message": "No services available"}, 404
    return {"services": [service.to_json() for service in services]}, 200


@app.route("/services/<int:service_id>/professionals", methods=["GET"])
def get_professionals_for_service(service_id):
    professionals = Professional.query.filter_by(professional_service_type=service_id).all()
    if not professionals:
        return {"message": f"No professionals found for service_id {service_id}"}, 404

    return {"professionals": [professional.to_json() for professional in professionals]}, 200





# Route to fetch the rating of a professional
@app.route('/professional/<int:professional_id>/rating', methods=['GET'])
def get_professional_rating(professional_id):
    try:
        # Fetch the professional from the database
        professional = Professional.query.get(professional_id)
        if professional:
            # Send the rating of the professional as a response
            return jsonify({"rating": professional.professional_rating}), 200
        else:
            return jsonify({"error": "Professional not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch reviews for a professional
@app.route('/professional/<int:professional_id>/reviews', methods=['GET'])
def get_professional_reviews(professional_id):
    try:
        # Fetch all reviews for the given professional_id
        reviews = Review.query.filter_by(professional_id=professional_id).all()
        review_data = []

        # Add each review to the response data
        for review in reviews:
            client = Client.query.get(review.client_id)  # Get client info for the review
            if client:
                review_data.append({
                    "review_id": review.review_id,
                    "review_comment": review.review_comment,
                    "client_name": client.client_name
                })

        return jsonify({"reviews": review_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/services', methods=['GET'])
def get_services_fp():
    services = Service.query.all()
    services_data = [{"service_id": service.service_id, "service_name": service.service_name} for service in services]
    return jsonify({"services": services_data})

# Route to handle professional signup
@app.route('/signup-professional', methods=['POST'])
def signup_professional():
    data = request.get_json()
    
    new_professional = Professional(
        professional_name=data['professional_name'],
        professional_password=data['professional_password'],
        professional_description=data['professional_description'],
        professional_experience=data['professional_experience'],
        professional_service_type=data['professional_service_type'],
        professional_date_created=datetime.utcnow().isoformat()
    )
    
    db.session.add(new_professional)
    db.session.commit()

    return jsonify({"success": True, "message": "Professional registered successfully"})
