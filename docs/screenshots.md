# Correct usage scenarios

* View all accounts: ``http://localhost:1337/accounts/status/``

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/status_all.png)

* Add new account: ``http --json POST http://localhost:1337/accounts/open/ full_name="Арапова Диана Владимировна"``

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/add.png)

* View account by account uuid: ``http://localhost:1337/accounts/status/{account_uuid}``

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/status_by_uuid.png)

* Add money to account: ``http --json PUT http://localhost:1337/accounts/add/ account_uuid="de891155-3dc3-4fa7-a5ef-b711f27ead51" change_amount=1000``

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/add.png)

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/after_addition.png)

* Spend money from account. For example for a delicious breakfast in Simple :)

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/substract.png)

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/after_subtraction.png)

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/afte_clearing_holds.png)

* Close account

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/close.png)


# Incorrect usage scenarios

* Working with incorrect uuid

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/get_account_by_wrong_uuid.png)

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/add_to_wrong_uuid.png)

* Working with closed account

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/add_to_close_account.png)

* Attempt to debit an unavailable amount of money from the account

![Screen](https://github.com/DianaArapova/BankApp/blob/main/docs/screens/wrong_substaction.png)


