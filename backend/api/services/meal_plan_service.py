"""
Meal Plan Generation Service using ML Models
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from api.models.loader import ModelLoader
from api.models.food import FoodDB
from api.models.database import get_db

logger = logging.getLogger(__name__)


class MealPlanService:
    """Generate personalized meal plans using ML models"""

    def __init__(self, model_loader: ModelLoader, db: Optional[Session] = None):
        self.model_loader = model_loader
        self.db = db

        # Fallback food database (used if DB is empty)
        self.fallback_foods_db = {
            'matooke': {'calories': 122, 'category': 'staple', 'protein': 1.3, 'carbs': 31},
            'beans': {'calories': 127, 'category': 'protein', 'protein': 8.7, 'carbs': 22.8},
            'nakati': {'calories': 23, 'category': 'vegetable', 'protein': 2.6, 'carbs': 3.7},
            'posho': {'calories': 96, 'category': 'staple', 'protein': 2, 'carbs': 21},
            'cassava': {'calories': 160, 'category': 'staple', 'protein': 1.4, 'carbs': 38},
            'sweet_potatoes': {'calories': 86, 'category': 'staple', 'protein': 1.6, 'carbs': 20},
            'groundnuts': {'calories': 567, 'category': 'protein', 'protein': 25.8, 'carbs': 16.1},
            'fish': {'calories': 206, 'category': 'protein', 'protein': 22, 'carbs': 0},
            'sukuma_wiki': {'calories': 50, 'category': 'vegetable', 'protein': 4.3, 'carbs': 10},
            'g_nut_sauce': {'calories': 188, 'category': 'sauce', 'protein': 7.6, 'carbs': 7.2},
        }

    def _get_db_session(self) -> Session:
        """Get database session"""
        if self.db is None:
            return next(get_db())
        return self.db

    def _get_foods_from_db(self, conditions: List[str]) -> List[Dict]:
        """Get foods from database based on conditions"""
        try:
            db = self._get_db_session()
            query = db.query(FoodDB)

            # Filter by health conditions
            if 'diabetes' in [c.lower() for c in conditions]:
                query = query.filter(FoodDB.is_diabetic_friendly == True)
            if 'hypertension' in [c.lower() for c in conditions]:
                query = query.filter(FoodDB.is_hypertension_friendly == True)

            foods = query.limit(20).all()

            if not foods:
                logger.warning("No foods found in database, using fallback")
                return []

            # Convert to dict format
            return [
                {
                    'name': food.name,
                    'local_name': food.local_name,
                    'category': food.category,
                    'calories': food.calories,
                    'protein': food.protein,
                    'carbs': food.carbs,
                    'fats': food.fats
                }
                for food in foods
            ]

        except Exception as e:
            logger.error(f"Failed to get foods from database: {e}")
            return []

    def generate_meal_plan(
        self,
        age: int,
        health_conditions: List[str],
        preferred_foods: List[str],
        name: str = "Patient"
    ) -> Dict:
        """
        Generate a 7-day meal plan using ML models

        Args:
            age: Patient age
            health_conditions: List of conditions (e.g., ['diabetes', 'hypertension'])
            preferred_foods: List of preferred foods
            name: Patient name

        Returns:
            Dict with meal plan, shopping list, and tips
        """
        try:
            # 1. Calculate caloric needs using ML model
            caloric_needs = self._calculate_caloric_needs(age, health_conditions)

            # 2. Get food recommendations based on conditions
            recommended_foods = self._get_food_recommendations(
                health_conditions,
                preferred_foods
            )

            # 3. Generate 7-day meal plan
            meal_plan = self._create_weekly_plan(
                caloric_needs,
                recommended_foods,
                health_conditions
            )

            # 4. Generate shopping list
            shopping_list = self._generate_shopping_list(meal_plan)

            # 5. Generate health tips
            tips = self._generate_health_tips(health_conditions)

            return {
                'success': True,
                'patient_name': name,
                'caloric_needs': caloric_needs,
                'meal_plan': meal_plan,
                'shopping_list': shopping_list,
                'tips': tips,
                'generated_at': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Meal plan generation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _calculate_caloric_needs(self, age: int, conditions: List[str]) -> int:
        """Use ML model to calculate daily caloric needs"""
        try:
            # Prepare input for model
            input_data = {
                'age': age,
                'has_diabetes': 1 if 'diabetes' in [c.lower() for c in conditions] else 0,
                'has_hypertension': 1 if 'hypertension' in [c.lower() for c in conditions] else 0,
                # Add default values for other required features
            }

            # Get prediction from model (HF -> XGBoost -> offline)
            result = self.model_loader.predict(input_data, model_preference='auto')

            if result['success']:
                return int(result['prediction']['caloric_needs'])
            else:
                # Fallback calculation
                return self._fallback_caloric_calculation(age)

        except Exception as e:
            logger.warning(f"Model prediction failed, using fallback: {e}")
            return self._fallback_caloric_calculation(age)

    def _fallback_caloric_calculation(self, age: int) -> int:
        """Simple fallback caloric calculation"""
        # Elderly baseline: 1600-2000 kcal/day
        if age >= 80:
            return 1600
        elif age >= 70:
            return 1800
        else:
            return 2000

    def _get_food_recommendations(
        self,
        conditions: List[str],
        preferred: List[str]
    ) -> List[str]:
        """Get food recommendations using ensemble ML models"""
        
        # Try to use ensemble models for recommendations
        try:
            ensemble = self.model_loader.models.get('ensemble', {})
            
            if ensemble.get('available'):
                logger.info("Using ensemble models for food recommendations")
                
                # Create a query based on health conditions
                # For now, we'll get general recommendations and filter by conditions
                # You can enhance this by creating condition-specific query vectors
                
                # Get recommendations from the ensemble
                recommendations = self.model_loader.recommend_foods(
                    top_k=15  # Get more recommendations to filter
                )
                
                if recommendations.get('success') and recommendations.get('items'):
                    # Extract food IDs from recommendations
                    recommended_foods = []
                    
                    for item in recommendations['items']:
                        food_id = item.get('id', '')
                        # Extract food name from ID (format: model_name_index)
                        # We'll use the ID as-is for now, or extract from metadata
                        if food_id:
                            recommended_foods.append(food_id)
                    
                    # Add preferred foods
                    for food in preferred:
                        food_lower = food.lower().strip()
                        if food_lower not in recommended_foods:
                            recommended_foods.append(food_lower)
                    
                    logger.info(f"Got {len(recommended_foods)} recommendations from ensemble models")
                    return recommended_foods[:8]
                else:
                    logger.warning("Ensemble recommendation failed, using fallback")
            else:
                logger.info("Ensemble models not available, using database/fallback")
        
        except Exception as e:
            logger.error(f"Error using ensemble models for recommendations: {e}")
        
        # Fallback: Try database first
        db_foods = self._get_foods_from_db(conditions)

        if db_foods:
            # Use database foods
            recommended = [food['name'].lower().replace(' ', '_') for food in db_foods[:8]]

            # Add preferred foods if mentioned
            for food in preferred:
                food_lower = food.lower().strip()
                if food_lower not in recommended:
                    recommended.append(food_lower)

            return recommended[:8]

        # Final fallback to hardcoded recommendations
        recommended = []

        # Base recommendations for elderly
        base_foods = ['matooke', 'beans', 'nakati', 'sweet_potatoes', 'fish']

        # Adjust for diabetes
        if 'diabetes' in [c.lower() for c in conditions]:
            # Low GI foods
            recommended.extend(['beans', 'nakati', 'fish', 'sukuma_wiki'])

        # Adjust for hypertension
        if 'hypertension' in [c.lower() for c in conditions]:
            # Low sodium, high potassium
            recommended.extend(['sweet_potatoes', 'beans', 'fish', 'nakati'])

        # Add preferred foods if they're healthy
        for food in preferred:
            food_lower = food.lower().strip()
            if food_lower in self.fallback_foods_db and food_lower not in recommended:
                recommended.append(food_lower)

        # Add base foods
        for food in base_foods:
            if food not in recommended:
                recommended.append(food)

        return recommended[:8]  # Return top 8 foods

    def _create_weekly_plan(
        self,
        daily_calories: int,
        foods: List[str],
        conditions: List[str]
    ) -> Dict:
        """Create 7-day meal plan"""
        has_diabetes = 'diabetes' in [c.lower() for c in conditions]

        # Meal templates
        meal_plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for i, day in enumerate(days):
            meal_plan[day] = self._generate_day_meals(foods, has_diabetes, i)

        return meal_plan

    def _generate_day_meals(self, foods: List[str], has_diabetes: bool, day_index: int) -> Dict:
        """Generate meals for one day"""
        # Rotate foods across the week
        primary_staple = foods[day_index % len(foods)] if foods else 'matooke'

        # Breakfast templates
        breakfasts = [
            f"Sweet potatoes with beans",
            f"Porridge (millet) with groundnuts",
            f"Cassava with g-nut sauce",
        ]

        # Lunch templates
        lunches = [
            f"Steamed {primary_staple} with beans and nakati",
            f"{primary_staple.capitalize()} with fish and sukuma wiki",
            f"Beans with {primary_staple} and steamed vegetables",
        ]

        # Dinner templates (lighter)
        dinners = [
            f"Light soup with vegetables and small portion of {primary_staple}",
            f"Steamed fish with nakati",
            f"Bean stew with vegetables",
        ]

        return {
            'breakfast': breakfasts[day_index % len(breakfasts)],
            'lunch': lunches[day_index % len(lunches)],
            'dinner': dinners[day_index % len(dinners)]
        }

    def _generate_shopping_list(self, meal_plan: Dict) -> List[str]:
        """Generate shopping list from meal plan"""
        items = set()

        # Extract all foods mentioned in the meal plan
        common_items = [
            'Matooke (bunch)',
            'Beans (2 kg)',
            'Nakati (greens)',
            'Sweet potatoes (2 kg)',
            'Fish (fresh, 1 kg)',
            'Sukuma wiki (greens)',
            'Groundnuts (500g)',
            'Cassava',
            'Millet flour',
            'Cooking oil',
            'Salt (minimal for hypertension)',
            'Onions',
            'Tomatoes'
        ]

        return common_items

    def _generate_health_tips(self, conditions: List[str]) -> List[str]:
        """Generate health tips based on conditions"""
        tips = [
            "Eat smaller portions more frequently (5-6 times/day)",
            "Stay hydrated - drink 6-8 glasses of water daily",
            "Steam or boil food instead of frying",
        ]

        if 'diabetes' in [c.lower() for c in conditions]:
            tips.extend([
                "Monitor blood sugar regularly, especially after meals",
                "Choose low-GI foods like beans and vegetables",
                "Limit sweet fruits and sugary drinks"
            ])

        if 'hypertension' in [c.lower() for c in conditions]:
            tips.extend([
                "Use minimal salt in cooking",
                "Eat potassium-rich foods like sweet potatoes and beans",
                "Avoid processed and salty foods"
            ])

        return tips


# Singleton instance
_meal_plan_service = None

def get_meal_plan_service(model_loader: Optional[ModelLoader] = None, db: Optional[Session] = None) -> MealPlanService:
    """Get or create meal plan service singleton"""
    global _meal_plan_service
    if _meal_plan_service is None:
        if model_loader is None:
            # Load the global model loader
            from api.main import model_loader as global_loader
            model_loader = global_loader
        _meal_plan_service = MealPlanService(model_loader, db)
    return _meal_plan_service
