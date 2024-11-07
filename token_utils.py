TOKEN_FILE_PATH = "token.txt"


def save_token(token, username):
    """Saves the login token and username to a text file."""
    try:
        with open(TOKEN_FILE_PATH, 'w') as token_file:
            token_file.write(f"token={token}\n")  # Save token with a key
            token_file.write(f"username={username}\n")  # Save username with a key
        print("Token and username saved successfully.")
    except Exception as e:
        print(f"Error saving token and username: {e}")

def get_token():
    """Retrieves only the login token from the saved file."""
    try:
        with open(TOKEN_FILE_PATH, 'r') as token_file:
            data = token_file.readlines()  # Read all lines
            
            # Find the token in the file
            for line in data:
                if line.startswith("token="):
                    token = line.strip().split('=')[1]
                    return token
            print("Token not found in the file.")
            return None
    except FileNotFoundError:
        print("Token file not found. Please log in first.")
        return None
    except Exception as e:
        print(f"Error retrieving token: {e}")
        return None

def get_username():
    """Retrieves only the username from the saved file."""
    try:
        with open(TOKEN_FILE_PATH, 'r') as token_file:
            data = token_file.readlines()  # Read all lines
            
            # Find the username in the file
            for line in data:
                if line.startswith("username="):
                    username = line.strip().split('=')[1]
                    return username
            print("Username not found in the file.")
            return None
    except FileNotFoundError:
        print("Token file not found. Please log in first.")
        return None
    except Exception as e:
        print(f"Error retrieving username: {e}")
        return None