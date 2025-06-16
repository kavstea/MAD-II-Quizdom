from celery import shared_task
from datetime import datetime
from backend.models import db, User, Subject, Chapter, Quiz, Question, Score
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import csv
import os
from email import encoders
import smtplib
from jinja2 import Template

# ----------------------------------------
# Helper function to send emails (with optional attachment)
# ----------------------------------------
def mail_config(to_address, subject, email_message, attachment=None):
    # Set up SMTP server details (localhost and test port)
    smtp_server_host = 'localhost'
    smtp_server_port = 1025
    sender_email = 'admin@gmail.com'

    # Create a multi-part email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(email_message, 'html'))  # Attach the email body as HTML

    # If an attachment is provided and exists, attach it to the email
    if attachment:
        if os.path.exists(attachment):
            with open(attachment, "rb") as f:
                part = MIMEBase('text', 'csv')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)
        else:
            print("File does not exist")        

    # Send the email using the SMTP server
    with smtplib.SMTP(smtp_server_host, smtp_server_port) as server:
        server.sendmail(sender_email, to_address, msg.as_string())
    print("Email sent successfully")

# ----------------------------------------
# Celery task: Send daily quiz reminders to users
# ----------------------------------------
@shared_task
def daily_reminder():
    users = User.query.all()      # Get all users
    quizzes = Quiz.query.all()    # Get all quizzes
    for user in users:
        if user.user_is_administrator:
            continue  # Skip admin users

        unattempted_quizzes = []
        for quiz in quizzes:
            # Check if the user has already attempted this quiz
            attempt = Score.query.filter_by(user_id_of_score=user.user_id, quiz_id_of_score=quiz.quiz_id).first()
            if not attempt:
                unattempted_quizzes.append(quiz)
        if unattempted_quizzes:
            # Build the email body listing unattempted quizzes
            html_body = build_html_email(user.user_name, unattempted_quizzes)
            # Send the reminder email
            mail_config(
                user.user_email,
                "Daily Reminder: Complete Your Quizzes On Time",
                html_body
            )

# ----------------------------------------
# Helper: Build HTML email listing unattempted quizzes
# ----------------------------------------
def build_html_email(user_name, unattempted_quizzes):
    html_body = f'<p>Hi {user_name},</p>'
    html_body += '<p>Here are the quizzes you have not attempted:</p>'
    html_body += '<ul>'
    for quiz in unattempted_quizzes:
        html_body += f'<li>{quiz.quiz_name}</li>'
    html_body += '</ul>'
    html_body += '<p>Please complete the quizzes as soon as possible. Thank you for using our service! </p>'
    return html_body

# ----------------------------------------
# Celery task: Export a user's quiz scores to CSV and email it to them
# ----------------------------------------
@shared_task
def export_scores(user_id):
    try:
        # Create a reports directory if it doesn't exist
        reports_dir = os.path.join(os.getcwd(), 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        # Name the report file with user ID and date
        report_file = os.path.join(reports_dir, f'{user_id}_quiz_reports_{datetime.now().strftime("%Y-%m-%d")}.csv')

        # Write quiz score data to CSV file
        with open(report_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Quiz ID', 'Quiz Name', 'Scores Obtained', 'Maximum Score', 'Date Attempted'])

            # Query all quizzes and scores for this user
            quizzes = db.session.query(
                Quiz.quiz_id,
                Quiz.quiz_name,
                Score.score_of_user.label('scores_obtained'),
                Score.maximum_score.label('maximum_score'),
                Score.score_release_date.label('date_attempted')
            ).join(Score, Score.quiz_id_of_score == Quiz.quiz_id).filter(Score.user_id_of_score == user_id).all()

            for quiz in quizzes:
                quiz_id, quiz_name, scores_obtained, maximum_score, date_attempted = quiz
                writer.writerow([
                    quiz_id, quiz_name, scores_obtained, maximum_score, date_attempted.strftime('%Y-%m-%d') if date_attempted else ''
                ])
        # Send the CSV file as an email attachment to the user
        user = User.query.get(user_id)
        mail_config(
            user.user_email,
            "Your Quiz Report",
            f"<p>Hi {user.user_name}, please find your quiz report attached.</p>",
            attachment=report_file
        )        
    except Exception as e:   
        print(e)

# ----------------------------------------
# Helper: Send a monthly report email using a Jinja2 HTML template
# ----------------------------------------
def send_email(user, month, quiz_details, total_quizzes, avg_percentage):
    template_path = 'templates/report.html'
    with open(template_path, 'r') as template_file:
        template_file = template_file.read()
    template = Template(template_file)
    html_content = template.render(
        user=user,
        month=month,
        quiz_details=quiz_details,
        total_quizzes=total_quizzes,
        avg_percentage=avg_percentage
    )
    mail_config(
        user.user_email,
        f'Monthly Report for {user.user_name}',
        html_content
    )

# ----------------------------------------
# Celery task: Send monthly quiz performance report to all users (except admins)
# ----------------------------------------
@shared_task
def send_monthly_report():
    users = User.query.filter_by(user_is_administrator=False).all()  # Get all non-admin users
    for user in users:
        month = datetime.now().strftime('%B')
        
        # Get all scores for this user
        scores = Score.query.filter_by(user_id_of_score=user.user_id).all()
        
        # Build a list of quiz details for the report
        quiz_details = []
        for score in scores:
            quiz_details.append({
                "quiz_id": score.quiz.quiz_id if score.quiz else "",
                "quiz_name": score.quiz.quiz_name if score.quiz else "",
                "score_of_user": score.score_of_user,
                "maximum_score": score.maximum_score,
                "score_release_date": score.score_release_date,
            })
        
        total_quizzes = len(quiz_details)
        if total_quizzes > 0:
            avg_percentage = sum(score.score_percentage for score in scores) / total_quizzes
        else:
            avg_percentage = 0
            
        # Send the monthly report email to the user
        send_email(user, month, quiz_details, total_quizzes, avg_percentage)



