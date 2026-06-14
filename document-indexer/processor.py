from database import (
    insert_document,
    document_exists
)


def process_file(path):


    if document_exists(path):

        print(
          "Already indexed"
        )

        return



    text = read_file(path)


    summary = create_summary(
        text
    )


    keywords = extract_keywords(
        text
    )


    insert_document(
        file_name=path.name,
        path=str(path),
        summary=summary,
        keywords=keywords
    )