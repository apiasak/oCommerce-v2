from .models import Customer

def save_customer(backend, user, response, *args, **kwargs):
    try:
        customer = Customer.objects.get(user_id=user.id)
    except Customer.DoesNotExist:
        customer = Customer(user_id=user.id)

    if backend.name == 'facebook':
        customer.email = response.get('email')
        print(response.get('email'))
        customer.photo = 'http://graph.facebook.com/%s/picture?type=large' % response.get('id')
        customer.save()