if [[ 7 ]]
then
    python3 manage.py runserver

elif [[ 2 ]]
then
    python3 manage.py makemigrations

elif [[ 3 ]]
then
    python3 manage.py migrate

# else
#     echo "Enter a valid choice!"
fi
