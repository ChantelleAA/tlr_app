import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from suggestor.models import Tlr, Material


class Command(BaseCommand):
    help = "Import TLR library from data/tlr_library.csv"

    def handle(self, *args, **options):
        path = Path("data/tlr_library.csv")
        if not path.exists():
            self.stderr.write("CSV not found")
            return
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                tlr, _ = Tlr.objects.get_or_create(
                    strand=row["strand"].strip(),
                    sub_strand=row.get("sub_strand", "").strip(),
                    class_level=row["class_level"].strip(),
                    intended_use=row["intended_use"].strip(),
                    tlr_type=row.get("tlr_type", "").strip(),
                    title=row["title"].strip(),
                    brief_description=row["brief_description"].strip(),
                    time_needed=row.get("time_needed", "lesson").strip(),
                    accessibility_notes=row.get("accessibility_notes", "").strip(),
                    classroom_setup=row.get("classroom_setup", "").strip(),
                    steps_to_make=row["steps_to_make"].strip(),
                    tips_for_use=row.get("tips_for_use", "").strip(),
                )
                for m in row.get("materials", "").split(";"):
                    m = m.strip()
                    if m:
                        mat, _ = Material.objects.get_or_create(name=m)
                        tlr.materials.add(mat)
        self.stdout.write(self.style.SUCCESS("Import complete"))
