import random
from faker import Faker

from vendor.models import Vendor
from purchase_order.models import Purchase_order


def main():
    """
    Generate Fake data for db.
    """

    fake = Faker()
    vendor_ids = []

    for _ in range(1, 1000):
        vendor_obj = Vendor.objects.create(name=fake.name(),
                                           contact_details=fake.phone_number(),
                                           address=fake.address(),
                                           vendor_code=fake.uuid4())

        vendor_ids.append(vendor_obj.id)

    for _ in range(1, 1000):
        Purchase_order.objects.create(
            vendor_id=random.choice(vendor_ids)['id'],
            po_number=fake.random_number(10),
            items=fake.json())


if __name__ == "__main__":
    main()
