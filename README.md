# CloudQuiz: AWS Deployment Guide

This guide walks you through deploying the CloudQuiz platform using **AWS EC2, RDS, and S3**. It includes special instructions for deploying the app entirely within the **AWS Free Tier**.

## Architecture Overview
- **Amazon S3**: Hosts the HTML, CSS, and JS files for the frontend.
- **Amazon EC2**: Runs the Python Flask backend API using Gunicorn.
- **Amazon RDS**: Stores user credentials, quizzes, questions, and attempt logs (MySQL).

---

## 1. Local Development / Testing

Before pushing to AWS, you can test the backend locally using an SQLite DB or local MySQL:

```bash
cd backend
pip install -r requirements.txt

# Run the backend process:
python app.py
```
> Ensure your frontend `js/api.js` points to `localhost:5000` (it does by default).
> Open `frontend/index.html` in your browser.

---

## 2. Fast Free Tier Deployment (CloudFormation)

I have provided an Infrastructure-as-Code template (`aws/cloudformation.yaml`) pre-configured to ONLY use Free Tier eligible instances (`t2.micro` and `db.t3.micro`).

1. Log in to the AWS Console and search for **CloudFormation**.
2. Click **Create stack** -> **With new resources (standard)**.
3. Select **Upload a template file** and upload `aws/cloudformation.yaml`.
4. Fill in the Stack details:
   - **Stack name**: `CloudQuizPlatform`
   - **DBPassword**: Enter a secure password
   - **S3BucketName**: Enter a globally unique name
5. Click Next through all the screens, check the IAM permission box, and click **Submit**.
6. Wait for the stack to reach `CREATE_COMPLETE`.

---

## 3. Manual Free Tier Deployment (Step-by-Step)

If you prefer to build it yourself using the AWS Console, follow these exact steps to stay within the 12-month Free Tier limits:

### A. The Database (Amazon RDS)
*Limit: 750 hours/month of db.t3.micro or db.t4g.micro*
1. Go to **RDS** -> **Create database**. Select **MySQL**.
2. **Crucial**: Under Templates, choose **Free tier** to avoid surprise charges.
3. Name the instance `quizdb`. Set Master username to `quizadmin` and create a secure password.
4. Under Connectivity, select **Yes** for Public access.
5. Click **Create database**. When finished, copy the "Endpoint" URL.

### B. The Backend (Amazon EC2)
*Limit: 750 hours/month of a t2.micro or t3.micro instance*
1. Go to **EC2** -> **Launch Instances**.
2. Name the instance `Quiz-Backend`.
3. Select **Amazon Linux 2023** AMI and the **t2.micro** Instance Type (both Free tier eligible).
4. Create or select a Key Pair.
5. Check the boxes to **Allow SSH traffic** and **Allow HTTP traffic**.
6. Launch instance. Once running, go to its Security Group and add an Inbound Rule for **Custom TCP, Port 5000** (Anywhere IPv4).

### C. Connect EC2 and RDS
1. Connect to your EC2 instance via SSH or "EC2 Instance Connect".
2. Upload or clone your `backend/` code folder into `/opt/cloudquiz`.
3. Inside `backend/`, create a `.env` file replacing `DB_HOST` and `DB_PASS` with your RDS info:
   ```env
   DB_HOST=your-rds-endpoint.cxyz123.us-east-1.rds.amazonaws.com
   DB_USER=quizadmin
   DB_PASS=YourSecurePassword!
   DB_NAME=quizdb
   SECRET_KEY=long-random-string
   CORS_ORIGINS=*
   ```
4. Run the setup script to start the server:
   ```bash
   chmod +x aws/setup_ec2.sh
   sudo ./aws/setup_ec2.sh
   ```

### D. The Frontend (Amazon S3)
*Limit: 5GB of standard storage*
1. Locate `frontend/js/api.js` on your computer. Change the `baseURL` from `localhost` to your EC2's Public IP (`http://<EC2_PUBLIC_IP>:5000/api`).
2. Go to **S3** -> **Create bucket**. Uncheck **Block all public access**.
3. Open the new bucket -> **Properties** tab -> scroll down to **Enable Static website hosting** (index document: `index.html`).
4. **Permissions** tab -> **Bucket Policy**. Paste the contents of `aws/s3_policy.json` (replacing `YOUR-BUCKET-NAME-HERE`).
5. Upload all the files inside your `frontend/` folder directly into the bucket.
6. Click the Bucket Website Endpoint URL in the Properties tab. Your free cloud app is live!

---

## Demo Accounts

If you seeded the database using `seed.sql`, the following accounts are available:
- **Admin Login**: `admin@quiz.com` / `Admin@123`
- **Student Login**: `student@quiz.com` / `Student@123`
