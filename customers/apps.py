from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'customers'
    verbose_name = 'Clientes'    # O django admin exibirá o nome do app como "Clientes" em vez de "Customers"