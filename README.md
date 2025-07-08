# UnemploymentMachineLearning
# 🛠️ Installation & Setup

### Install Python Dependencies

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt

#Run to reformat information  to  create::  data/processed_unemployment_data.cs   data/sagemaker_input_data.csv: 

python preprocess.py

# Upload datasets to S3 bucketts

aws s3 cp ./data/sagemaker_input_data.csv s3://unemployment-ml-processed-data/sagemaker_input_data.csv
aws s3 cp ./data/processed_unemployment_data.csv s3://unemployment-ml-processed-data/processed_unemployment_data.csv

# Build your IaC

cd terraform
terraform init
terraform apply -var="model_data_url=s3://dummy/dummy.tar.gz"

# Run the training job for Sagemaker

aws s3 ls s3://unemployment-ml-processed-data/model-artifacts/

# Run the  next uncommented lline  to check your output EXAMPLE s3://unemployment-ml-processed-data/model-artifacts/unemployment-xgboost-train-1751864925/output/model.tar.gz

aws s3 ls s3://unemployment-ml-processed-data/model-artifacts/

# Apply again the terraform plan with the updaated url

terraform apply -var="model_data_url=s3://unemployment-ml-processed-data/model-artifacts/unemployment-xgboost-train-1751864925/output/model.tar.gz"

# Run the following to test predictions

python predict.py

# Test locally the Flask app

python app.py

# Post prediction

curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"features": "2025,7,3,25"}'

# If needed to save resources

rm -f terraform.tfstate.lock.info
terraform destroy -var="model_data_url=s3://dummy/dummy.tar.gz" -lock=false

# Always make sure SageMaker endpoints exist before predicting. 
#Use remote state management (backend "s3") for production deployments.
#Update instance types / region variables as needed in variables.tf.
##The predict.py can easily handle multiple future months via its payloads list.
#This setup allows you to train, deploy, and query your ML model fully via AWS CLI + Terraform + Python.







