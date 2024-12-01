from enum import StrEnum

class KaggleDataSet(StrEnum):
    FOOD_RECIPES_AND_INGREDIENTS = 'realalexanderwei/food-com-recipes-with-ingredients-and-tags'
    FOOD_RECIPES_AND_REVIEWS     = 'irkaal/foodcom-recipes-and-reviews'
    FOOD_RECIPES_TERMS_AND_TAGS  = 'shuyangli94/foodcom-recipes-with-search-terms-and-tags'
    USDA_FOODDATA_CENTRAL        = 'johncsloan/usda-fooddata-central' # Or source the latest and greatest from https://fdc.nal.usda.gov/download-datasets.

class Paths(StrEnum):
    DATASET_ROOT                 = 'datasets'
    FOOD_DATASET                 = f'{DATASET_ROOT}/{KaggleDataSet.USDA_FOODDATA_CENTRAL}/food.csv'
    FOOD_NUTRIENT_DATASET        = f'{DATASET_ROOT}/{KaggleDataSet.USDA_FOODDATA_CENTRAL}/food_nutrient.csv'
    NUTRIENT_DATASET             = f'{DATASET_ROOT}/{KaggleDataSet.USDA_FOODDATA_CENTRAL}/nutrient.csv'
    RECIPE_TERM_TAG_DATASET      = f'{DATASET_ROOT}/{KaggleDataSet.FOOD_RECIPES_TERMS_AND_TAGS}/recipes_w_search_terms.csv'
    RESOURCE_ROOT                = 'resources'
    NUTRITION_DATA_RESOURCE      = f'{RESOURCE_ROOT}/nutrition.csv'
