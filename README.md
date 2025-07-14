# 📊 Unemployment ML Pipeline on AWS SageMaker

End-to-end ML pipeline to train an unemployment rate predictor using AWS SageMaker, CDK, and XGBoost. Deploys infrastructure via AWS CDK and runs SageMaker Pipelines for training and hosting a real-time inference endpoint.

---

## 🚀 Prerequisites

- AWS CLI installed and configured (`aws configure`)
- Python 3.12+ and `virtualenv`
- Node.js (>= v20.x)
- AWS CDK v2 (`npm install -g aws-cdk`)

---

## 📦 Setup Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install -g aws-cdk

📥 Upload Raw Data to S3

aws s3 cp ./data/unemployment_data.csv s3://unemployment-ml-raw-data/unemployment_data.csv

📝 Prepare Clean Data (if required)

If your training expects no headers or specific columns:

# Remove header
tail -n +2 data/unemployment_data.csv > data/unemployment_data_noheader.csv

# Remove non-numeric columns (e.g., first 3 cols)
cut -d',' -f4-7 data/unemployment_data.csv | tail -n +2 > data/sagemaker_input_data_clean.csv

# Upload processed data to S3
aws s3 cp ./data/sagemaker_input_data_clean.csv s3://unemployment-ml-processed-data/processed_data.csv

⚙️ Deploy Infrastructure via CDK

cd cdk
cdk bootstrap
cdk deploy

This will create:

    Raw & processed S3 buckets

    SageMaker IAM execution role

    SageMaker model (reference to a placeholder model data URL — to update later)

    Endpoint configuration

    Deployed SageMaker endpoint

🏗️ Run SageMaker Pipeline (to train your model)

python cdk/pipeline_run.py

This will:

    Trigger SageMaker pipeline

    Train your XGBoost model

    Upload model artifact to s3://unemployment-ml-processed-data/model-artifacts/<training-job-name>/output/model.tar.gz

Check training job status:

aws sagemaker list-training-jobs --region us-east-1

And describe it:

aws sagemaker describe-training-job --training-job-name <training-job-name>

📦 Update CDK Model Data URL

Once your model artifact is uploaded by the pipeline:

    Open cdk/unemployment_stack.py

    Update:

model_data_url = "s3://unemployment-ml-processed-data/model-artifacts/<training-job-name>/output/model.tar.gz"

Then redeploy:

    cdk deploy

🎯 Predict with New Data

Prepare your test payload (comma-separated, no headers)

Example in predict.py:

payload = "4.2,200000,1"

Then run:

python predict.py

Expected output:

Predicted result: 4.19...

docker run -v ~/.aws:/root/.aws -p 5000:5000 -e SAGEMAKER_ENDPOINT_NAME=your-real-endpoint-name unemployment-predictor


🧹 Clean Up Resources

To safely tear down and clean:

cdk destroy
aws cloudformation delete-stack --stack-name UnemploymentMLStack
aws s3 rm s3://unemployment-ml-processed-data --recursive
aws s3 rm s3://unemployment-ml-raw-data --recursive

📊 Architecture Summary

Raw CSV in S3 →
  [Preprocessing (optional)] →
  SageMaker Training Job →
  Model Artifact in S3 →
  SageMaker Model →
  Endpoint Config →
  Real-time Endpoint →
  Predictions via API

📖 References

    AWS CDK Docs

    SageMaker Pipelines

    SageMaker Python SDK