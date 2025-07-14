from flask import Flask, render_template, request
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# 🔐 SageMaker Runtime client
runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")

# 📌 Hardcoded endpoint name (or make configurable)
ENDPOINT_NAME = "SageMakerEndpoint-asoVIzNLjgal"

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        input_values = request.form.get("input")
        if not input_values:
            error = "Please enter input values."
        else:
            try:
                response = runtime.invoke_endpoint(
                    EndpointName=ENDPOINT_NAME,
                    ContentType="text/csv",
                    Body=input_values
                )
                prediction = response["Body"].read().decode("utf-8").strip()
            except ClientError as e:
                error = f"❌ Prediction failed: {e.response['Error']['Message']}"

    return render_template("index.html", prediction=prediction, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

