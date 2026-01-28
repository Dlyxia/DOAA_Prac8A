import pytest
import time
import requests
import base64
import io
from PIL import Image
from application.routes import url as model_url

def wait_for_model_server(timeout=120, interval=5):
    """
    Wait for the TensorFlow Serving model server to be ready.
    Render free tier can take a while to spin up (cold start).
    """
    # TF Serving model status URL is usually /v1/models/<model_name>
    # Our url is /v1/models/digit_classifier:predict
    status_url = model_url.split(':predict')[0]
    
    start_time = time.time()
    print(f"\nChecking model server availability at {status_url}...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(status_url, timeout=10)
            if response.status_code == 200:
                print("Model server is UP and ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"Model server not ready yet, retrying in {interval}s...")
        time.sleep(interval)
    
    return False

def test_index_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"canvas" in response.data.lower()

def test_predict_endpoint(client):
    """
    Test the /predict endpoint with a dummy base64 image.
    This test will wait for the model server to start if it's in a cold state.
    """
    # 1. Wait for model server (Render cold start handling)
    if not wait_for_model_server():
        pytest.fail("Model server failed to start within timeout period.")

    # 2. Create a dummy 280x280 white image with a black stroke (simulating canvas)
    img = Image.new('RGB', (280, 280), color='white')
    # Just a simple dot to represent 'something' on the canvas
    img.putpixel((140, 140), (0, 0, 0)) 
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    data_url = f"data:image/png;base64,{img_str}"

    # 3. Post to /predict
    response = client.post('/predict', data=data_url)
    
    # 4. Assertions
    assert response.status_code == 200
    # The response should be a digit (0-9)
    prediction = response.data.decode('utf-8')
    assert prediction.isdigit()
    assert 0 <= int(prediction) <= 9
