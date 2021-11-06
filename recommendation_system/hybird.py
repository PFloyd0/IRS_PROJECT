from recommendation_system import matrix_factorisation
from recommendation_system import rbm_cf_books_tf2
import pandas as pd

def do_recommendation(user_id, k=0.1):
    result = rbm_cf_books_tf2.do_recommendation(user_id)
    re = []
    for row in result.itertuples():
        re.append(getattr(row, 'RecommendationScore') + k*matrix_factorisation.do_recommendation(user_id, getattr(row, 'Id_x')))
    df = pd.DataFrame({'Name_x': result['Name_x'],
                       'Id_x': result['Id_x'],
                       'RecommendationScore': re})
    df = df.sort_values(["RecommendationScore"], ascending=False)
    return df

# do_recommendation(4)