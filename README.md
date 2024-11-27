# notes-syn-with-drive-template

run python -m venv venv

pip install -r requirements.txt

touch client_secrets.json

go to google dev console and create oauth cred follow the below steps

  Select ‘Application type’ to be Web application.
  Enter an appropriate name.
  Input http://localhost:8080 for ‘Authorized JavaScript origins’.
  Input http://localhost:8080/ for ‘Authorized redirect URIs’.
  Click ‘Save’.

copy paste the downloaded content to client_secrets.json

run upload_wikis.py

make necessary changes

and run pyinstaller -F upload_wikis.py

and use the generated executable
