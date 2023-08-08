from datasets import load_dataset
import json
DATASET = load_dataset("allenai/qasper")

def main():
    outputObject = []
    train = DATASET["train"]
    for paperidx, eachTrain in enumerate(train):
        dictionary = {}
        dictionary["paper_index"] = paperidx
        full_text = eachTrain["full_text"]["paragraphs"]
        flatten = flatten_list(full_text)
        flatten = [item for item in flatten if item]
        
        dictionary["passages"] = flatten
        
        questions = eachTrain["qas"]["question"]
        answersPerQuestion = eachTrain["qas"]["answers"]
        
        numQuestions = len(questions)                              

        qasArray = []

        for i in range(numQuestions):
            evidenceIndexArray = []
            currentQuestion = questions[i]
            answers = answersPerQuestion[i]
            
            for eachAnswer in answers["answer"]:
                unanswerable = eachAnswer["unanswerable"]
                if unanswerable == False:
                    allEvidence = eachAnswer["evidence"]
                    for evidenceIndex, eachEvidence in enumerate(allEvidence):
                        if eachEvidence in flatten:
                            evidenceIndexArray.append(flatten.index(eachEvidence))
            
            evidenceIndexArray = list(set(evidenceIndexArray))
            if len(evidenceIndexArray) > 0:
                questionDictionary = {}
                questionDictionary["question"] = currentQuestion
                questionDictionary["evidence"] = evidenceIndexArray
                qasArray.append(questionDictionary)
                  
                
        if len(qasArray) > 0:
            dictionary["qas"] = qasArray
            outputObject.append(dictionary)
        else:
            print(f"Article {paperidx} no evidence.")
            addDictionary = {}
            addDictionary["qas"] = []
            addDictionary["evidence"] = []
            addDictionary["passages"] = []
            outputObject.append(addDictionary)
    
    export(outputObject)



            
def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

def export(data):
    output_file = "getExperiment.json"
    with open(output_file, "w") as file:
        json.dump(data, file, indent=1)

    print(f"Data exported to {output_file}")

main()

