from flask_mail import Message
import os

error_notification_email_address = os.getenv('ERROR_NOTIFICATION_EMAIL_RECIEVER')

def send_email(pr_status, mail, res):
    """
    Sends an email and updates the response dictionary with the status.

    :param pr_status: Boolean indicating PR status.
    :param email_service: Email service to create the email.
    :param mail: Mail sending service.
    :param res: Response dictionary to update with email status.
    """
    msg = create_email_message(pr_status, res)
    try:
        mail.send(msg)
        res['Email_Send'] = True
    except Exception as e:
        res['Email_Send'] = False
        res['Email_Error_Message'] = str(e)



def create_email_message(pr_status, res):
    """
    Generates an email message based on PR card and E-transfer validation results.

    :param pr_status (bool): Indicates if PR validation is required.
    :param res (dict): Response dictionary containing validation results and user details.

    :return Message: An email message object with the appropriate subject, recipients, and body.
    """
    if pr_status and res['PR_Success'] and res['E_Transfer_Success']:
        email_body = f"""
        Dear {res['Full_Name']},

        Thank you for registering for our course! Here are your registration details:
        - PR card validation Success: {res['PR_Success']}
        - E-transfer validation Success: {res['E_Transfer_Success']}
        - Form ID: {res['Form_ID']}
        - Submission ID: {res['Submission_ID']}
        - Full Name: {res['Full_Name']}
        - Email: {res['Email']}
        - Phone Number: {res['Phone_Number']}

        We look forward to seeing you in the course!

        Best regards,
        [Organization's Name]
        """
        recipients = res['Email']
        subject = 'Registration Confirmation: Welcome to Our Course!'
    else:
        errors = []
        if not res.get('PR_Success', True):
            errors.append(res.get('PR_Error', 'PR validation failed'))
        if not res.get('E_Transfer_Success', True):
            errors.append(res.get('E_Transfer_Error', 'E-transfer validation failed'))

        error_message = ' / '.join(errors)
        email_body = f"""
        Dear [Sponsor's Name / Organization's Name],

        An error occurred during form submission:
        - Errors: {error_message}
        - Form ID: {res['Form_ID']}
        - Submission ID: {res['Submission_ID']}
        - Full Name: {res['Full_Name']}
        - Email Address: {res['Email']}
        - Phone Number: {res['Phone_Number']}

        Please address these issues as soon as possible.

        The Customer Form Detail: https://www.jotform.com/inbox/{res['Form_ID']}/{res['Submission_ID']}

        Course Table: https://www.jotform.com/tables/{res['Form_ID']}
        """
        recipients = error_notification_email_address
        subject = 'Error in Form Submission - Action Required'

    return Message(subject=subject, recipients=[recipients], body=email_body)