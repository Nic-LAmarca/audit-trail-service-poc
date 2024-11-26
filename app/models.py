""" 
This module defines the data models for the application. 
The primary model defined in this module is the AuditLogEvent model,
which is used for logging events within the system.
The AuditLogEvent model captures important details about events, such as
the type of event, the time it occurred, the client that generated it, and more.

Classes:
    - AuditLogEvent: Represents an audit log event entry.
"""

from datetime import datetime
import uuid
from . import audit_trail_db

class AuditLogEvent(audit_trail_db.Model):
    """ Represents an audit log entry for tracking events in the system. 
    
    Attributes: 
    event_id (str): Unique identifier for the event in UUID format. If one is not provided, an UUID value will be automatically generated. 
    event_type (str): Type of event (e.g., 'USER_LOGIN'). 
    created_at (datetime): Time when the event occurred. 
    client_id (str): Identifier for the client generating the event. 
    user_id (str, optional): Identifier for the user performing the action. 
    request_method (str): HTTP method used for the request. 
    status (int, optional): Status code of the event captured by the audit log (e.g., 200). 
    entity_json (JSON, optional): the variant data for the event, specific to the given microservice logging it.
    """
    event_id = audit_trail_db.Column(audit_trail_db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    event_type = audit_trail_db.Column(audit_trail_db.String(50), nullable=False) 
    created_at = audit_trail_db.Column(audit_trail_db.DateTime, default=lambda: datetime.utcnow(), nullable=False) 
    client_id = audit_trail_db.Column(audit_trail_db.String(50), nullable=False) 
    user_id = audit_trail_db.Column(audit_trail_db.String(50), nullable=True) 
    request_method = audit_trail_db.Column(audit_trail_db.String(10), nullable=False) 
    status = audit_trail_db.Column(audit_trail_db.Integer, nullable=True) 
    entity_json = audit_trail_db.Column(audit_trail_db.JSON, nullable=True)
    