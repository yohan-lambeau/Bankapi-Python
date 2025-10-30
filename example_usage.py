#!/usr/bin/env python3
"""
Example script demonstrating how to use the Banking API.
Make sure the server is running before executing this script:
    uvicorn app.main:app --reload
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Print formatted response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    """Run example API calls."""
    print("Banking API Example Usage")
    print("="*60)
    
    # 1. Register a new user
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepass123",
        "full_name": "John Doe"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print_response("1. Register User", response)
    
    # 2. Login and get token
    login_data = {
        "username": "johndoe",
        "password": "securepass123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response("2. Login", response)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Create a checking account
        account_data = {
            "account_type": "checking",
            "currency": "USD"
        }
        response = requests.post(f"{BASE_URL}/accounts/", json=account_data, headers=headers)
        print_response("3. Create Checking Account", response)
        
        if response.status_code == 201:
            account_id = response.json()["id"]
            
            # 4. Create a savings account
            account_data = {
                "account_type": "savings",
                "currency": "USD"
            }
            response = requests.post(f"{BASE_URL}/accounts/", json=account_data, headers=headers)
            print_response("4. Create Savings Account", response)
            
            # 5. Get all accounts
            response = requests.get(f"{BASE_URL}/accounts/", headers=headers)
            print_response("5. Get All Accounts", response)
            
            # 6. Deposit money
            transaction_data = {
                "transaction_type": "deposit",
                "amount": 1000.00,
                "description": "Initial deposit"
            }
            response = requests.post(f"{BASE_URL}/transactions/{account_id}", json=transaction_data, headers=headers)
            print_response("6. Deposit Money", response)
            
            # 7. Get account details
            response = requests.get(f"{BASE_URL}/accounts/{account_id}", headers=headers)
            print_response("7. Get Account Details (After Deposit)", response)
            
            # 8. Withdraw money
            transaction_data = {
                "transaction_type": "withdrawal",
                "amount": 250.00,
                "description": "ATM withdrawal"
            }
            response = requests.post(f"{BASE_URL}/transactions/{account_id}", json=transaction_data, headers=headers)
            print_response("8. Withdraw Money", response)
            
            # 9. Get transaction history
            response = requests.get(f"{BASE_URL}/transactions/{account_id}", headers=headers)
            print_response("9. Get Transaction History", response)
            
            # 10. Get final account balance
            response = requests.get(f"{BASE_URL}/accounts/{account_id}", headers=headers)
            print_response("10. Final Account Balance", response)
    
    print(f"\n{'='*60}")
    print("Example completed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Make sure the server is running:")
        print("    uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\nError: {e}")
