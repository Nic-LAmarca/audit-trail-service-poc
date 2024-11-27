"""
This module defines the APIs for the audit-trail-service.
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from .models import AuditLogEvent, EventType
from . import audit_trail_db

main = Blueprint('main', __name__)

@main.route('/event', methods=['POST'])
def add_audit_log_event ():
    """
    Adds a new AuditLogEvent to the database.

    TODO: Implement authorization and authentication of the client here to ensure that
    they are allowed to be adding to this database.

    ### Request Headers
    - `X-Client-ID` _(string, required)_: The ID of the client making the request.
    - `Content-Type` _(string, required)_: application/json

    ### Request Body
    - `event_type` _(string, required)_: The type of event.
    - `status` _(integer, optional)_: The status code of the event.
      (TODO: Create enum class for status codes)
    - `entity_json` _(JSON, optional)_: Additional data specific to the event.

    ### Responses
    #### 201 Created
    ```json
    {
        "message": "Audit Log Event added successfully."
    }
    ```

    #### 400 Bad Request
    ```json
    {
        "error": "Invalid JSON provided.", "message": "Detailed error message."
    }
    ```
    ```json
    {
        "error": "Client ID is required"
    }
    ```
    ```json
    {
        "error": "User ID is required"
    }
    ```
    ```json
    {
        "error": "event_type is required"
    }
    ```
    ```json
    {
        "error": "Invalid event_type"
    }
    ```

    #### 500 Internal Server Error
    ```json
    {
        "error": "Database error", "message": "Detailed error message."
    }
    ```
    ```json
    {
        "error": "An unexpected error occurred", "message": "Detailed error message."
    }
    ```

    ### Example Request
    #### Request
    ```http
    POST /event HTTP/1.1
    Host: example.com
    Content-Type: application/json
    X-Client-ID: client123
    {
        "event_type": "USER_LOGIN",
        "user_id": "user1",
        "status": 200,
        "entity_json": {
            "key": "value"
        }
    }
    ```

    #### Response
    **201 Created**
    ```json
    {
        "message": "Audit Log Event added successfully."
    }
    ```
    """
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': 'Invalid JSON provided.', 'message': str(e)}), 400

    client_id = request.headers.get('X-Client-ID')
    user_id = data.get('user_id')
    request_method = request.method
    # TODO: Create enum class for status codes and handle appropriately
    status = data.get('status')
    event_type = data['event_type']

    if not event_type:
        return jsonify({'error': 'event_type is required'}), 400

    # If event_type is present in Enum, use the associated value. Else treat it as a custom type.
    if EventType.has_value(event_type):
        event_type = EventType[event_type].value

    if not client_id:
        return jsonify({'error': 'Client ID is required'}),400

    # TODO: Validate the caller has the required permissions to add a new entry to this db
    try:
        new_audit_log_event = AuditLogEvent(
            event_type=event_type,
            client_id=client_id,
            user_id=user_id,
            request_method = request_method,
            status=status,
            entity_json=data.get('entity_json')
        )

        audit_trail_db.session.add(new_audit_log_event)
        audit_trail_db.session.commit()
    except SQLAlchemyError as e:
        # Rollback in case of database error
        audit_trail_db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'message': str(e)}), 500

    return jsonify({'message': 'Audit Log Event added successfully.'}), 201

@main.route('/event/<string:event_id>', methods=['GET'])
def get_audit_log_event(event_id):
    """
    Retrieves a specific AuditLogEvent by its event_id.

    TODO: Implement authorization and authentication of the client here to ensure that
    they are allowed to be accessing this resource (i.e., general access to audit log events
    or audit log events that are for a specific microservice).

    ### Request Headers
    - `X-Client-ID` _(string, required)_: The ID of the client making the request.

    ### Responses
    #### 200 OK
    ```json
    {
        "event_id": "event_id",
        "event_type": "USER_LOGIN",
        "created_at": "2024-04-06T14:00:00Z",
        "client_id": "client123",
        "user_id": "user456",
        "request_method": "POST",
        "status": 200,
        "entity_json": { "key": "value" }
    }
    ```

    #### 400 Bad Request
    ```json
    {
        "error": "Client ID is required"
    }
    ```

    #### 404 Not Found
    ```json
    {
        "error": "Event not found"
    }
    ```

    #### 500 Internal Server Error
    ```json
    {
        "error": "An unexpected error occurred",
        "message": "Detailed error message."
    }
    ```
    """
    client_id = request.headers.get('X-Client-ID')


    #TODO: Validate the caller has the required permissions to access this resource.
    #  For now ensure client_id is present.
    if not client_id:
        return jsonify({'error': 'Client ID is required'}), 400

    try:
        requested_audit_log_event = AuditLogEvent.query.filter_by(event_id=event_id).first()
        if not requested_audit_log_event:
            return jsonify({'error': 'Event not found'}), 404

        return jsonify({
            'event_id': requested_audit_log_event.event_id,
            'event_type': requested_audit_log_event.event_type,
            'created_at': requested_audit_log_event.created_at,
            'client_id': requested_audit_log_event.client_id,
            'user_id': requested_audit_log_event.user_id,
            'request_method': requested_audit_log_event.request_method,
            'status': requested_audit_log_event.status,
            'entity_json': requested_audit_log_event.entity_json
        }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'message': str(e)}), 500

@main.route('/events', methods=['GET'])
def get_all_audit_log_events():
    """
    Retrieves all AuditLogEvents.

    TODO: Implement authorization and authentication of the client here to ensure that
    they are allowed to be accessing this resource. In addition, have a discussion with
    the team on if this endpoint should return all entries, or if it should return only
    those which corespond to the client that is making the given request:
    - i.e., Client A can only read entries that have a matching client_id value to it
      (that of Client A), whereas entries corresponding to Client B would not be returned.
    - With this, it would then bring up the discussion of if users/clients with an Admin
      role can exist, and only they could access all entries belonging to any microservice.

    ### Request Headers
    - `X-Client-ID` _(string, required)_: The ID of the client making the request.

    ### Responses
    #### 200 OK
    ```json
    [
        {
            "event_id": "event_id",
            "event_type": "USER_LOGIN",
            "created_at": "2024-04-06T14:00:00Z",
            "client_id": "client123",
            "user_id": "user456",
            "request_method": "POST",
            "status": 200,
            "entity_json": { "key": "value" }
        },
        ...
    ]
    ```

    #### 400 Bad Request
    ```json
    {
        "error": "Client ID is required"
    }
    ```

    #### 500 Internal Server Error
    ```json
    {
        "error": "An unexpected error occurred",
        "message": "Detailed error message."
    }
    ```
    """
    client_id = request.headers.get('X-Client-ID')
    #TODO: Validate the caller has the required permissions to access this resource.
    # For now ensure client_id is present.
    if not client_id:
        return jsonify({'error': 'Client ID is required'}), 400

    try:
        # Currently retrieves all events without filtering.
        audit_log_events = AuditLogEvent.query.all()
        audit_log_event_list = [
            {
                'event_id': event.event_id,
                'event_type': event.event_type,
                'created_at': event.created_at,
                'client_id': event.client_id,
                'user_id': event.user_id,
                'request_method': event.request_method,
                'status': event.status,
                'entity_json': event.entity_json
            } for event in audit_log_events
        ]

        return jsonify(audit_log_event_list), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'message': str(e)}), 500
