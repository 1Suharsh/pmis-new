from app.services.embeddings_recommender import EmbeddingsRecommender
from app.pm_client import fetch_internships
def combine_fields(item):
    title = item.get('title',''); comp = item.get('company',''); desc = item.get('description',''); skills = item.get('required_skills','')
    return {**item, 'combined_text': f"{title} . {comp} . {desc} . skills: {skills}"}
def main():
    listings = fetch_internships({})
    items = [combine_fields(x) for x in listings]
    rec = EmbeddingsRecommender()
    rec.build_index(items)
    print('Index built.')
if __name__ == '__main__':
    main()
