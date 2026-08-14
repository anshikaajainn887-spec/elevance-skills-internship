import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def load_medquad_data(data_folder):
    qa_pairs = []
    
    xml_files = glob.glob(os.path.join(data_folder, "**", "*.xml"), recursive=True)
    
    print(f"Found {len(xml_files)} XML files")
    
    for file_path in xml_files:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            
            for qa in root.findall(".//QAPair"):
                question = qa.findtext("Question")
                answer = qa.findtext("Answer")
                
                if question and answer:
                    qa_pairs.append({
                        "question": question.strip(),
                        "answer": answer.strip()
                    })
        except:
            continue
            
    return qa_pairs

if __name__ == "__main__":
    data_folder = "data/xml"
    
    qa_pairs = load_medquad_data(data_folder)
    
    print("Total Questions:", len(qa_pairs))
    
    if len(qa_pairs) > 0:
        print("\nFirst Question:")
        print(qa_pairs[0]["question"])
        
        print("\nFirst Answer:")
        print(qa_pairs[0]["answer"][:300])
        
        
        df = pd.DataFrame(qa_pairs)
        df.to_csv("data/medquad_clean.csv", index=False)
        print(f"\nSuccess! {len(qa_pairs)} Q&A pairs saved to data/medquad_clean.csv")
    else:
        print("No questions found. Check folder path.")