import argparse
from nlp.core import process_article  # adjust if your actual import path differs

def main():
    parser = argparse.ArgumentParser(description="Run NER on a single article")
    parser.add_argument("--article-id", required=True, help="ID of the article to process")

    args = parser.parse_args()
    article_id = args.article_id

    entities = process_article(article_id)
    if entities is not None:
        print(f"✔️ Extracted {len(entities)} entities from article {article_id}")
    else:
        print(f"⚠️ No article found or article was already processed: {article_id}")

if __name__ == "__main__":
    main()