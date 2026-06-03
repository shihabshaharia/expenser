from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from core.models import Entry


class Command(BaseCommand):
    help = 'Create new entry instances for all due recurring entries.'

    # Map frequency strings to their date delta
    DELTAS = {
        Entry.DAILY:   lambda: timedelta(days=1),
        Entry.WEEKLY:  lambda: timedelta(weeks=1),
        Entry.MONTHLY: lambda: relativedelta(months=1),
        Entry.YEARLY:  lambda: relativedelta(years=1),
    }

    def handle(self, *args, **options):
        today = date.today()
        templates = Entry.objects.filter(is_recurring=True).select_related('category')
        created_count = 0

        for template in templates:
            if not template.recurrence_frequency:
                continue  # misconfigured — skip safely

            delta_fn = self.DELTAS.get(template.recurrence_frequency)
            if delta_fn is None:
                self.stderr.write(
                    f'Unknown frequency "{template.recurrence_frequency}" '
                    f'on entry #{template.pk} — skipping.'
                )
                continue

            # Start from the last processed date, falling back to the entry's own date
            last = template.last_processed_at or template.date
            next_date = last + delta_fn()

            # Generate one new entry per due period up to and including today
            while next_date <= today:
                Entry.objects.create(
                    user=template.user,
                    entry_type=template.entry_type,
                    amount=template.amount,
                    category=template.category,
                    description=template.description,
                    date=next_date,
                    is_recurring=False,   # instance, not template
                )
                created_count += 1
                last = next_date
                next_date = last + delta_fn()

            # Update the template's watermark so we don't duplicate next run
            if last != (template.last_processed_at or template.date):
                template.last_processed_at = last
                template.save(update_fields=['last_processed_at'])

        self.stdout.write(
            self.style.SUCCESS(
                f'process_recurring: {created_count} new instance(s) created '
                f'from {templates.count()} recurring template(s).'
            )
        )
