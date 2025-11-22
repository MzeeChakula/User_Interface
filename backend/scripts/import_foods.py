"""
Import food data from CSV into database
"""
import csv
import sys
from pathlib import Path
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from api.models.database import SessionLocal
from api.models.food import FoodDB


def determine_health_flags(category, sodium, carbs):
    """Determine if food is diabetic/hypertension friendly"""
    # Diabetic friendly: low GI categories and low carbs
    diabetic_friendly = category.lower() in ['vegetables', 'protein'] or carbs < 20

    # Hypertension friendly: low sodium
    hypertension_friendly = sodium < 100  # mg per 100g

    return diabetic_friendly, hypertension_friendly


def estimate_glycemic_index(category, fiber, carbs):
    """Estimate glycemic index based on food properties"""
    if category.lower() == 'vegetables':
        return 15
    elif category.lower() == 'protein':
        return 0
    elif fiber > 5:
        return 40  # High fiber = lower GI
    elif carbs > 30:
        return 70  # High carbs = higher GI
    else:
        return 55  # Medium


def import_foods():
    """Import foods from CSV file"""
    csv_path = Path(__file__).parent / 'food_composition_clean.csv'

    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return

    db = SessionLocal()
    created = 0
    skipped = 0
    errors = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    # Check if food already exists
                    name = row['food_name_english']
                    existing = db.query(FoodDB).filter(FoodDB.name == name).first()
                    if existing:
                        skipped += 1
                        continue

                    # Parse nutritional values (handle empty strings)
                    def parse_float(val, default=0.0):
                        try:
                            return float(val) if val else default
                        except:
                            return default

                    category = row['food_category']
                    sodium = parse_float(row.get('sodium_mg_per_100g', 0))
                    carbs = parse_float(row.get('carbohydrate_g_per_100g', 0))
                    fiber = parse_float(row.get('fiber_g_per_100g', 0))

                    # Determine health flags
                    diabetic_friendly, hypertension_friendly = determine_health_flags(
                        category, sodium, carbs
                    )

                    # Estimate GI
                    gi = estimate_glycemic_index(category, fiber, carbs)

                    # Create food entry
                    food = FoodDB(
                        name=name,
                        local_name=row.get('food_name_luganda') or None,
                        category=category,
                        calories=parse_float(row['energy_kcal_per_100g']),
                        protein=parse_float(row.get('protein_g_per_100g', 0)),
                        carbs=carbs,
                        fats=parse_float(row.get('fat_g_per_100g', 0)),
                        fiber=parse_float(row.get('fiber_g_per_100g')) if row.get('fiber_g_per_100g') else None,
                        vitamin_a=parse_float(row.get('vitamin_a_mcg_per_100g')) if row.get('vitamin_a_mcg_per_100g') else None,
                        vitamin_c=parse_float(row.get('vitamin_c_mg_per_100g')) if row.get('vitamin_c_mg_per_100g') else None,
                        calcium=parse_float(row.get('calcium_mg_per_100g')) if row.get('calcium_mg_per_100g') else None,
                        iron=parse_float(row.get('iron_mg_per_100g')) if row.get('iron_mg_per_100g') else None,
                        potassium=parse_float(row.get('potassium_mg_per_100g')) if row.get('potassium_mg_per_100g') else None,
                        sodium=sodium if sodium > 0 else None,
                        glycemic_index=gi,
                        is_diabetic_friendly=diabetic_friendly,
                        is_hypertension_friendly=hypertension_friendly,
                        description=row.get('notes'),
                        preparation_tips=f"Best prepared: {row.get('preparation_state', 'various methods')}",
                        availability=row.get('seasonality')
                    )

                    db.add(food)
                    created += 1

                    # Commit in batches to avoid rolling back everything on error
                    if created % 100 == 0:
                        try:
                            db.commit()
                            print(f"✓ Committed {created} foods...")
                        except Exception as commit_error:
                            db.rollback()
                            errors.append(f"Batch commit error at {created}: {str(commit_error)}")

                except Exception as e:
                    errors.append(f"Error importing {row.get('food_name_english', 'unknown')}: {str(e)}")

        # Final commit for remaining foods
        try:
            db.commit()
        except Exception as final_error:
            errors.append(f"Final commit error: {str(final_error)}")
        print(f"\nImport complete!")
        print(f"   Created: {created}")
        print(f"   Skipped (duplicates): {skipped}")
        print(f"   Errors: {len(errors)}")

        if errors and len(errors) <= 10:
            print("\nErrors:")
            for error in errors[:10]:
                print(f"   - {error}")

    except Exception as e:
        db.rollback()
        print(f"Import failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting food data import...")
    print("=" * 50)
    import_foods()
