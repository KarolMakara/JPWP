# JPWP
```shell
echo "secret = '$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')'" > JPWP/key.py
```
