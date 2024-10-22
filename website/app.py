from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import pymysql
import socket

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages

# S3 and RDS configuration (Update with your values or environment variables)
s3 = boto3.client('s3')
rds_host = "your-rds-endpoint"
rds_user = "your-username"
rds_password = "your-password"
rds_db = "your-database"
rds_port = 3306  # Update if needed

# Route to display the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    ec2_hostname = socket.gethostname()
    ec2_ip = request.remote_addr
    
    if request.method == 'POST':
        if 'test_db' in request.form:
            # Handle DB connection testing
            host = request.form['db_host']
            db_name = request.form['db_name']
            username = request.form['db_user']
            password = request.form['db_pass']
            port = int(request.form['db_port'])

            try:
                conn = pymysql.connect(host=host, user=username, password=password, db=db_name, port=port)
                flash("Connected to database successfully!", "success")
            except Exception as e:
                flash(f"Failed to connect to database: {str(e)}", "danger")

        elif 'upload_file' in request.form:
            # Handle file upload to S3
            bucket_name = request.form['bucket_name']
            file = request.files['file']
            if file:
                try:
                    s3.upload_fileobj(file, bucket_name, file.filename)
                    file_url = f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"
                    flash(f"File uploaded successfully! Download URL: {file_url}", "success")
                except Exception as e:
                    flash(f"Failed to upload file: {str(e)}", "danger")
    
    return render_template('index.html', ec2_hostname=ec2_hostname, ec2_ip=ec2_ip)

if __name__ == "__main__":
    app.run(debug=True)
