import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import ssl
import os 
from dotenv import load_dotenv

load_dotenv() 


smtp_server = os.environ['smtp_server'] 
smtp_port = os.environ['smtp_port'] 
sender_email = os.environ['sender_email'] 
app_password = os.environ['app_password']

# 🎨 Template for selected candidate
SELECTED_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Arial, sans-serif; background-color: #f9fdf9; }}
    .container {{ max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; border: 2px solid #4CAF50; }}
    .title {{ color: #4CAF50; font-size: 24px; font-weight: bold; }}
    .score {{ font-weight: bold; color: #4CAF50; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="title">🎉 Congratulations, {candidate_name}!</div>
    <p>We are thrilled to inform you that based on your performance evaluation, you have been <b>selected</b> for the next stage of the interview process for the role of <b>{job_role}</b>.</p>
    <p>Your evaluation score: <span class="score">{score}/100</span></p>
    <p>Our recruitment team will contact you shortly with further details.</p>
    <p>Based on our Analysis, Here are few points which we liked/disliked about you, We would highly encourage you to check it out</p> 
    <p>{insights}</p> 
    <p>Regards,<br>{company} Software Ltd</p>
  </div>
</body>
</html>
"""

# 🎨 Template for rejected candidate
REJECTED_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Arial, sans-serif; background-color: #fdf9f9; }}
    .container {{ max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; border: 2px solid #f44336; }}
    .title {{ color: #f44336; font-size: 24px; font-weight: bold; }}
    .score {{ font-weight: bold; color: #f44336; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="title">⚠ Application Status: Not Selected</div>
    <p>Dear {candidate_name},</p>
    <p>We appreciate your interest in the role of <b>{job_role}</b>. After reviewing your profile and evaluation, unfortunately you have not been shortlisted for the next stage.</p>
    <p>Your evaluation score: <span class="score">{score}/100</span></p>
    <p>Based on our Analysis, Here are few points which we liked/disliked about you, We would highly encourage you to check it out</p> 
    <p>{insights}</p> 
    <p>We encourage you to apply for future openings at MetricLabs Software Ltd that match your skills and experience.</p>
    <p>Regards,<br>{company} Recruitment Team</p> 
  </div>
</body>
</html>
"""

def send_html_email(smtp_host, smtp_port, username, password, use_ssl,
                    from_name, from_email, to_email, subject, html_body, plain_body):
    """Send HTML + plain text email."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_email))
    msg["To"] = to_email
    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")

    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host=smtp_host, port=smtp_port, context=context) as smtp:
            smtp.login(username, password)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(host=smtp_host, port=smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(username, password)
            smtp.send_message(msg)

def notify_candidate(candidate_name, job_role, score, to_email, company , insights , reason):
    """Choose template based on score and send email."""
    threshold = 65
    if score >= threshold:
        html_body = SELECTED_TEMPLATE.format(candidate_name=candidate_name, job_role=job_role, score=score , company = company , insights = insights, reason=reason)
        plain_body = f"Congratulations {candidate_name}, you have been selected for {job_role}. Score: {score}/100."
        subject = f"🎉 You have been selected for {job_role}"
    else:
        html_body = REJECTED_TEMPLATE.format(candidate_name=candidate_name, job_role=job_role, score=score, company=company , insights = insights, reason=reason)
        plain_body = f"Dear {candidate_name}, we regret to inform you that you were not selected for {job_role}. Score: {score}/100."
        subject = f"Application Status for {job_role}"

    send_html_email(
        smtp_host=smtp_server, 
        smtp_port=smtp_port,
        username=sender_email, 
        password=app_password,  # Use app password for Gmail
        use_ssl=False,
        from_name=f"{company} Hiring Update",
        from_email=sender_email,
        to_email=to_email,
        subject=subject,
        html_body=html_body,
        plain_body=plain_body
    )


# # Example usage after AI scoring
# notify_candidate(
#     candidate_name="Ayush Mishra",
#     job_role="Backend Developer",
#     score=8,  # This comes from your AI score-based analysis
#     to_email="candidate@example.com" , 
#     company = "MetricLabs"
# )
