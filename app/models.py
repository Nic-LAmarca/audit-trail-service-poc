""" 
This module defines the data models for the application. 
The primary model defined in this module is the AuditLogEvent model,
which is used for logging events within the system.
The AuditLogEvent model captures important details about events, such as
the type of event, the time it occurred, the client that generated it, and more.

Classes:
    - AuditLogEvent: Represents an audit log event entry.
    - EventType(Enum): Enum of valid AuditLogEvent event_type field values.
"""
from datetime import datetime
from enum import Enum
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
    #TODO: Discuss with team if any fields or field data could be considered PII (i.e., user_id or details in entity_json) and handle.
    event_id = audit_trail_db.Column(audit_trail_db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    event_type = audit_trail_db.Column(audit_trail_db.String(50), nullable=False)
    created_at = audit_trail_db.Column(audit_trail_db.DateTime, default=lambda: datetime.utcnow(), nullable=False)
    client_id = audit_trail_db.Column(audit_trail_db.String(50), nullable=False)
    user_id = audit_trail_db.Column(audit_trail_db.String(50), nullable=True)
    request_method = audit_trail_db.Column(audit_trail_db.String(10), nullable=False)
    status = audit_trail_db.Column(audit_trail_db.Integer, nullable=True)
    entity_json = audit_trail_db.Column(audit_trail_db.JSON, nullable=True)

class EventType(Enum):
    """
    Enum of valid AuditLogEvent event_type field values.
    This enum is open-ended, where in cases the event_type field 
    is not recognized, it remains treated as a custom, valid event_type.
    This is to meet the requirements defined for the assignment.
    """
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    USER_REGISTERED = "USER_REGISTERED"
    ACCOUNT_CREATED = "ACCOUNT_CREATED"
    ACCOUNT_UPDATED = "ACCOUNT_UPDATED"
    ACCOUNT_DEACTIVATED = "ACCOUNT_DEACTIVATED"
    PAYMENT_PROCESSED = "PAYMENT_PROCESSED"
    BILLING_ADJUSTED = "BILLING_ADJUSTED" 
    REFUND_ISSUED = "REFUND_ISSUED"
    SERVICE_REQUESTED = "SERVICE_REQUESTED"
    SERVICE_COMPLETED = "SERVICE_COMPLETED"
    SERVICE_FAILED = "SERVICE_FAILED"
    SYSTEM_START = "SYSTEM_START"
    SYSTEM_SHUTDOWN = "SYSTEM_SHUTDOWN"
    ERROR_OCCURRED = "ERROR_OCCURRED"
    
    @classmethod 
    def has_value(cls, value):
        return value in cls._value2member_map_
    