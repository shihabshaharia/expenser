from django.core.management.base import BaseCommand

# TODO (Person 2): implement this management command
#
# Logic:
#   1. Query all Entry objects where is_recurring=True
#   2. For each recurring entry (template):
#      a. Determine the next due date:
#           last = entry.last_processed_at or entry.date
#           next_date = last + delta(entry.recurrence_frequency)
#           Use timedelta for DAILY/WEEKLY; relativedelta for MONTHLY/YEARLY
#      b. While next_date <= date.today():
#           - Create a new Entry (is_recurring=False) copying user, entry_type,
#             amount, category, description — with date=next_date
#           - Advance: last = next_date; next_date = last + delta
#      c. Save template.last_processed_at = last (update_fields=['last_processed_at'])
#   3. Print a summary of how many instances were created
#
# Imports you will need:
#   from datetime import date, timedelta
#   from dateutil.relativedelta import relativedelta
#   from core.models import Entry


class Command(BaseCommand):
    help = 'Create new entry instances for all due recurring entries.'

    def handle(self, *args, **options):
        # TODO (Person 2): implement
        self.stdout.write('process_recurring: not yet implemented.')
