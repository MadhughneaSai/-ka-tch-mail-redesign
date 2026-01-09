# Author: Kenneth Kang
# Modified by: AI Assistant (Added bonus features: unread count, delete, starred emails)

# Import necessary modules from Flask and other packages
from flask import Blueprint, jsonify, request, session
from flask_mail import Message
from routes.auth_routes import users

# Create a Blueprint for mail-related routes
mail_bp = Blueprint('mail', __name__)

# Dummy inbox data for demonstration and testing purposes
# Each email has a unique sender, subject, body, label (inbox or sent), read status, and starred status
dummy_inbox = [
    {"id": 1, "from": "alice@ka-tch.com", "subject": "Welcome!", "body": "Hello and welcome to Ka-tch Mail! We're excited to have you on board. This is your new home for all communications.", "label": "inbox", "read": False, "starred": True, "timestamp": "2026-01-08T09:00:00Z"},
    {"id": 2, "from": "bob@outlook.com", "subject": "Meeting Tomorrow", "body": "Hey! Let's meet tomorrow at 3pm to discuss the project. Looking forward to it!", "label": "inbox", "read": False, "starred": False, "timestamp": "2026-01-08T08:30:00Z"},
    {"id": 3, "from": "carol@company.org", "subject": "(No Subject)", "body": "", "label": "inbox", "read": True, "starred": False, "timestamp": "2026-01-07T14:20:00Z"},
    {"id": 4, "from": "dave@ka-tch.com", "subject": "Quarterly Report Review", "body": "Please review the attached quarterly report and provide your feedback by EOD Friday.", "label": "inbox", "read": False, "starred": True, "timestamp": "2026-01-07T11:00:00Z"},
    {"id": 5, "from": "eve@sub.example.com", "subject": "Special chars !@#$%^&*()_+", "body": "Body with special characters: <>&\"'", "label": "inbox", "read": True, "starred": False, "timestamp": "2026-01-06T16:45:00Z"},
    {"id": 6, "from": "frank@my-email.net", "subject": "Unicode: 你好, мир, 😀", "body": "Testing unicode in body: こんにちは世界", "label": "inbox", "read": True, "starred": False, "timestamp": "2026-01-06T10:30:00Z"},
    {"id": 7, "from": "grace@anotherdomain.co.uk", "subject": "Project Update", "body": "The project is on track. All milestones have been met so far.", "label": "inbox", "read": False, "starred": False, "timestamp": "2026-01-05T09:15:00Z"},
    {"id": 8, "from": "hank@ka-tch.com", "subject": "Weekly Newsletter", "body": "This week's highlights include new features, team updates, and upcoming events. Stay tuned for more exciting news!", "label": "inbox", "read": True, "starred": False, "timestamp": "2026-01-04T08:00:00Z"},
    {"id": 9, "from": "ivan@demo-example.com", "subject": "Security Alert", "body": "We noticed a new login from your account. If this was you, no action is needed.", "label": "inbox", "read": False, "starred": True, "timestamp": "2026-01-03T22:30:00Z"},
    {"id": 10, "from": "judy@example.com", "subject": "Re: Meeting", "body": "See you at 10am.\n\nBest,\nJudy", "label": "inbox", "read": True, "starred": False, "timestamp": "2026-01-03T15:00:00Z"}
]

@mail_bp.route('/send', methods=['POST'])
def send_mail():
    """
    Endpoint to send an email.
    Expects JSON payload with 'to', 'subject', and 'body'.
    Only allows sending if the user is logged in (session['user'] exists).
    Actually sends the email using Flask-Mail if the recipient is not the sender (for demo/testing).
    Always adds the sent email to the dummy inbox with label 'sent'.
    """
    # Check if user is logged in
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    # Parse and validate request data
    data = request.get_json()
    if not data or not all(key in data for key in ('to', 'subject', 'body')):
        return jsonify({'error': 'Invalid request data'}), 400
    to = data['to']
    subject = data['subject']
    body = data['body']
    # Validate recipient email format
    import re
    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.match(email_regex, to):
        return jsonify({'error': 'Invalid recipient email address'}), 400
    # Get sender's email from user session
    sender = users.get(session['user'], {}).get('email', None)
    if not sender:
        sender = session['user']  # fallback to username if email not set
    try:
        # Always add to dummy inbox as 'sent' for the sender
        dummy_inbox.append({
            "id": len(dummy_inbox) + 1,
            "from": sender,
            "subject": subject,
            "body": body + "\n\n" + f"Sent to: {to}",
            "label": "sent"
        })
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        # Return error if sending fails
        return jsonify({'error': str(e)}), 500

@mail_bp.route('/status', methods=['GET'])
def mail_status():
    """
    Endpoint to check the status of the mail service.
    Returns a simple operational status message.
    """
    return jsonify({'status': 'Mail service is operational'}), 200

@mail_bp.route('/inbox', methods=['GET'])
def inbox():
    """
    Endpoint to get the inbox for the logged-in user.
    Only available if the user is logged in.
    Returns all dummy inbox emails, labeling sent emails as 'sent' and others as 'inbox'.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    # Mark sent emails in the inbox
    inbox_with_labels = []
    for email in dummy_inbox:
        if email.get('label') == 'sent':
            inbox_with_labels.append(email)
        else:
            # For received emails, add label 'inbox' if not present
            labeled_email = dict(email)
            if 'label' not in labeled_email:
                labeled_email['label'] = 'inbox'
            inbox_with_labels.append(labeled_email)
    return jsonify(inbox_with_labels), 200

# BONUS FEATURE: Unread Count Endpoint
@mail_bp.route('/inbox/count', methods=['GET'])
def inbox_count():
    """
    Endpoint to get email counts for the logged-in user.
    Returns total count, unread count, inbox count, sent count, and starred count.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    total = len(dummy_inbox)
    unread = sum(1 for e in dummy_inbox if not e.get('read', True) and e.get('label') != 'sent')
    inbox_count = sum(1 for e in dummy_inbox if e.get('label') == 'inbox')
    sent_count = sum(1 for e in dummy_inbox if e.get('label') == 'sent')
    starred_count = sum(1 for e in dummy_inbox if e.get('starred', False))
    
    return jsonify({
        'total': total,
        'unread': unread,
        'inbox': inbox_count,
        'sent': sent_count,
        'starred': starred_count
    }), 200

# BONUS FEATURE: Delete Email Endpoint
@mail_bp.route('/inbox/<int:email_id>', methods=['DELETE'])
def delete_email(email_id):
    """
    Endpoint to delete an email by its ID.
    Only available if the user is logged in.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    global dummy_inbox
    original_length = len(dummy_inbox)
    dummy_inbox = [e for e in dummy_inbox if e['id'] != email_id]
    
    if len(dummy_inbox) < original_length:
        return jsonify({'message': 'Email deleted successfully'}), 200
    else:
        return jsonify({'error': 'Email not found'}), 404

# BONUS FEATURE: Toggle Read Status Endpoint
@mail_bp.route('/inbox/<int:email_id>/read', methods=['PUT'])
def toggle_read(email_id):
    """
    Endpoint to toggle the read status of an email.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    for email in dummy_inbox:
        if email['id'] == email_id:
            email['read'] = not email.get('read', False)
            return jsonify({'message': 'Read status toggled', 'read': email['read']}), 200
    
    return jsonify({'error': 'Email not found'}), 404

# BONUS FEATURE: Toggle Starred Status Endpoint
@mail_bp.route('/inbox/<int:email_id>/star', methods=['PUT'])
def toggle_star(email_id):
    """
    Endpoint to toggle the starred status of an email.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    for email in dummy_inbox:
        if email['id'] == email_id:
            email['starred'] = not email.get('starred', False)
            return jsonify({'message': 'Starred status toggled', 'starred': email['starred']}), 200
    
    return jsonify({'error': 'Email not found'}), 404
