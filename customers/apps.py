from django.apps import AppConfig


class CustomersConfig(AppConfig):
    name = 'customers'
    verbose_name = 'Cliente'    # O django admin exibirá o nome do app como "Cliente" em vez de "Customers"
    verbose_name_plural = 'Clientes'