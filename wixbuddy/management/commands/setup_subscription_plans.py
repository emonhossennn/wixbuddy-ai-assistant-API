from django.core.management.base import BaseCommand
from wixbuddy.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Set up default subscription plans'

    def handle(self, *args, **options):
        plans_data = [
            {
                'name': 'Basic Plan',
                'plan_type': 'basic',
                'billing_cycle': 'monthly',
                'price': 9.99,
                'stripe_price_id': 'price_1Ri0wNR0frcqXXUzpdSFE5Pead4peAwcFRVXG3GwIGiVjCxVoIsX2WTqRrkkWQ8Ina4PD1vB5YqgxW3eBPPjD4fk00nHcKxTFc',
                'features': ['Basic features', 'Email support', '1GB storage']
            },
            {
                'name': 'Basic Plan (Yearly)',
                'plan_type': 'basic',
                'billing_cycle': 'yearly',
                'price': 99.99,
                'stripe_price_id': 'price_1Ri0wNR0frcqXXUzpdSFE5Pead4peAwcFRVXG3GwIGiVjCxVoIsX2WTqRrkkWQ8Ina4PD1vB5YqgxW3eBPPjD4fk00nHcKxTFc',
                'features': ['Basic features', 'Email support', '1GB storage', '2 months free']
            },
            {
                'name': 'Pro Plan',
                'plan_type': 'pro',
                'billing_cycle': 'monthly',
                'price': 19.99,
                'stripe_price_id': 'price_1Ri0wNR0frcqXXUzpdSFE5Pead4peAwcFRVXG3GwIGiVjCxVoIsX2WTqRrkkWQ8Ina4PD1vB5YqgxW3eBPPjD4fk00nHcKxTFc',
                'features': ['Pro features', 'Priority support', '10GB storage', 'Advanced analytics']
            },
            {
                'name': 'Pro Plan (Yearly)',
                'plan_type': 'pro',
                'billing_cycle': 'yearly',
                'price': 199.99,
                'stripe_price_id': 'price_1Ri0wNR0frcqXXUzpdSFE5Pead4peAwcFRVXG3GwIGiVjCxVoIsX2WTqRrkkWQ8Ina4PD1vB5YqgxW3eBPPjD4fk00nHcKxTFc',
                'features': ['Pro features', 'Priority support', '10GB storage', 'Advanced analytics', '2 months free']
            },
            {
                'name': 'Premium Plan',
                'plan_type': 'premium',
                'billing_cycle': 'monthly',
                'price': 39.99,
                'stripe_price_id': 'price_1Ri0wNR0frcqXXUzpdSFE5Pead4peAwcFRVXG3GwIGiVjCxVoIsX2WTqRrkkWQ8Ina4PD1vB5YqgxW3eBPPjD4fk00nHcKxTFc',
                'features': ['Premium features', '24/7 support', 'Unlimited storage', 'Custom integrations', 'White-label options']
            },
            {
                'name': 'Premium Plan (Yearly)',
                'plan_type': 'premium',
                'billing_cycle': 'yearly',
                'price': 399.99,
                'stripe_price_id': 'price_1Ri0wNR0frcqXXUzpdSFE5Pead4peAwcFRVXG3GwIGiVjCxVoIsX2WTqRrkkWQ8Ina4PD1vB5YqgxW3eBPPjD4fk00nHcKxTFc',
                'features': ['Premium features', '24/7 support', 'Unlimited storage', 'Custom integrations', 'White-label options', '2 months free']
            }
        ]

        for plan_data in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                plan_type=plan_data['plan_type'],
                billing_cycle=plan_data['billing_cycle'],
                defaults=plan_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created plan: {plan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Plan already exists: {plan.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully set up subscription plans')
        ) 