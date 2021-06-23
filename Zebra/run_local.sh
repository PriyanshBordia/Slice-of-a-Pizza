choice=$1

while : $choice > 3 || $choice == "view";
do
    if [[ $choice == view ]]
    then
        open orders/views.py
        break

    elif [[ $choice == 1 ]]
    then
        python3 manage.py runserver
        break

    elif [[ $choice == 2 ]]
    then
        python3 manage.py makemigrations
        break

    elif [[ $choice == 3 ]]
    then
        python3 manage.py migrate
        break

    fi
done
