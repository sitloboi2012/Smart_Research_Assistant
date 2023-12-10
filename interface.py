import streamlit as st
import pandas as pd
from question_generator import QuestionGenerator
from web_searcher import search_paper


st.title("Personal Research Assistant :male-scientist:")
st.text("Hi, mình là Huy Mo 👨 - trợ lý ảo của bạn.")
st.text("Mình sẽ giúp bạn tìm kiếm các bài báo liên quan đến chủ đề mà bạn quan tâm.")

question_generator = QuestionGenerator()
status = None

def generate_question(topic: str, description: str):
    output = question_generator.generate_question(topic, description)
    #final_response = question_generator.filter_result(topic, description, output)
    return output.lines

def parsing_api_result(response_json):
    list_of_result = response_json["data"]
    list_of_paper_id = [i["paperId"] for i in list_of_result]
    list_of_year = [i["year"] for i in list_of_result]
    list_of_title = [i["title"] for i in list_of_result]
    list_of_abstract = [i["abstract"] for i in list_of_result]
    list_of_url = [i["url"] for i in list_of_result]
    list_of_field_study = [i["fieldsOfStudy"] for i in list_of_result]
    list_of_s2_field_study = [[field["category"] for field in i["s2FieldsOfStudy"]] for i in list_of_result]
    list_of_publication_type = [i["publicationTypes"] for i in list_of_result]
    list_of_publication_date = [i["publicationDate"] for i in list_of_result]
    list_of_authors = [[author["name"] for author in i["authors"]] for i in list_of_result]
    list_of_references = [[paper["title"] for paper in i["references"]] for i in list_of_result]
    list_of_field_study = [i["citationCount"] for i in list_of_result]
    list_of_citation = [[cite["title"] for cite in i["citations"]] for i in list_of_result]
    
    #st.write(list_of_paper_id)
    #st.write(list_of_title)
    #st.write(list_of_abstract)
    #st.write(list_of_url)
    #st.write(list_of_field_study)
    #st.write(list_of_s2_field_study)
    #st.write(list_of_publication_type)
    #st.write(list_of_publication_date)
    #st.write(list_of_authors)
    #st.write(list_of_year)
    #st.write(list_of_references)
    #st.write(list_of_citation)
    return list_of_paper_id, list_of_title, list_of_abstract, list_of_url, list_of_field_study, list_of_s2_field_study, list_of_publication_type, list_of_publication_date, list_of_authors, list_of_year, list_of_references, list_of_citation

def make_clickable(link, title):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">{title}</a>'

def convert_to_hyperlink(dataframe):
    clean_url = []
    for url, title in zip(dataframe["url"].tolist(), dataframe["title"].tolist()):
        if i is None:
            clean_url.append(None)
        else:
            clean_url.append(make_clickable(url, title))
    
    dataframe["url"] = clean_url
    return dataframe

def convert_data_to_langchain_format(dataframe):
    document = None

with st.sidebar:
    form = st.form("Topic and Description Info Form")
    topic = form.text_area("Topic", value="XR in Marketing and Business", key="topic")
    description = form.text_area("Description", value="Unleashing the Metaverse: Extended Reality (XR) in Marketing", key="description")
    related_field = form.multiselect(label = "Field of study", options = ["Business","Economics","Education","Linguistics","Engineering","Political Science","Sociology","Computer Science","Psychology"], key="related_field", default = ["Business","Economics","Education","Linguistics","Engineering","Political Science","Sociology","Computer Science","Psychology"])
    submmited = form.form_submit_button(label = 'Start finding related papers 🔎')

if submmited:
    current_total = 0
    result = {"paper_id": [], "title": [],
              "abstract": [], "url": [], "field_study": [], 
              "s2_field_study": [], "publication_type": [], "publication_date": [], 
              "authors": [], "year": [], "references": [], "citation": []}

    
    status = st.status("Finding related papers...", expanded=True)
    status.write("Generating list of keywords...")
    keyword_list = generate_question(topic, description)
    status.write("Crawling related papers...")
    progress_text = "Đợi xíu đi kiếm tài liệu cho bạn nè 🏃‍♂️"
    my_bar = st.progress(0, text=progress_text)
    for index in range(1):
        search_result = search_paper(keyword_list[index], ",".join(related_field))
        try:
            list_of_paper_id, list_of_title, list_of_abstract, list_of_url, list_of_field_study, list_of_s2_field_study, list_of_publication_type, list_of_publication_date, list_of_authors, list_of_year, list_of_references, list_of_citation = parsing_api_result(search_result)
            current_total += search_result['total']
            result["paper_id"].extend(list_of_paper_id)
            result["title"].extend(list_of_title)
            result["abstract"].extend(list_of_abstract)
            result["url"].extend(list_of_url)
            result["field_study"].extend(list_of_field_study)
            result["s2_field_study"].extend(list_of_s2_field_study)
            result["publication_type"].extend(list_of_publication_type)
            result["publication_date"].extend(list_of_publication_date)
            result["authors"].extend(list_of_authors)
            result["year"].extend(list_of_year)
            result["references"].extend(list_of_references)
            result["citation"].extend(list_of_citation)
        except KeyError:
            pass
        my_bar.progress(index + 50, text=progress_text)

    my_bar.empty()
    status.write("Polishing the result...")
    status.update(label="Kiếm xong ùi check thử xem ạ 👏", state="complete", expanded=True)
    st.markdown(f"Found __{current_total}__ papers related to the topic __{topic}__")
    st.markdown("""List of keyword that has been used to find the papers: """)
    for i in keyword_list:
        st.markdown("- " + i)
    result_df = pd.DataFrame(result)
    st.data_editor(result_df, num_rows="dynamic", column_config={"url": st.column_config.LinkColumn("URL to website")})
    #parsing_api_result(search_result)
    
    
    
    
    
    
    
    
    

